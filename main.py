from classes.plotting_data import PlottingData
from cli.parseargs import parse_args
from rich.console import Console
from apis.csvintake import read_monitor_output_from_csv
from apis.jsonintake import single_room_json
from classes.room_params import RoomParams
from classes.monitor_output import MonitorOutput
from classes.sitedata import SiteData
from approaches.kalman import apply_kalman_filter
from out.daily import plot_daily
from pathlib import Path


def run_kalman_filter(site_data: SiteData, room_params: RoomParams) -> PlottingData:
    """
    Run the Kalman filter approach on the provided SiteData and RoomParams.
    For now only does daily plots and split by day happens in the SiteData class before plotting.

    Args:
        site_data: SiteData object containing the CO2 data and room parameters.
        room_params: RoomParams object containing the room parameters.
    Returns:
        PlottingData object containing the filtered occupancy and ACH data.
    """
    
    plotting_data = apply_kalman_filter(site_data, room_params)
    return plotting_data


def main() -> int:
    console = Console()
    args = parse_args()

    if args.guide:
        from cli.parseargs import print_guide

        print_guide(console)
        return 0
    # Run the main program
    # Implementingthe kalman filter approach to estimate occupancy and ACH
    room_json = args.room_json or Path("data/json/room.json")
    monitor_csv = args.monitor_csv or Path("data/csv/monitor.csv")
    room_params = single_room_json(room_json) #currently only one room supported while setting up
    monitor_output = read_monitor_output_from_csv(monitor_csv)
    site_data = SiteData(site_name=room_params[0]or "Default Site", room_params=room_params[1], monitor_output=monitor_output)
    plotting_data = run_kalman_filter(site_data, room_params[1])
    plotting_data.site_data._days_data = plotting_data.site_data._split_by("D")  # Ensure days_data is populated
    for day_label in plotting_data.site_data.days_data.keys():
        plot_daily(plotting_data, day_label, title=f"CO2 Trace for {day_label}", savepath="results/{day_label}.png")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())