from classes.sitedata import SiteData
from classes.monitor_output import MonitorOutput
from classes.room_params import RoomParams


class PlottingData:
    def __init__(self, site_data: SiteData, monitor_output: MonitorOutput,room_params: RoomParams):
        self.site_data = site_data
        self.monitor_output = monitor_output
        self.room_params = room_params