"""
graphing/base.py
=================
Shared plotting helpers used by every module in graphing/ (box_plot, scatter_plot,
daily, weekly, monthly). These wrap the raw matplotlib calls so individual plot
files stay ~15-30 lines and never touch rcParams, hex colors, or spine/grid
formatting directly.

Typical usage inside e.g. graphing/daily.py:

    from pathlib import Path
    from graphing.base import new_figure, style_axis, shade_co2_bands, mark_cycles, save_figure

    def plot_daily_co2(df, cycles, out_path: Path):
        fig, ax = new_figure()
        shade_co2_bands(ax, df["datetime"].min(), df["datetime"].max())
        ax.plot(df["datetime"], df["co2"], color=PALETTE["co2_line"], linewidth=1.2)
        mark_cycles(ax, cycles, df)
        style_axis(ax, title="Daily CO2", xlabel="Time", ylabel="CO2 (ppm)")
        save_figure(fig, out_path)
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional, Sequence

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from out.style import PALETTE, CO2_BANDS, FIG_WIDTH_IN, FIG_HEIGHT_IN, apply_style

# Apply the global style as soon as this module is imported, so any caller
# that imports graphing.base gets consistent figures without an extra step.
apply_style()


# ---------------------------------------------------------------------------
# Figure / axis setup
# ---------------------------------------------------------------------------

def new_figure(
    nrows: int = 1,
    ncols: int = 1,
    figsize: Optional[tuple[float, float]] = None,
    sharex: bool = False,
) -> tuple[Figure, Axes]:
    """Create a figure/axes pair with project defaults already applied
    (rcParams handles color/grid/spines; this just handles sizing)."""
    fig, ax = plt.subplots(
        nrows=nrows,
        ncols=ncols,
        figsize=figsize or (FIG_WIDTH_IN, FIG_HEIGHT_IN),
        sharex=sharex,
    )
    return fig, ax


def style_axis(
    ax: Axes,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    legend: bool = False,
) -> None:
    """Apply consistent title/label formatting. Grid/spines already come from
    rcParams — this only handles the per-plot text and optional legend."""
    if title:
        ax.set_title(title, pad=12)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    if legend:
        ax.legend(loc="upper right")


def format_datetime_axis(ax: Axes, span_hours: float) -> None:
    """Pick a sensible date/time tick formatter based on how much time the
    x-axis spans, so daily/weekly/monthly plots don't each hand-roll this."""
    if span_hours <= 30:
        locator = mdates.HourLocator(interval=2)
        fmt = mdates.DateFormatter("%H:%M")
    elif span_hours <= 24 * 10:
        locator = mdates.DayLocator()
        fmt = mdates.DateFormatter("%b %d")
    else:
        locator = mdates.WeekdayLocator(interval=1)
        fmt = mdates.DateFormatter("%b %d")
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(fmt)
    ax.figure.autofmt_xdate(rotation=30, ha="right")


# ---------------------------------------------------------------------------
# Domain-specific helpers (CO2 bands, cycles)
# ---------------------------------------------------------------------------

def shade_co2_bands(ax: Axes, x_start, x_end, bands: Sequence[tuple] = CO2_BANDS) -> None:
    """Shade horizontal bands across the full x-range for each CO2 comfort
    threshold (Good / Moderate / Poor). Call this BEFORE plotting the line
    series so the shading sits behind the data."""
    for lower, upper, color, _label in bands:
        ax.axhspan(lower, upper, xmin=0, xmax=1, color=color, zorder=0)


def mark_cycles(ax: Axes, cycles: Iterable, datetimes: Sequence) -> None:
    """Overlay detected peak/valley markers for a list of BuildUpDecayCycle
    objects (see structs/cycles.py). `datetimes` should align by index with
    the co2_series the cycles were detected against."""
    for cycle in cycles:
        peak_t = datetimes[cycle.peak_idx]
        valley_t = datetimes[cycle.valley_idx]
        ax.scatter(peak_t, cycle.peak_value, color=PALETTE["peak"], s=18, zorder=5, marker="^")
        ax.scatter(valley_t, cycle.valley_value, color=PALETTE["valley"], s=18, zorder=5, marker="v")
        ax.axvspan(valley_t, peak_t, color=PALETTE["cycle_span"], zorder=1)


def mark_excluded(ax: Axes, indices: Iterable[int], datetimes: Sequence, co2: Sequence) -> None:
    """Overlay excluded/invalid peak or valley points in a muted color so they
    remain visible for debugging without competing with valid cycle markers."""
    for idx in indices:
        ax.scatter(datetimes[idx], co2[idx], color=PALETTE["excluded"], s=14, zorder=4, marker="x")


# ---------------------------------------------------------------------------
# Saving
# ---------------------------------------------------------------------------

def save_figure(fig: Figure, path: Path | str, close: bool = True) -> Path:
    """Save with project defaults (dpi/bbox come from rcParams) and optionally
    close the figure to avoid memory build-up across batch plot generation."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    if close:
        plt.close(fig)
    return path