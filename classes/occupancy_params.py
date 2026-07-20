from typing import  Optional
import pandas as pd


class OccupancyParameters:
    """
    Physical constants for the CO2 mass-balance model.

    VOLUME MUST BE PROVIDED. 
    
    All other parameters have defaults that are reasonable for a typical office space.

    Args:
        volume:      Volume of the office space (m³). Required.
        rho_air:     Density of air (kg/m³). Default 1.2 kg/m³ at ~20 °C.
        c_amb:       Ambient outdoor CO2 concentration (ppm). Default 420 ppm.
        c_adj:       CO2 concentration of adjacent rooms (ppm).
                     Defaults to c_amb (i.e. no net adjacent-room contribution).
        m_v_in:      Mass flow rate of air exchanged with adjacent rooms (kg/s).
                     Default 0.0 — ignored unless you have a measured value.
        cpp_per_person: CO2 generation rate per person (ppm·m³/s). FIND
    """
    def __init__(self, volume: float, rho_air: float = 1.2, c_amb: float = 420,
                 c_adj: Optional[float] = None, m_v_in: float = 0.0,
                 cpp_per_person: float = 5e-6,site_code: str = ""):
        self.volume          = volume
        self.rho_air         = rho_air
        self.c_amb           = c_amb
        self.c_adj           = c_adj if c_adj is not None else c_amb
        self.m_v_in          = m_v_in
        self.cpp_per_person  = cpp_per_person
        self.site_code       = site_code