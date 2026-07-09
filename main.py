from cli.parseargs import parse_args
from rich.console import Console
from apis.csvintake import read_monitor_output_from_csv
from apis.jsonintake import single_room_json
from classes.room_params import RoomParams
from classes.monitor_output import MonitorOutput
from classes.sitedata import SiteData
from approaches.kalman import apply_kalman_filter
from pathlib import Path

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
    site_data = SiteData(site_name=args.site_name or "Default Site", room_params=room_params[1], monitor_output=monitor_output)
    plotting_data = apply_kalman_filter(site_data, room_params[1])
    return 1


if __name__ == "__main__":
    raise SystemExit(main())