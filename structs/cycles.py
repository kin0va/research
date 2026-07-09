import numpy as np
import pandas as pd

class BuildUpDecayCycle:
    """
    Represents a single build-up and decay cycle in CO₂ data.
    """

    def __init__(self, peak_idx: int, valley_idx: int, co2_series: np.ndarray):
        self.peak_idx = peak_idx
        self.valley_idx = valley_idx
        self.co2_series = co2_series

    @property
    def peak_value(self) -> float:
        return self.co2_series[self.peak_idx]

    @property
    def valley_value(self) -> float:
        return self.co2_series[self.valley_idx]

    @property
    def duration(self) -> int:
        return self.peak_idx - self.valley_idx

    def __repr__(self):
        return (
            f"BuildUpDecayCycle(peak_idx={self.peak_idx}, "
            f"valley_idx={self.valley_idx}, "
            f"peak_value={self.peak_value:.2f}, "
            f"valley_value={self.valley_value:.2f}, "
            f"duration={self.duration})"
        )