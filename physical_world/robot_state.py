from typing import List, Dict, Any

class RobotState:
    """
    Physical robotic arm state representation.
    Tracks commanded vs measured state independently.
    """
    def __init__(self):
        self.commanded_joints: List[float] = [90.0, 45.0, 45.0, 30.0, 90.0]
        self.measured_joints: List[float] = [90.0, 45.0, 45.0, 30.0, 90.0]
        self.commanded_position: List[float] = [135.0, 0.0, 150.0]
        self.measured_position: List[float] = [135.0, 0.0, 150.0]
        self.gripper_state: str = "OPEN"
        self.status: str = "READY"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "joints_commanded": list(self.commanded_joints),
            "joints_measured": list(self.measured_joints),
            "position_commanded": list(self.commanded_position),
            "position_measured": list(self.measured_position),
            "position": list(self.measured_position),
            "gripper": self.gripper_state,
            "status": self.status
        }
