from digital_twin.world_model import WorldModel
from digital_twin.kinematics import RoboticArmKinematics
from typing import Dict, Any, List

class StateManager:
    def __init__(self):
        self.world = WorldModel()
        self.kinematics = RoboticArmKinematics()
        self.current_joints: List[float] = [90.0, 45.0, 45.0, 30.0, 10.0]
        self.person_present: bool = False
        self.objects: List[Any] = []
        self.current_task: str = "PERCEPTION & TRACKING"
        self.safety_status: str = "APPROVED"
        self.last_command: str = "IDLE"

    def sync_perception(self, perception_data: Dict[str, Any]):
        pos = [perception_data.get("x", 0.0), perception_data.get("y", 0.0), 0.0]
        vel = [perception_data.get("vx", 0.0), perception_data.get("vy", 0.0), 0.0]
        self.world.object.update_state(pos, vel)
        self.person_present = perception_data.get("person_present", False)
        self.objects = perception_data.get("objects", [])

    def sync_joints(self, joints_deg: List[float], gripper_state: str = "OPEN"):
        """
        Synchronizes actual 5-DOF joint telemetry from real hardware / controller to Digital Twin,
        and computes the real-time Cartesian end-effector position using Forward Kinematics (FK).
        """
        if len(joints_deg) >= 5:
            self.current_joints = list(joints_deg[:5])
            x, y, z = self.kinematics.forward_kinematics(*self.current_joints)
            self.world.robot.update_position([x, y, z])
            self.world.robot.update_gripper(gripper_state)

    def sync_robot(self, robot_pos: list, gripper_state: str = "OPEN"):
        self.world.robot.update_position(robot_pos)
        self.world.robot.update_gripper(gripper_state)
        # Compute IK to obtain joint angles for target pos
        j1, j2, j3, j4, j5 = self.kinematics.inverse_kinematics(robot_pos[0], robot_pos[1], robot_pos[2])
        self.current_joints = [j1, j2, j3, j4, j5]

    def set_task(self, task_name: str):
        self.current_task = task_name

    def set_last_command(self, cmd: str):
        self.last_command = cmd

    def get_state(self) -> Dict[str, Any]:
        full_state = self.world.get_full_state()
        full_state["robot"]["joints"] = self.current_joints
        
        # Centralized PHYGENT_STATE representation
        phygent_state = {
            "person_present": self.person_present,
            "objects": self.objects,
            "robot_status": "READY",
            "robot_position": full_state["robot"]["position"],
            "robot_joints": self.current_joints,
            "gripper_state": full_state["robot"]["gripper"],
            "current_task": self.current_task,
            "prediction": full_state["object"]["position"],
            "safety": self.safety_status,
            "last_command": self.last_command
        }

        full_state["phygent_state"] = phygent_state
        return full_state


