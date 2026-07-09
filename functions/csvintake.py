from __future__ import annotations

from pathlib import Path
import re
import typing

import numpy as np
import pandas as pd

from structs.monitor_output import MonitorOutput

PathLike = str | Path


# ---------------------------------------------------------------------------
# CSV Intake Helpers
# ---------------------------------------------------------------------------

def _normalize_column_name(column_name: str) -> str:
    """Normalize a CSV header into a simple canonical field name.

    The Airthings CSV headers use units and special characters, e.g.
    "CO2 ppm" and "TEMP °C". This helper strips units, punctuation,
    and whitespace, then converts the header to a lower-case snake-like key.
    """
    normalized = column_name.strip().lower()
    normalized = re.sub(r"\s*\(.*?\)", "", normalized)
    normalized = re.sub(r"[°%]", "", normalized)
    normalized = re.sub(r"\b(ppm|bq/m3|μg/m3|hpa|m3)\b", "", normalized)
    normalized = re.sub(r"[^a-z0-9]+", "_", normalized)
    normalized = normalized.strip("_")
    return normalized


def read_monitor_output_from_csv(path: PathLike) -> MonitorOutput:
    """Load a CSV file and convert it into a MonitorOutput object.

    This function expects a semicolon-delimited CSV with a timestamp column
    like "recorded" and a CO₂ column like "CO2 ppm". It validates the file,
    normalizes the column names, and converts the selected data to arrays.
    """
    csv_path = Path(path)

    # Ensure the file exists before attempting to parse it.
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    # Read the CSV using semicolon delimiters to match the sample data.
    df = pd.read_csv(csv_path, sep=";", skipinitialspace=True)

    if df.empty:
        raise ValueError(f"CSV file is empty: {csv_path}")

    # Normalize column names so we can detect fields reliably.
    normalized_columns = {
        original: _normalize_column_name(original)
        for original in df.columns
    }
    df = df.rename(columns=normalized_columns)

    # Verify that required fields exist after normalization.
    if "recorded" not in df.columns:
        raise ValueError(
            "Could not find a timestamp column in CSV. "
            "Expected a column like 'recorded'."
        )

    if "co2" not in df.columns:
        raise ValueError(
            "Could not find a CO2 column in CSV. "
            "Expected a column like 'CO2 ppm'."
        )

    # Parse timestamps and numeric CO2 values in their native formats.
    # The sensor CSV data can include ISO-8601 timestamps without seconds
    # or other common date/time string formats, so use mixed parsing.
    try:
        time_series = pd.to_datetime(df["recorded"], errors="raise")
    except ValueError:
        time_series = pd.to_datetime(
            df["recorded"],
            errors="raise",
            format="ISO8601",
        )

    co2_series = pd.to_numeric(df["co2"], errors="coerce")

    if co2_series.isna().any():
        raise ValueError(
            "CO2 column contains non-numeric values or missing data. "
            "Please verify the CSV contents."
        )

    if (co2_series < 0).any():
        raise ValueError("CO2 values must be non-negative.")

    # Build the MonitorOutput object from validated arrays.
    return MonitorOutput(
        co2_series=co2_series.to_numpy(dtype=float),
        time_series=time_series.to_numpy(),
    )
