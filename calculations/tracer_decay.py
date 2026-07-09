import typing as t
import numpy as np

def decay_profile(t: t.List[float], C_init: float, C_background: float, ACH: float) -> np.ndarray:
    """Calculate CO2 concentration at time t using the exponential decay model.

    Model: C(t) = C_background + (C_init - C_background) * e^(-ACH * t / 60)

    Args:
        t:            Time points in minutes relative to the peak.
        C_init:       Initial CO2 concentration at t=0 (the peak).
        C_background: Steady-state background CO2 concentration.
        ACH:          Air Changes per Hour — the ventilation rate.

    Returns:
        Array of CO2 concentrations at each time point.
    """
    return np.array(
        [C_background + (C_init - C_background) * (np.e ** (-ACH * time / 60))
         for time in t]
    )


def build_up_profile(t: t.List[float], C_valley: float, C_peak: float, ACH: float) -> np.ndarray:
    """Calculate CO2 concentration at time t during the build-up phase.

    Model: C(t) = C_peak + (C_valley - C_peak) * (1 - e^(-ACH * t / 60))

    Args:
        t:        Time points in minutes relative to the build-up start.
        C_valley: CO2 concentration at the start of the build-up (the valley floor).
        C_peak:   Target steady-state CO2 concentration (the peak ceiling).
        ACH:      Air Changes per Hour — the ventilation rate.

    Returns:
        Array of CO2 concentrations at each time point.
    """
    return np.array(
        [C_peak + (C_valley - C_peak) * (1 - np.e ** (-ACH * time / 60))
         for time in t]
    )