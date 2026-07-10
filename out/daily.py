"""Single-day CO2 plots."""

from __future__ import annotations

import typing as t

import matplotlib.dates as mdates
from matplotlib.axes import Axes

from out.style import CO2_BACKGROUND_PPM, COLOR_CO2
from out.base import new_figure, style_axis, mark_cycles, save_figure

if t.TYPE_CHECKING:
    import pandas as pd
    from classes.cycles import BuildUpDecayCycle
    from classes.plotting_data import PlottingData


def plot_daily(
    plotting_data: "PlottingData",
    day_label: str,
    title: t.Optional[str] = None,
    ax: t.Optional[Axes] = None,
    savepath: t.Optional[str] = None,
) -> Axes:
    """Plot one day's CO2 trace against time-of-day.

    Args:
        plotting_data: a PlottingData object containing SiteData, monitor output,
            and Kalman-derived series.
        day_label: label for the day to plot, matching SiteData.days_data keys.
        title: plot title. Defaults to the day label if omitted.
        ax: existing Axes to draw into (for grids); otherwise a new
            Figure/Axes is created.
        savepath: if provided (and ax was None), saves the figure here.
    """
    day_frames = plotting_data.site_data.days_data
    try:
        df = day_frames[day_label]
    except KeyError as exc:
        raise ValueError(
            f"Day label {day_label!r} not found in PlottingData.site_data.days_data"
        ) from exc

    day_start = df["Time"].iloc[0]
    day_end = df["Time"].iloc[-1]
    cycles = [
        cycle
        for cycle in plotting_data.site_data.valid_cycles
        if day_start <= plotting_data.monitor_output.time_series[cycle.peak_idx] <= day_end
    ]

    original_ax = ax
    if ax is None:
        fig, ax = new_figure()
    else:
        fig = ax.figure

    if df.empty:
        ax.text(0.5, 0.5, "No data", ha="center", va="center", transform=ax.transAxes)
        style_axis(ax, title=title)
        if savepath and original_ax is None:
            save_figure(fig, savepath) #type: ignore
        return ax

    ax.plot(df["Time"], df["CO2"], color=COLOR_CO2, linewidth=1.2, label="CO₂")
    ax.axhline(CO2_BACKGROUND_PPM, color="grey", linestyle="--", linewidth=0.8,
               alpha=0.7, label="Ambient (~420 ppm)")

    if cycles:
        mark_cycles(ax, cycles, plotting_data.monitor_output.time_series) #type: ignore

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=3))
    ax.set_xlabel("Time of day")

    default_title = title if title is not None else day_label
    style_axis(ax, title=default_title)

    if savepath and original_ax is None:
        save_figure(fig, savepath) #type: ignore
    return ax