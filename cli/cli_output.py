from classes.plotting_data import PlottingData
from cli.updater import RuntimeUpdater

import numpy as np

from rich.panel import Panel
from rich.table import Table


def cli_output(data: PlottingData, updater: RuntimeUpdater):
    """
    Display summary statistics from a completed PlottingData run.
    """

    title = data.site_data.site_name

    num_co2_readings = len(data.site_data.monitor_output.co2_series)
    num_occ_periods = len(data.site_data.occupied_periods)

    average_co2 = np.median(
        data.site_data.monitor_output.co2_series
    )

    average_occ = np.mean(data.occupancy_series)

    average_ACH = np.mean(data.ACH_series)  # type: ignore

    table = Table(
        show_header=False,
        expand=True,
        padding=(0, 1),
    )

    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="white", justify="right")

    table.add_row(
        "CO2 readings",
        f"{num_co2_readings:,}",
    )

    table.add_row(
        "Occupancy periods",
        f"{num_occ_periods:,}",
    )

    table.add_row(
        "Median CO2",
        f"{average_co2:.0f} ppm",
    )

    table.add_row(
        "Average occupancy",
        f"{average_occ:.2f} people",
    )

    table.add_row(
        "Average ACH",
        f"{average_ACH:.2f} /hr",
    )

    panel = Panel(
        table,
        title=f"[bold cyan]{title}[/bold cyan]",
        border_style="blue",
    )

    updater.console.print(panel)