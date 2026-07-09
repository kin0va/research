import numpy as np
import typing as t
from structs.occupancy_params import OccupancyParameters

def Cali_Occupancy_Equation(co2_series: np.ndarray, delta_t_s: np.ndarray, ACH_decay: float, params:OccupancyParameters,) -> np.ndarray:
    """
    This function uses the occupancy equation of Cali et al. to calculate the occupancy profile.

    Formula:
            C[i+1] = (1 - mairx x ^t/(rho x V)) x  C[i] + mv_amb x ^t/(rho x V) x  C_amb + mv_in x ^t/(rho x V) x  C_adj + nocc x ^t/V x  CpPp CHECK WITH FRESH EYES
    Where:
        C[i]: CO2 concentration at time step i
        mairx: mass of air in the room (rho x V)
        t: time step duration in seconds
        rho: density of air
        V: volume of the room
        mv_amb: mass flow rate of ambient air
        C_amb: CO2 concentration of ambient air
        mv_in: mass flow rate of incoming air (e.g., from ventilation)
        C_adj: CO2 concentration of incoming air
        nocc: number of occupants
        CpPp: CO2 production per person

    Rearranging the formula to solve for nocc gives:
            nocc = (C[i+1] - (1 - mairx x ^t/(rho x V)) x  C[i] - mv_amb x ^t/(rho x V) x  C_amb - mv_in x ^t/(rho x V) x  C_adj) / ( ^t/V x  CpPp) CHECK WITH FRESH EYES

    Args:
        co2_series: Array of CO2 concentrations at each time step.
        delta_t_s: Array of time step durations in seconds.
        ACH_decay: Air Changes per Hour from the decay phase.
        params: OccupancyParameters object containing physical constants.

    Returns:
        Array of estimated occupancy (number of occupants) at each time step.
    """
    #initialise variables
    V = params.volume
    rho = params.rho_air
    co2pp = params.cpp_per_person
    ambco2 = params.c_amb
    adjco2 = params.c_adj
    mv_in = params.m_v_in

    # Calculate mass of air in the room
    mairx = rho * V

    #initialise occupancy numpy array
    occupancy = np.zeros_like(co2_series)

    for i in range(len(co2_series) - 1):
        delta_t = delta_t_s[i]
        C_i = co2_series[i]
        C_next = co2_series[i + 1]

        # Calculate the occupancy using the rearranged formula
        occupancy[i] = (C_next - (1 - mairx * np.exp(-ACH_decay * delta_t / 3600)) * C_i - (mv_in * np.exp(-ACH_decay * delta_t / 3600) / (rho * V)) * adjco2 - (ambco2 * np.exp(-ACH_decay * delta_t / 3600) / (rho * V))) / ((delta_t / V) * co2pp)

    return occupancy
