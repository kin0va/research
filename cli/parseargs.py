import argparse
from pathlib import Path
from rich.console import Console

from cli.termuserguide import TermUserGuide
    


def print_guide(console: Console) -> None:
    """Print a Rich-based user guide for the main script."""
    guide = TermUserGuide(console=console)
    guide.print_guide()

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="Load room metadata and CO₂ monitor output into a SiteData object.",
        add_help=True,
    )
    parser.add_argument(
        "--room-json",
        type=Path,
        default=None,
        help="Path to the room metadata JSON file (default: data/json/room.json)",
    )
    parser.add_argument(
        "--monitor-csv",
        type=Path,
        default=None,
        help="Path to the CO₂ monitor CSV file (default: first CSV in data/csv/)",
    )
    parser.add_argument(
        "--guide",
        action="store_true",
        help="Print the user guide and exit",
    )
    parser.add_argument(
        "--plots-dir",
        type=Path,
        default=Path("output/plots"),
        help="Directory to save generated plots (default: output/plots)",
    )
    return parser.parse_args()