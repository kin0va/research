import typing as t
import numpy as np

def ACH_steady_state(c_indoor: float, c_outdoor: float, G: float) -> float:
    """
    This function calculates the Air Changes per Hour (ACH). 
    It uses the steady-state CO2 concentration, the background CO2 concentration, and the initial CO2 concentration to compute the ACH value.
    It is used in scenarios where the CO2 concentration reaches a steady state, allowing for the calculation of the ventilation rate. 

    Args:
        c_indoor (float): The steady-state indoor CO2 concentration (ppm).
        c_outdoor (float): The outdoor/background CO2 concentration (ppm).
        G (float): The CO2 generation rate (ppm per hour).
    
    Returns:
        float: The calculated ACH value.
    """
    
    if c_indoor <= c_outdoor:
        raise ValueError("Indoor CO2 concentration must be greater than outdoor CO2 concentration for ACH calculation.")
    
    return G / (c_indoor - c_outdoor)

def ACH_tracer_decay(c_init: float, c_background: float, c_final: float, t: float) -> float:
    """
    This function calculates the Air Changes per Hour (ACH) using the tracer decay method.
    It uses the initial CO2 concentration, the background CO2 concentration, the final CO2 concentration after a certain time period, and the time elapsed to compute the ACH value.
    It is used in scenarios where the CO2 concentration decays over time, allowing for the calculation of the ventilation rate based on the decay rate.

    Args:
        c_init (float): The initial CO2 concentration at time t=0 (ppm).
        c_background (float): The background CO2 concentration (ppm).
        c_final (float): The final CO2 concentration after time t (ppm).
        t (float): The time elapsed in minutes.
    
    Returns:
        float: The calculated ACH value.
    """
    
    if c_final <= c_background:
        raise ValueError("Final CO2 concentration must be greater than background CO2 concentration for ACH calculation.")
    
    return -60 / t * np.log((c_final - c_background) / (c_init - c_background))

def ACH_build_up(c_init: float, c_background: float, c_final: float, t: float) -> float:
    """
    This function calculates the Air Changes per Hour (ACH) using the build-up method.
    It uses the initial CO2 concentration, the background CO2 concentration, the final CO2 concentration after a certain time period, and the time elapsed to compute the ACH value.
    It is used in scenarios where the CO2 concentration builds up over time, allowing for the calculation of the ventilation rate based on the build-up rate.

    Args:
        c_init (float): The initial CO2 concentration at time t=0 (ppm).
        c_background (float): The background CO2 concentration (ppm).
        c_final (float): The final CO2 concentration after time t (ppm).
        t (float): The time elapsed in minutes.
    
    Returns:
        float: The calculated ACH value.
    """
    
    if c_final <= c_background:
        raise ValueError("Final CO2 concentration must be greater than background CO2 concentration for ACH calculation.")
    
    return 60 / t * np.log((c_final - c_background) / (c_init - c_background))