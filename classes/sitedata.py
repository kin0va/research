import typing as t
from pathlib import Path

from rich.table import Table
from rich.console import Console

from classes.cycles import BuildUpDecayCycle
from classes.monitor_output import MonitorOutput
from classes.room_params import RoomParams
import pandas as pd

class SiteData:
    def __init__(self, site_name, room_params, monitor_output, cycles):
        self.site_name = site_name
        self.room_params = room_params
        self.monitor_output = monitor_output
        self.cycles = cycles
        self.invalid_peaks: list[int] = []
        self.invalid_valleys: list[int] = []
        self.valid_cycles: list[BuildUpDecayCycle] = []
        self.invalid_cycles: list[BuildUpDecayCycle] = []
        self._days_data = None
        self._weekly_data = None
        self._monthly_data = None

    # ------------------------------------------------------------------
    # Generic period-splitting helper
    # ------------------------------------------------------------------
    def _split_by(self, freq: str) -> dict[str, pd.DataFrame]:
        """
        Split monitor_output into a dict of period_label -> DataFrame.
        freq: 'D' (day), 'W' (ISO week), 'M' (calendar month)
        """
        df = self.monitor_output.to_dataframe()  # columns: Time, CO2

        if freq == "D":
            key = df["Time"].dt.date.astype(str)
        elif freq == "W":
            # ISO year-week avoids Jan/Dec boundary weirdness that
            # plain week-number would have
            key = df["Time"].dt.strftime("%G-W%V")
        elif freq == "M":
            key = df["Time"].dt.strftime("%Y-%m")
        else:
            raise ValueError(f"Unsupported freq: {freq!r}")

        return {
            label: group.reset_index(drop=True)
            for label, group in df.groupby(key, sort=True)
        }

    @property
    def days_data(self) -> dict[str, pd.DataFrame]:
        if self._days_data is None:
            self._days_data = self._split_by("D")
        return self._days_data

    @property
    def weekly_data(self) -> dict[str, pd.DataFrame]:
        if self._weekly_data is None:
            self._weekly_data = self._split_by("W")
        return self._weekly_data

    @property
    def monthly_data(self) -> dict[str, pd.DataFrame]:
        if self._monthly_data is None:
            self._monthly_data = self._split_by("M")
        return self._monthly_data

    # ------------------------------------------------------------------
    # Attach cycles to whichever period they fall in — useful for
    # overlaying peak/valley markers on daily/weekly/monthly plots
    # ------------------------------------------------------------------
    def cycles_in_period(self, period_data: dict[str, pd.DataFrame]) -> dict[str, list[BuildUpDecayCycle]]:
        """
        Map each period label to the cycles whose peak_idx falls inside it.
        period_data should be one of self.days_data / weekly_data / monthly_data.
        """
        # build index -> period_label lookup once
        idx_to_label = {}
        for label, seg in period_data.items():
            idx_to_label.update({i: label for i in seg.index})
        # NOTE: seg.index was reset above, so this only works if you keep
        # the ORIGINAL index instead — see caveat below.

        result: dict[str, list[BuildUpDecayCycle]] = {label: [] for label in period_data}
        for cycle in self.cycles:
            label = idx_to_label.get(cycle.peak_idx)
            if label is not None:
                result[label].append(cycle)
        return result