from pathlib import Path
import pandas as pd

from filters.peak_valley import identify_valid_peak_valley_pairs
from functions.csvintake import read_monitor_output_from_csv
from classes.sitedata import SiteData
from calculations.occupancy import Cali_Occupancy_Equation

def build_site_data(room_json: Path, monitor_csv: Path, order: int = 200) -> SiteData:
    monitor_output = read_monitor_output_from_csv(monitor_csv)
    site_data = SiteData.from_json(
        room_json,
        monitor_output=monitor_output,
        cycles=[],
    )

    dataframe = pd.DataFrame(
        {
            "co2": monitor_output.co2_series,
            "datetime": monitor_output.time_series,
        }
    )
    valid_cycles, (excluded_peaks, excluded_valleys) = identify_valid_peak_valley_pairs(
        dataframe,
        order=order,
    )

    site_data.cycles = valid_cycles
    site_data.valid_cycles = valid_cycles
    site_data.invalid_cycles = []
    site_data.invalid_peaks = excluded_peaks
    site_data.invalid_valleys = excluded_valleys
    return site_data

def calculate_occupancy(site_data: SiteData) -> None:
    """
    Calculate the occupancy profile for the given SiteData object using the Cali occupancy equation.
    This function modifies the SiteData object in place by adding the occupancy_series attribute.

    Args:
        site_data: A SiteData object containing room metadata and monitor output.
    """
    co2_series = site_data.monitor_output.co2_series
    delta_t_s = site_data.monitor_output.time_series
    params = site_data.room_params
    