import math
from typing import List, Dict, Any
from robotics.kinematics import RoboticArmKinematics

class CandidateActionGenerator:
    """
    Generates alternative candidate trajectories (e.g. Direct Intercept, Early Intercept, Hover Wait).
    """
    def __init__(self):
        self.kinematics = RoboticArmKinematics()

    def generate_actions(self, hybrid_pred: tuple, robot_pos: list) -> List[Dict[str, Any]]:
        target_x, target_y = hybrid_pred[0], hybrid_pred[1]
        rx, ry, rz = robot_pos[0], robot_pos[1], robot_pos[2]

        candidates = []

        # Candidate A: Direct Intercept
        cand_a_xyz = [target_x, target_y, 100.0]
        dist_a = math.sqrt((cand_a_xyz[0] - rx)**2 + (cand_a_xyz[1] - ry)**2 + (cand_a_xyz[2] - rz)**2)
        j1_a, j2_a, j3_a, j4_a, j5_a = self.kinematics.inverse_kinematics(*cand_a_xyz)
        candidates.append({
            "name": "DIRECT_INTERCEPT",
            "target_xyz": cand_a_xyz,
            "x": cand_a_xyz[0], "y": cand_a_xyz[1], "z": cand_a_xyz[2],
            "target_joints": [j1_a, j2_a, j3_a, j4_a, j5_a],
            "distance": dist_a,
            "estimated_time": dist_a / 150.0,
            "predicted_error": 5.0,
            "safety": "PENDING",
            "feasible": True
        })

        # Candidate B: Early Intercept (Shifted offset)
        cand_b_xyz = [target_x - 30.0, target_y + 20.0, 120.0]
        dist_b = math.sqrt((cand_b_xyz[0] - rx)**2 + (cand_b_xyz[1] - ry)**2 + (cand_b_xyz[2] - rz)**2)
        j1_b, j2_b, j3_b, j4_b, j5_b = self.kinematics.inverse_kinematics(*cand_b_xyz)
        candidates.append({
            "name": "EARLY_INTERCEPT",
            "target_xyz": cand_b_xyz,
            "x": cand_b_xyz[0], "y": cand_b_xyz[1], "z": cand_b_xyz[2],
            "target_joints": [j1_b, j2_b, j3_b, j4_b, j5_b],
            "distance": dist_b,
            "estimated_time": dist_b / 150.0,
            "predicted_error": 8.0,
            "safety": "PENDING",
            "feasible": True
        })

        # Candidate C: Hover Wait (Elevated position)
        cand_c_xyz = [target_x, target_y, 200.0]
        dist_c = math.sqrt((cand_c_xyz[0] - rx)**2 + (cand_c_xyz[1] - ry)**2 + (cand_c_xyz[2] - rz)**2)
        j1_c, j2_c, j3_c, j4_c, j5_c = self.kinematics.inverse_kinematics(*cand_c_xyz)
        candidates.append({
            "name": "HOVER_WAIT",
            "target_xyz": cand_c_xyz,
            "x": cand_c_xyz[0], "y": cand_c_xyz[1], "z": cand_c_xyz[2],
            "target_joints": [j1_c, j2_c, j3_c, j4_c, j5_c],
            "distance": dist_c,
            "estimated_time": dist_c / 150.0,
            "predicted_error": 12.0,
            "safety": "PENDING",
            "feasible": True
        })

        return candidates
