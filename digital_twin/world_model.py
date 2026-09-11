from digital_twin.robot_model import RobotModel
from digital_twin.object_model import ObjectModel
from typing import Dict, Any

class WorldModel:
    def __init__(self):
        self.robot = RobotModel()
        self.object = ObjectModel()

    def get_full_state(self) -> Dict[str, Any]:
        return {
            "robot": {
                "joints": self.robot.joint_angles,
                "gripper": self.robot.gripper_state,
                "position": self.robot.current_position,
                "workspace": self.robot.workspace_bounds
            },
            "object": {
                "position": self.object.position,
                "velocity": self.object.velocity,
                "predicted_trajectory": self.object.predicted_trajectory
            }
        }
