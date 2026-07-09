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
                "[bold cyan]IAQ Occupancy Inference[/bold cyan]\n"
                "[italic]Terminal guide for loading room metadata and CO₂ monitor data.[/italic]",
                border_style="cyan",
                box=ROUNDED,
            )
        )
        self.console.print()

        self._print_section(
            "Overview",
            "This package combines room metadata and CO₂ sensor logs to build occupancy-related site models.",
        )

        self._print_section(
            "How it works",
            "The workflow loads room parameters, ingests monitor output, and prepares the data for analysis modules such as occupancy estimation, filtering, and plotting.",
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
            "calculations/\nfilters/\nfunctions/\ngraphing/\nstructs/\ndata/\ndocs/\nmain.py\nrequirements.txt",
        )

        self._print_section(
            "Example usage",
            "python main.py\npython main.py --room-json data/json/room.json --monitor-csv data/csv/example.csv",
        )

        self._print_section(
            "Scientific breakdown",
            "[dim]TODO: Add your modelling assumptions, ventilation equations, tracer decay discussion, and any scientific rationale here.[/dim]",
        )

        self._print_section(
            "Accuracy and validation",
            "[dim]TODO: Add precision, calibration notes, validation metrics, uncertainty estimates, and known limitations here.[/dim]",
        )

    def _print_section(self, title: str, body: str) -> None:
        self.console.print(Panel(Text(body, style="white"), title=f"[bold]{title}[/bold]", border_style="blue", box=ROUNDED))


if __name__ == "__main__":
    TermUserGuide().print_guide()
