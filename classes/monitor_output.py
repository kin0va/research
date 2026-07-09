from __future__ import annotations

import typing

import numpy as np
import pandas as pd


class MonitorOutput:
    """
    Stores the continuous output from the CO₂ monitor.
    """

    def __init__(
        self,
        co2_series: np.ndarray,
        time_series: np.ndarray,
    ):

        if not (
            len(co2_series)
            == len(time_series)
        ):
            raise ValueError(
                "CO₂, temperature and time series must have equal length."
            )

        self.co2_series = np.asarray(co2_series)
        self.time_series = pd.to_datetime(time_series)

    def to_dataframe(self) -> pd.DataFrame:
        """
        Convert monitor output into a pandas DataFrame.
        """

        return pd.DataFrame(
            {
                "Time": self.time_series,
                "CO2": self.co2_series,
            }
        )

    def __repr__(self):

        return (
            f"MonitorOutput("
            f"{len(self.co2_series)} samples)"
        )


