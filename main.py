#cli functionality
from cli.parseargs import parse_args
from cli.updater import RuntimeUpdater
from rich.console import Console
from cli.cli_output import cli_output
#apis
from apis.csvintake import read_monitor_output_from_csv
from apis.jsonintake import single_room_json
#data structs
from classes.room_params import RoomParams
from classes.monitor_output import MonitorOutput
from classes.sitedata import SiteData
from classes.plotting_data import PlottingData
#approaches
from approaches.kalman import apply_kalman_filter
#output
from out.daily import plot_daily


from pathlib import Path


def run_kalman_filter(site_data: SiteData, room_params: RoomParams,updater: RuntimeUpdater,plotting_period: str = "D") -> PlottingData:
    """
    Run the Kalman filter approach on the provided SiteData and RoomParams.
    For now only does daily plots and split by day happens in the SiteData class before plotting.

    Args:
        site_data: SiteData object containing the CO2 data and room parameters.
        room_params: RoomParams object containing the room parameters.
        updater: RuntimeUpdater object for displaying runtime information.
        plotting_period: The period for plotting (default is "D" for daily).
    Returns:
        PlottingData object containing the filtered occupancy and ACH data.
    """
    updater.string_update(f"Running Kalman filter for site: {site_data.site_name}")
    plotting_data = apply_kalman_filter(site_data, room_params,updater)
    plotting_data.site_data._days_data = plotting_data.site_data._split_by(plotting_period)  # Ensure days_data is populated

    total_days = len(plotting_data.site_data.days_data)

    with updater.create_progress() as progress:
        task = progress.add_task("[cyan]Generating daily plots...", total=total_days)

        for day_label in plotting_data.site_data.days_data.keys():
            progress.update(
                task,
        )

            plot_daily(
                plotting_data,
                day_label,
                title=f"CO2 Trace for {day_label}",
                savepath=f"results/daily/{day_label}.png"
            )

            progress.advance(task)

    updater.string_process_finish("Finished generating daily plots.")
    return plotting_data


def main() -> int:
    console = Console()
    args = parse_args()

    if args.guide:
        from cli.parseargs import print_guide

        print_guide(console)
        return 0
    
    # Enter main flow of program
    # Create a RuntimeUpdater instance for displaying progress and runtime information
    updater = RuntimeUpdater(console)

    # Load data from files 
    updater.string_update("Loading files...")
    room_json = args.room_json or Path("data/json/room.json")
    monitor_csv = args.monitor_csv or Path("data/csv/monitor.csv")
    room_params = single_room_json(room_json) #currently only one room supported while setting up
    monitor_output = read_monitor_output_from_csv(monitor_csv)

    # Update the console with the loaded data information
    updater.string_process_finish(f"Loaded room parameters from {room_json} and monitor output from {monitor_csv}")
    updater.string_update("Creating SiteData object...")
    # Create SiteData object, will need refactoring to support multiple rooms in the future
    site_data = SiteData(site_name=room_params[0]or "Default Site", room_params=room_params[1], monitor_output=monitor_output)
    updater.string_process_finish("SiteData Object Created")
    #this section dictates what approach is being used, for now just kalman but will be expanded using cmd args to select approach
    data = run_kalman_filter(site_data, room_params[1], updater)
    updater.string_process_finish("Kalman filter processing complete. Plots saved in results/ directory.")
    cli_output(data,updater)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())