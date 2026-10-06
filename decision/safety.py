from typing import Dict, Any, Tuple, List
import config
from robotics.kinematics import RoboticArmKinematics

class SafetyValidator:
    """
    Hard-Gate Safety Engine for PHYGENT.
    Evaluates candidate target AFTER voice/context adjustments.
    Order:
      Candidate Action -> Context/Voice Offset -> IK Solvability -> Final Target Validation -> Joint Limits Check -> Human Proximity Gate -> EXECUTE.
    """
    def __init__(self, workspace_bounds: dict = None):
        self.bounds = workspace_bounds or config.WORKSPACE_BOUNDS
        self.kinematics = RoboticArmKinematics()

    def validate_final_target(
        self,
        target_xyz: List[float],
        human_info: Dict[str, Any] = None,
        data_quality: Dict[str, Any] = None
    ) -> Tuple[bool, str]:
        """
        Hard gate safety check on final target XYZ and joints.
        """
        # 1. Data Quality Gate
        if data_quality and not data_quality.get("allow_action", True):
            return False, f"REJECTED: Data quality check failed ({data_quality.get('status')})"

        # 2. Human Proximity Gate
        if human_info and human_info.get("inside_workspace", False):
            return False, "REJECTED: Human inside robot workspace."

        # 3. Final Target Workspace Bounds Validation
        x, y, z = target_xyz[0], target_xyz[1], target_xyz[2]
        if not (self.bounds["x_min"] <= x <= self.bounds["x_max"]):
            return False, f"REJECTED: X coordinate {x:.1f} out of workspace bounds [{self.bounds['x_min']}, {self.bounds['x_max']}]"
        if not (self.bounds["y_min"] <= y <= self.bounds["y_max"]):
            return False, f"REJECTED: Y coordinate {y:.1f} out of workspace bounds [{self.bounds['y_min']}, {self.bounds['y_max']}]"
        if not (self.bounds["z_min"] <= z <= self.bounds["z_max"]):
            return False, f"REJECTED: Z coordinate {z:.1f} out of workspace bounds [{self.bounds['z_min']}, {self.bounds['z_max']}]"

        # 4. IK Solvability & Joint Limits Check
        j1, j2, j3, j4, j5 = self.kinematics.inverse_kinematics(x, y, z)
        joints = [j1, j2, j3, j4, j5]
        for idx, angle in enumerate(joints, 1):
            limit = config.JOINT_LIMITS.get(f"j{idx}", (0.0, 180.0))
            if not (limit[0] <= angle <= limit[1]):
                return False, f"REJECTED: Joint J{idx} angle {angle:.1f}° exceeds physical limit [{limit[0]}, {limit[1]}]"

        return True, "APPROVED_SAFE"
