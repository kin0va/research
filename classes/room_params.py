"""
Room Parameters Data Structure

This module defines the RoomParams class for storing and managing
room dimensional and occupancy information.
"""


class RoomParams:
    """
    Represents the physical parameters and occupancy constraints of a room.
    
    This class stores room dimensions (height, width, length), calculates
    volume if not explicitly provided, and tracks the maximum expected
    occupancy for the space.
    
    Attributes:
        height (float): Room height in meters
        width (float): Room width in meters
        length (float): Room length in meters
        volume (float | None): Room volume in cubic meters (calculated if not provided)
        max_occupancy (int): Maximum expected number of people in the room
    """
    
    def __init__(
        self,
        height: float,
        width: float,
        length: float,
        max_occupancy: int,
        volume: float | None = None,
        c_amb: float | None = None,
        cpp_per_person: float = 5e-6,
    ) -> None:
        """
        Initialize room parameters.
        
        Args:
            height: Room height in meters
            width: Room width in meters
            length: Room length in meters
            max_occupancy: Maximum expected number of people in the room
            volume: Optional room volume in cubic meters. If not provided,
                   it will be calculated from dimensions.
            c_amb: Optional ambient CO2 level in ppm. If not provided, defaults to 420.
            cpp_per_person: Optional CO2 production per person in m³/s. If not provided, defaults to 0.005.

        Raises:
            ValueError: If any dimension is non-positive or max_occupancy is non-positive
        """
        # Validate dimensions are positive
        if height <= 0 or width <= 0 or length <= 0:
            raise ValueError("All dimensions (height, width, length) must be positive")
        
        if max_occupancy <= 0:
            raise ValueError("max_occupancy must be positive")
        
        # Store dimensional parameters
        self.height: float = height
        self.width: float = width
        self.length: float = length
        
        # Store or calculate volume
        # If volume is provided, use it; otherwise calculate from dimensions
        if volume is not None:
            self.volume: float = volume
        else:
            self.volume = self._calculate_volume()
        
        # Store occupancy constraint
        self.max_occupancy: int = max_occupancy
        
        # Store CO2 parameters
        self.c_amb: float | None = c_amb
        self.cpp_per_person: float | None = cpp_per_person

    def _calculate_volume(self) -> float:
        """
        Calculate room volume from dimensional parameters.
        
        Formula: volume = height × width × length
        
        Returns:
            float: Room volume in cubic meters
        """
        return self.height * self.width * self.length
    
    def __repr__(self) -> str:
        """Return a detailed string representation of room parameters."""
        return (
            f"RoomParams(height={self.height}m, width={self.width}m, "
            f"length={self.length}m, volume={self.volume}m³, "
            f"max_occupancy={self.max_occupancy})"
        )
