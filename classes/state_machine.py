from classes.sitedata import SiteData
import typing as t
import pandas as pd
import numpy as np

def validate_occupied_periods(start_time: pd.Timestamp, end_time: pd.Timestamp, co2_series: pd.Series, time_series: pd.Series) -> bool:
    """
    Validate the occupied period based on the room parameters and monitor output.
    Returns True if the period is valid, False otherwise.
    """
    # Example validation logic: Check if the duration of the occupied period is reasonable
    duration = (end_time - start_time).total_seconds() / 60  # duration in minutes
    if duration < 5 or duration > 480:  # less than 5 minutes or more than 8 hours
        return False

    # Additional validation logic can be added here based on room_params and monitor_output

    return True

def occupancy_state_machine(sitedata: SiteData):
    """"
    State machine to be ran over dataset to determine occupied vs unoccupied periods.
    It modifies the sitedata.occupied_periods list in place, which is a list of tuples of (start_time, end_time) for each occupied period.
    """
    occupancy_threshold = 450 #Initial threshold for occupancy detection CO2 in ppm, can be adjusted based on the specific site and conditions.

    state = "unoccupied"

    start_time = None # type: ignore
    end_time = None # type: ignore

    for index, row in sitedata.monitor_output.to_dataframe().iterrows():
        time = row["Time"]
        co2 = row["CO2"]

        if state == "unoccupied":
            if co2 > occupancy_threshold:
                state = "occupied"
                start_time : pd.Timestamp = time
        elif state == "occupied":
            if co2 < occupancy_threshold:
                state = "unoccupied"
                end_time: pd.Timestamp = time
                # Validate the occupied period before appending
                if validate_occupied_periods(start_time, end_time, sitedata.monitor_output.to_dataframe()["CO2"], sitedata.monitor_output.to_dataframe()["Time"]):
                    sitedata.occupied_periods.append((start_time, end_time))
                    start_time = None # type: ignore
                    end_time = None  # type: ignore

                else:
                    # If the period is invalid, we can choose to log it or handle it differently
                    print(f"Invalid occupied period from {start_time} to {end_time}. Not added to occupied_periods.")
                    start_time = None # type: ignore
                    end_time = None  # type: ignore