from typing import Dict, Any
import config

class WorkspaceManager:
    """
    Manages physical spatial workspace boundaries and clearance zones.
    """
    def __init__(self):
        self.bounds = config.WORKSPACE_BOUNDS

    def is_within_bounds(self, x: float, y: float, z: float) -> bool:
        return (
            self.bounds["x_min"] <= x <= self.bounds["x_max"] and
            self.bounds["y_min"] <= y <= self.bounds["y_max"] and
            self.bounds["z_min"] <= z <= self.bounds["z_max"]
        )
