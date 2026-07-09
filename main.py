
import importlib

from rich.console import Console


def main() -> int:
    console = Console()
    cli_parser = importlib.import_module("cli.parse-args")
    args = cli_parser.parse_args()

    # Print guide if requested
    if args.guide:
        cli_parser.print_guide(console)
        return 0

    console.print("[bold red]Error:[/bold red] No functionality implemented yet.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())