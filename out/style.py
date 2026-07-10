"""
graphing/style.py
==================
Single source of truth for how every plot in this project looks.

Nothing in here plots data. It only defines:
  - the color palette (including CO2-specific semantic colors)
  - figure sizing / dpi defaults
  - the matplotlib rcParams applied globally via `apply_style()`

Every other graphing module should import PALETTE / CO2_BANDS / constants
from here instead of hard-coding hex values or font sizes.
"""

from __future__ import annotations

import matplotlib as mpl
from cycler import cycler

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
# Keep this small and named by *meaning*, not by hue, so plot code reads as
# `PALETTE["co2_line"]` rather than `"#2b6cb0"`. Makes re-theming a one-file change.

PALETTE = {
    "background":    "#FAFAF8",
    "panel":         "#FFFFFF",
    "grid":          "#E4E2DD",
    "text":          "#2A2A28",
    "text_muted":    "#6B6963",

    "co2_line":      "#3C6E71",   # primary CO2 series
    "peak":          "#C1543C",   # detected peaks
    "valley":        "#3C7A5A",   # detected valleys
    "cycle_span":    "#3C6E7122", # translucent fill under a build-up/decay cycle
    "excluded":      "#B5B2AA",   # excluded/invalid peaks-valleys

    "occupied":      "#E8B23D33", # translucent occupancy-episode shading
    "unoccupied":    "#00000000", # transparent — no shading

    "temp_line":     "#8E5572",
    "humidity_line": "#4C7A9E",

    "accent":        "#C1543C",
    "categorical": [  # for multi-series plots (box plots across sites, etc.)
        "#3C6E71", "#C1543C", "#E8B23D", "#4C7A9E", "#8E5572", "#6B8E23",
    ],
}

# Semantic CO2 concentration bands (ppm), used for background shading so a
# reader can see "elevated" / "poor" air quality at a glance without a legend.
# Roughly aligned with ASHRAE/REHVA guidance; tune the thresholds, not the code.
CO2_BANDS = [
    # (lower_ppm, upper_ppm, color, label)
    (0,    800,  "#3C6E7114", "Good"),
    (800,  1000, "#E8B23D22", "Moderate"),
    (1000, 5000, "#C1543C22", "Poor"),
]

# Convenience constants for other modules
# Typical ambient/background CO2 level shown on plots (approximate)
CO2_BACKGROUND_PPM = 420
# Semantic color shortcut for CO2 series
COLOR_CO2 = PALETTE["co2_line"]

# ---------------------------------------------------------------------------
# Figure sizing
# ---------------------------------------------------------------------------
FIG_WIDTH_IN = 10.0
FIG_HEIGHT_IN = 5.0
DPI = 150

FONT_FAMILY = "DejaVu Sans"  # ships with matplotlib, no install dependency
FONT_SIZE_BASE = 11
FONT_SIZE_TITLE = 14
FONT_SIZE_LABEL = 11
FONT_SIZE_TICK = 9.5


def apply_style() -> None:
    """Apply project-wide matplotlib rcParams. Call once, near the top of main.py
    or at import time of graphing/__init__.py — every subsequent figure inherits it.
    """
    mpl.rcParams.update({
        "figure.facecolor": PALETTE["background"],
        "figure.figsize": (FIG_WIDTH_IN, FIG_HEIGHT_IN),
        "figure.dpi": DPI,
        "savefig.dpi": DPI,
        "savefig.facecolor": PALETTE["background"],
        "savefig.bbox": "tight",

        "axes.facecolor": PALETTE["panel"],
        "axes.edgecolor": PALETTE["grid"],
        "axes.labelcolor": PALETTE["text"],
        "axes.titlecolor": PALETTE["text"],
        "axes.grid": True,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.prop_cycle": cycler(color=PALETTE["categorical"]),
        "axes.titlesize": FONT_SIZE_TITLE,
        "axes.titleweight": "bold",
        "axes.labelsize": FONT_SIZE_LABEL,

        "grid.color": PALETTE["grid"],
        "grid.linewidth": 0.7,
        "grid.alpha": 0.8,

        "xtick.color": PALETTE["text_muted"],
        "ytick.color": PALETTE["text_muted"],
        "xtick.labelsize": FONT_SIZE_TICK,
        "ytick.labelsize": FONT_SIZE_TICK,

        "font.family": FONT_FAMILY,
        "font.size": FONT_SIZE_BASE,
        "text.color": PALETTE["text"],

        "legend.frameon": False,
        "legend.fontsize": FONT_SIZE_TICK,
    })