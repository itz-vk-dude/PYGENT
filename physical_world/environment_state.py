import time
from typing import Dict, Any

class EnvironmentState:
    """
    Physical environment workspace state model.
    """
    def __init__(self):
        self.light_level = "NORMAL"
        self.workspace_occupied = False
        self.last_updated = time.time()

    def update(self, occupied: bool, light: str = "NORMAL"):
        self.workspace_occupied = occupied
        self.light_level = light
        self.last_updated = time.time()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "light_level": self.light_level,
            "workspace_occupied": self.workspace_occupied,
            "last_updated": self.last_updated
        }
