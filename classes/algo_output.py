import typing as t
from sitedata import SiteData
from cycles import BuildUpDecayCycle


class PlottingData:
    def __init__(self, site_data: SiteData, occupancy_series: t.List[float]):
        self.site_data: SiteData = site_data
        self.cycles: t.List[BuildUpDecayCycle] = site_data.cycles
        self.occupancy_series: t.List[float] = occupancy_series

    def get_cycle_data(self) -> t.List[dict]:
        """Return a list of dictionaries containing cycle data for plotting."""
        cycle_data = []
        for cycle in self.cycles:
            cycle_info = {
                "peak_idx": cycle.peak_idx,
                "valley_idx": cycle.valley_idx,
                "peak_value": cycle.peak_value,
                "valley_value": cycle.valley_value,
                "duration": cycle.duration,
            }
            cycle_data.append(cycle_info)
        return cycle_data