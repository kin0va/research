from classes.state_machine import occupancy_state_machine
from classes.sitedata import SiteData
from classes.room_params import RoomParams
from classes.plotting_data import PlottingData
from classes.occupancy_params import OccupancyParameters

from cli.updater import RuntimeUpdater

from calculations.tracer_decay import build_up_profile
from calculations.occupancy import Cali_Occupancy_Equation
from calculations.ach import ACH_tracer_decay

from scipy.optimize import curve_fit
import numpy as np


def _pre_buildup_baseline(co2_series: np.ndarray, start_idx: int, lookback: int = 10) -> float:
    """
    Estimate the steady-state 'valley' CO2 concentration immediately preceding
    a build-up (occupied) period, by averaging the samples right before it.
    """
    window_start = max(0, start_idx - lookback)
    baseline_window = co2_series[window_start:start_idx]
    if len(baseline_window) == 0:
        return co2_series[start_idx]
    return float(np.mean(baseline_window))

def _prior_decay_ach(
    co2_series: np.ndarray,
    time_series,
    start_idx: int,
    c_background: float,
    lookback: int = 10,
    default: float = 1.0,
) -> float:
    """
    Estimate ACH from the decay immediately preceding a build-up period,
    using the same lookback window as the C_valley baseline. Used as the
    initial guess for the build-up curve fit — a real prior beats a
    hardcoded constant, especially when ventilation varies cycle to cycle.
    """
    window_start = max(0, start_idx - lookback)
    if window_start >= start_idx - 1:
        return default

    c_init = float(co2_series[window_start])
    c_final = float(co2_series[start_idx - 1])
    t_minutes = (time_series[start_idx - 1] - time_series[window_start]).total_seconds() / 60

    if t_minutes <= 0 or c_final <= c_background or c_init <= c_background:
        # Not a valid decay (flat, rising, or already at background) — fall back
        return default

    try:
        ach = ACH_tracer_decay(c_init, c_background, c_final, t_minutes)
    except ValueError:
        return default

    if not np.isfinite(ach) or ach <= 0:
        return default

    return ach

def fit_build_up_ach(
    t_minutes: np.ndarray,
    co2_segment: np.ndarray,
    C_valley: float,
    ach_initial_guess: float = 1.0,
    param_range: float = 5000.0,
):
    def model(t, C_peak, ACH):
        return build_up_profile(t, C_valley, C_peak, ACH)

    lower = [C_valley, 0.01]
    upper = [param_range, 20.0]

    p0 = [
        float(np.clip(co2_segment.max(), lower[0] + 1e-6, upper[0])),
        float(np.clip(ach_guess if (ach_guess := ach_initial_guess) and np.isfinite(ach_guess) else 1.0,
                       lower[1], upper[1])),
    ]

    try:
        popt, _ = curve_fit(model, t_minutes, co2_segment, p0=p0, bounds=(lower, upper))
        C_peak_fit, ACH_fit = popt
        fitted_series = model(t_minutes, *popt)
        return C_peak_fit, ACH_fit, fitted_series
    except (RuntimeError, ValueError) as exc:
        print(f"Build-up fit failed (C_valley={C_valley:.1f}): {exc}")
        return None


def model_buildup(data: SiteData, room_params: RoomParams, runtime: RuntimeUpdater) -> PlottingData:
    """
    For each occupied period:
      1. Take the steady-state CO2 just before it as C_valley.
      2. Fit the build-up model over the period to estimate ACH.
      3. Use that ACH in the Cali occupancy equation to estimate occupancy.
    """
    occupancy_state_machine(data, runtime)

    co2_series = data.monitor_output.co2_series
    time_series = data.monitor_output.time_series

    occupancy_out = np.zeros(len(co2_series))
    ACH_out = np.full(len(co2_series), np.nan)

    occ_params = OccupancyParameters(
        volume=room_params.volume,
        c_amb=room_params.c_amb if room_params.c_amb is not None else 420,
        cpp_per_person=room_params.cpp_per_person if room_params.cpp_per_person is not None else 5e-6,
    )

    with runtime.create_progress() as progress:
        task = progress.add_task("[cyan]Modelling build-up periods...", total=len(data.occupied_periods))

        for start_time, end_time in data.occupied_periods:
            mask = (time_series >= start_time) & (time_series <= end_time)
            idx = np.where(mask)[0]

            if len(idx) < 3:
                progress.advance(task)
                continue

            period_co2 = co2_series[idx]
            period_time = time_series[idx]

            t_minutes = np.array(
                [(ts - period_time[0]).total_seconds() / 60 for ts in period_time]
            )

            C_valley = _pre_buildup_baseline(co2_series, idx[0])
            ach_guess = _prior_decay_ach(co2_series, time_series, idx[0], occ_params.c_amb)

            fit_result = fit_build_up_ach(t_minutes, period_co2, C_valley, ach_initial_guess=ach_guess)
            if fit_result is None:
                progress.advance(task)
                continue

            _, ACH_fit, _ = fit_result

            delta_t_s = np.array(
                [(period_time[i + 1] - period_time[i]).total_seconds()
                 for i in range(len(period_time) - 1)]
                + [0.0]
            )

            period_occupancy = Cali_Occupancy_Equation(period_co2, delta_t_s, ACH_fit, occ_params)

            occupancy_out[idx] = period_occupancy
            ACH_out[idx] = ACH_fit

            progress.advance(task)

    return PlottingData(
        site_data=data,
        monitor_output=data.monitor_output,
        room_params=room_params,
        occupancy_series=occupancy_out.tolist(),
        ACH_series=ACH_out.tolist(),
    )