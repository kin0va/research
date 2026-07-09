from classes.sitedata import SiteData
from classes.room_params import RoomParams
from classes.plotting_data import PlottingData

import scipy.signal as signal
import numpy as np
import pandas as pd
from filterpy.kalman import UnscentedKalmanFilter, MerweScaledSigmaPoints
from classes.state_machine import occupancy_state_machine
from typing import List


def apply_kalman_filter(sitedata: SiteData, room_params: RoomParams) -> PlottingData:
    """
    Apply Kalman filter to the CO2 data in sitedata.monitor_output.
    Uses the filter to calculate occupancy and monitor ACH.

    Args:
        sitedata: SiteData object containing the CO2 data and room parameters.
        room_params: RoomParams object containing the room parameters.

    Returns:
        PlottingData object containing the filtered occupancy and ACH data.
    """

    points = MerweScaledSigmaPoints(n=2, alpha=0.1, beta=2.0, kappa=0)
    ukf = UnscentedKalmanFilter(dim_x=2, dim_z=1, dt=300, fx=fx, hx=hx, points=points)
    ukf.x = np.array([0.0, 1.0])          # initial [N, ACH]
    ukf.P = np.diag([25.0, 0.5])
    ukf.Q = np.diag([4.0, 0.01])          # asymmetric process noise — still yours to tune
    ukf.R = np.array([[272.0]])           # measurement variance from your noise diagnostics
    N_out = np.zeros(len(sitedata.monitor_output.co2_series))
    ACH_out = np.zeros(len(sitedata.monitor_output.co2_series))
    for i in range(len(sitedata.monitor_output.co2_series) - 1):
        dt_s = sitedata.monitor_output.time_series[i + 1] - sitedata.monitor_output.time_series[i]
        ukf.predict(dt=dt_s)
        ukf.update(z=[sitedata.monitor_output.co2_series[i + 1]], hx=lambda x: hx(x, sitedata.monitor_output.co2_series[i], dt_s, room_params))
        N_out[i], ACH_out[i] = ukf.x

    return PlottingData(
        site_data=sitedata,
        monitor_output=sitedata.monitor_output,
        room_params=room_params,
        occupancy_series=N_out.tolist(),
        ACH_series=ACH_out.tolist()
    )

def fx(x, dt):
    """State transition — random walk, nothing to debug here."""
    return x  # [N, ACH] unchanged; filterpy adds process noise Q separately

def hx(x, C_i, dt_s, params):
    """Observation model — predicted next CO2 given current state."""
    N, ACH = x
    ACH = max(ACH, 0.05)
    C_eq = params.c_amb + (N * params.cpp_per_person) / ACH
    alpha = np.exp(-ACH * dt_s / 3600.0)
    return np.array([C_eq + (C_i - C_eq) * alpha])