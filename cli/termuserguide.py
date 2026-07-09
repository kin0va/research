from __future__ import annotations

from rich.box import ROUNDED
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


class TermUserGuide:
    """Rich-based console guide for the IAQ occupancy inference package."""

    def __init__(self, console: Console | None = None) -> None:
        self.console = console or Console()

    def print_guide(self) -> None:
        """Print a structured terminal guide with placeholders for future details."""
        self.console.print()
        self.console.print(
            Panel.fit(
                "[bold cyan]CO₂ Occupancy Estimation[/bold cyan]\n"
                "[italic]Terminal guide for loading room metadata and CO₂ monitor data for occupancy modelling.[/italic]",
                border_style="cyan",
                box=ROUNDED,
            )
        )
        self.console.print()

        self._print_section(
            "Overview",
            "This project estimates room occupancy from time-series CO₂ measurements by comparing multiple modelling approaches, including decay analysis, build-up analysis, Kalman filtering, and machine learning.",
        )

        self._print_section(
            "How it works",
            "The workflow loads room metadata, ingests CO₂ monitor data, and prepares shared site models for analysis modules that estimate occupancy and generate reports or plots.",
        )

        self.console.print(Panel.fit("[bold]Quick start[/bold]", border_style="magenta"))
        commands = Table(show_header=True, header_style="bold magenta")
        commands.add_column("Command", style="cyan")
        commands.add_column("Purpose")
        commands.add_row("python main.py", "Run the package with default room and monitor files")
        commands.add_row("python main.py --room-json path/to/room.json", "Use a custom room metadata file")
        commands.add_row("python main.py --monitor-csv path/to/monitor.csv", "Use a custom CO₂ monitor export")
        self.console.print(commands)
        self.console.print()

        self._print_section(
            "Dependencies",
            "numpy\nmatplotlib\npandas\nscipy\nscikit-learn\nrich",
        )

        self._print_section(
            "Project structure",
            "1-decay-approach/\n2-build-up-approach/\n3-kalman-approach/\n4-ml-approach/\ncalculations/\nclasses/\napis/\ndata/\ndocs/\nprogress-reports/\nresults/\nmain.py\nrequirements.txt",
        )

        self._print_section(
            "Example usage",
            "python main.py\npython main.py --room-json data/json/room.json --monitor-csv data/csv/example.csv",
        )

        self._print_section(
            "Scientific breakdown",
            "CO₂ is used as a proxy for occupancy because human metabolism increases indoor concentration while ventilation and air exchange reduce it. The package compares ventilation-driven decay estimates, accumulation-based build-up estimates, recursive state-space filtering, and learned occupancy patterns from historical data.",
        )

        self._print_section(
            "Accuracy and validation",
            "Validation is based on comparing the outputs of each approach on the same room and sensor data, while checking consistency across room configurations and monitoring conditions. Sensor placement, ventilation variability, and measurement noise can all affect the precision of the estimates.",
        )

    def _print_section(self, title: str, body: str) -> None:
        self.console.print(Panel(Text(body, style="white"), title=f"[bold]{title}[/bold]", border_style="blue", box=ROUNDED))


if __name__ == "__main__":
    TermUserGuide().print_guide()
