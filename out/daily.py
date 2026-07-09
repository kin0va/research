"""Single-day CO2 plots."""

from __future__ import annotations

import typing as t

import matplotlib.dates as mdates
from matplotlib.axes import Axes

from out.style import (
    CO2_BACKGROUND_PPM, COLOR_CO2, finish, new_ax, overlay_cycles, style_axes,
)

if t.TYPE_CHECKING:
    import pandas as pd
    from classes.cycles import BuildUpDecayCycle


def plot_daily(
    df: "pd.DataFrame",
    cycles: t.Optional[list["BuildUpDecayCycle"]] = None,
    title: t.Optional[str] = None,
    ax: t.Optional[Axes] = None,
    savepath: t.Optional[str] = None,
) -> Axes:
    """Plot one day's CO2 trace against time-of-day.

    Args:
        df: a value from SiteData.days_data — columns 'Time', 'CO2',
            index preserved from the original monitor_output series.
        cycles: cycles whose peak/valley fall within this day, e.g. from
            SiteData.cycles_in_period(SiteData.days_data)[day_label].
        title: plot title. Defaults to the date if omitted.
        ax: existing Axes to draw into (for grids); otherwise a new
            Figure/Axes is created.
        savepath: if provided (and ax was None), saves the figure here.
    """
    fig, ax = new_ax(ax)

    if df.empty:
        ax.text(0.5, 0.5, "No data", ha="center", va="center", transform=ax.transAxes)
        style_axes(ax, title=title)
        return finish(fig, ax, savepath)

    ax.plot(df["Time"], df["CO2"], color=COLOR_CO2, linewidth=1.2, label="CO₂")
    ax.axhline(CO2_BACKGROUND_PPM, color="grey", linestyle="--", linewidth=0.8,
               alpha=0.7, label="Ambient (~420 ppm)")

    overlay_cycles(ax, df, cycles)

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=3))
    ax.set_xlabel("Time of day")

    default_title = df["Time"].iloc[0].date().isoformat() if title is None else title
    style_axes(ax, title=default_title)

    return finish(fig, ax, savepath)