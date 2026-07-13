from __future__ import annotations

from dataclasses import is_dataclass, asdict
from typing import Any

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from rich.table import Table


class RuntimeUpdater:
    """Displays runtime information and progress."""

    def __init__(self, console: Console | None = None):
        self.console = console or Console()

    # ----------------------------------------------------
    # Generic object display
    # ----------------------------------------------------

    def object_table(self, obj: Any, title: str | None = None) -> Panel:
        """Convert any object into a Rich table."""

        table = Table(show_header=True)
        table.add_column("Attribute", style="cyan", no_wrap=True)
        table.add_column("Value", style="white")

        if is_dataclass(obj):
            values = asdict(obj) #type: ignore

        elif hasattr(obj, "__dict__"):
            values = vars(obj)

        else:
            values = {
                name: getattr(obj, name)
                for name in dir(obj)
                if not name.startswith("_")
                and not callable(getattr(obj, name))
            }

        for key, value in values.items():
            table.add_row(key, repr(value))

        return Panel(
            table,
            title=title or obj.__class__.__name__, #type: ignore
            border_style="blue",
        )

    def print_object(self, obj: Any, title: str | None = None):
        self.console.print(self.object_table(obj, title))

    # ----------------------------------------------------
    # Live updating
    # ----------------------------------------------------

    def live_object(self, obj: Any, refresh_per_second: int = 4):
        """Returns a Rich Live context."""

        return Live(
            self.object_table(obj),
            console=self.console,
            refresh_per_second=refresh_per_second,
        )

    # ----------------------------------------------------
    # Progress bars
    # ----------------------------------------------------

    def create_progress(self) -> Progress:
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
        )
    
    def string_update(self, message: str):
        """Print a message to the console without disrupting the progress bar."""
        self.console.print(message, style=" yellow")
    
    def string_process_finish(self, message:str):
        self.console.print(message, style="bold green")