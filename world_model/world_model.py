from typing import Dict, Any, List
from world_model.robot_model import RobotModel
from world_model.object_model import ObjectModel

class WorldModel:
    """
    Combined Digital Twin World Model.
    """
    def __init__(self):
        self.robot = RobotModel()
        self.object = ObjectModel()
        self.workspace_bounds = {
            "x_min": -350.0, "x_max": 350.0,
            "y_min": 0.0,    "y_max": 450.0,
            "z_min": 0.0,    "z_max": 350.0
        }

    def get_full_state(self) -> Dict[str, Any]:
        return {
            "robot": self.robot.to_dict(),
            "object": self.object.to_dict(),
            "workspace": self.workspace_bounds
        }
