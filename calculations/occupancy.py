import numpy as np
import typing as t
from classes.occupancy_params import OccupancyParameters

def Cali_Occupancy_Equation(co2_series: np.ndarray, delta_t_s: np.ndarray, ACH_decay: float, params: OccupancyParameters) -> np.ndarray:
    C_amb = params.c_amb
    G = params.cpp_per_person   # m³/s of CO2 per person, ~5e-6 at rest
    V = params.volume           # m³

    occupancy = np.zeros_like(co2_series)

    for i in range(len(co2_series) - 1):
        dt = delta_t_s[i]
        C_i = co2_series[i]
        C_next = co2_series[i + 1]

        alpha = np.exp(-ACH_decay * dt / 3600.0)
        denom = 1 - alpha
        if denom < 1e-4:
            occupancy[i] = np.nan
            continue

        C_eq = (C_next - C_i * alpha) / denom
        # C_eq = C_amb + N*G*3.6e9/(V*ACH)  →  solve for N
        occupancy[i] = ACH_decay * V * (C_eq - C_amb) / (G * 3.6e9)

    return occupancy