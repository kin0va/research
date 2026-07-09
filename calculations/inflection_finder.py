"""Peak and valley detection, pairing, and validation."""

from typing import List, Tuple

import numpy as np
import pandas as pd
from scipy import signal

from classes.cycles import BuildUpDecayCycle


def find_peaks_and_valleys(dataframe: pd.DataFrame, order: int = 200) -> Tuple[List[int], List[int]]:
    """Find local maxima (peaks) and minima (valleys) in CO2 data."""
    arr = np.array(list(dataframe["co2"]))
    peaks = list(signal.find_peaks(arr, distance=order)[0])
    valleys = list(signal.find_peaks(-arr, distance=order)[0])
    print(f"Initial detection found {len(peaks)} peaks and {len(valleys)} valleys.")
    print(f"CO2 range: {dataframe['co2'].min():.1f} – {dataframe['co2'].max():.1f} ppm")
    print(f"CO2 mean:  {dataframe['co2'].mean():.1f} ppm")
    return peaks, valleys


def filter_peaks(dataframe: pd.DataFrame, peaks: List[int], valleys: List[int], peak_floor: float):
    """Filter peaks to keep only those above the floor and with a preceding valley."""
    valid_peaks: List[int] = []
    invalid_peaks: List[int] = []
    data = dataframe["co2"]
    for peak_idx in peaks:
        if data[peak_idx] <= peak_floor:
            invalid_peaks.append(peak_idx)
        else:
            preceding_valleys = [valley_idx for valley_idx in valleys if valley_idx < peak_idx]
            if not preceding_valleys:
                invalid_peaks.append(peak_idx)
            else:
                valid_peaks.append(peak_idx)
    return valid_peaks, invalid_peaks


def filter_valleys(dataframe: pd.DataFrame, peaks: List[int], valleys: List[int], valley_ceiling: float):
    """Filter valleys to keep only those below the ceiling and with a following peak."""
    valid_valleys: List[int] = []
    invalid_valleys: List[int] = []
    data = dataframe["co2"]
    for valley_idx in valleys:
        if data[valley_idx] >= valley_ceiling:
            invalid_valleys.append(valley_idx)
        else:
            following_peaks = [peak_idx for peak_idx in peaks if peak_idx > valley_idx]
            if not following_peaks:
                invalid_valleys.append(valley_idx)
            else:
                valid_valleys.append(valley_idx)
    return valid_valleys, invalid_valleys


def identify_valid_peak_valley_pairs(dataframe: pd.DataFrame, order: int = 200) -> tuple[List[BuildUpDecayCycle], tuple[List[int], List[int]]]:
    """
    Identify valid peak-valley cycles from the dataframe with filtering.
    Iteratively filter invalid points until no new invalid peaks or valleys are found.

    Args:
        dataframe: DataFrame with 'co2' and 'datetime' columns.
        order: Minimum number of points on each side to consider local extremum.

    Returns:
        (valid_cycles, (excluded_peaks, excluded_valleys)) where valid_cycles is a list of BuildUpDecayCycle objects and the second element is a tuple of lists of excluded peak and valley indices.
    """
    co2 = dataframe['co2']

    # Use robust but permissive thresholds so the standard sample data still
    # yields cycles while invalid outliers are filtered out.
    peak_floor = float(co2.quantile(0.35))
    valley_ceiling = float(co2.quantile(0.65))

    print(f"Thresholds — peak floor: {peak_floor:.1f}, valley ceiling: {valley_ceiling:.1f}")
    excluded_peaks: List[int] = []
    excluded_valleys: List[int] = [] 
    valid =  []
    peaks, valleys = find_peaks_and_valleys(dataframe, order=order)
    #Clear condition to loop until no new pairs are found
    invalid_remaining = True
    while invalid_remaining:
        #Filter peaks and valleys based on the current lists of peaks and valleys
        valid_peaks, invalid_peaks = filter_peaks(dataframe, peaks, valleys, peak_floor)
        valid_valleys, invalid_valleys = filter_valleys(dataframe, peaks, valleys, valley_ceiling)
        #If no new invalid peaks or valleys are found, we have our final valid pairs
        if not invalid_peaks and not invalid_valleys:
            invalid_remaining = False
            break
        #Add excluded points to the lists of excluded peaks and valleys
        excluded_peaks.extend(invalid_peaks)
        excluded_valleys.extend(invalid_valleys)
        #Create new lists of peaks and valleys for the next iteration
        peaks = [p for p in valid_peaks if p not in excluded_peaks]
        valleys = [v for v in valid_valleys if v not in excluded_valleys]

    # Create BuildUpDecayCycle objects for the valid peaks and valleys.
    # Each peak is paired with the nearest preceding valley that still has a
    # following peak, which matches the intended build-up/decay cycle shape.
    for p in peaks:
        preceding_valleys = [v for v in valleys if v < p]
        if not preceding_valleys:
            continue

        first_valley = max(preceding_valleys)
        # this needs to be fixed as data can have multiple peaks and valleys in a row
        valid.append(
            BuildUpDecayCycle(
                peak_idx=p,
                valley_idx=first_valley,
                co2_series=np.array(dataframe['co2']),
            )
        )

    return valid, (excluded_peaks, excluded_valleys)
