from typing import List, Dict, Any
import config

class RobotModel:
    """
    5-DOF Robotic Arm Digital Twin Kinematic Model.
    """
    def __init__(self):
        self.l1 = config.LINK_L1_BASE_HEIGHT
        self.l2 = config.LINK_L2_UPPER_ARM
        self.l3 = config.LINK_L3_FOREARM
        self.l4 = config.LINK_L4_WRIST_EE
        
        self.commanded_joints: List[float] = [90.0, 45.0, 45.0, 30.0, 90.0]
        self.measured_joints: List[float] = [90.0, 45.0, 45.0, 30.0, 90.0]
        self.position: List[float] = [135.0, 0.0, 150.0]
        self.gripper: str = "OPEN"
        self.status: str = "READY"

    def update_measured_joints(self, joints: List[float]):
        if len(joints) >= 5:
            self.measured_joints = list(joints[:5])

    def update_commanded_joints(self, joints: List[float]):
        if len(joints) >= 5:
            self.commanded_joints = list(joints[:5])

    def update_position(self, pos: List[float]):
        if len(pos) >= 3:
            self.position = [float(pos[0]), float(pos[1]), float(pos[2])]

    def update_gripper(self, state: str):
        self.gripper = state

    def to_dict(self) -> Dict[str, Any]:
        return {
            "link_lengths": [self.l1, self.l2, self.l3, self.l4],
            "joints_commanded": list(self.commanded_joints),
            "joints_measured": list(self.measured_joints),
            "position": list(self.position),
            "gripper": self.gripper,
            "status": self.status
        }
