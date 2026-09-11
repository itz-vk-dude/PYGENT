import math
from typing import List, Dict, Any

class Simulator:
    def __init__(self, use_pybullet: bool = False):
        self.use_pybullet = use_pybullet
        if self.use_pybullet:
            try:
                import pybullet as p
                self.physics_client = p.connect(p.DIRECT)
            except Exception as e:
                print(f"[Simulator] PyBullet notice (using kinematic simulator): {e}")
                self.use_pybullet = False

    def simulate_action(self, action: Dict[str, Any], current_robot_pos: list, hybrid_pred_px: tuple) -> Dict[str, Any]:
        """
        Simulates candidate action. Calculates estimated movement time, travel distance, and predicted position error.
        """
        target_px = action.get("target_px", (0.0, 0.0))
        position_error = math.sqrt((target_px[0] - hybrid_pred_px[0])**2 + (target_px[1] - hybrid_pred_px[1])**2)

        robot_x, robot_y, robot_z = action["x"], action["y"], action["z"]
        dx = robot_x - current_robot_pos[0]
        dy = robot_y - current_robot_pos[1]
        dz = robot_z - current_robot_pos[2]
        travel_distance = math.sqrt(dx**2 + dy**2 + dz**2)

        execution_time = travel_distance / 200.0 if travel_distance > 0 else 0.1

        return {
            "action": action,
            "position_error": position_error,
            "execution_time": execution_time,
            "movement_cost": travel_distance
        }

    def simulate_all(self, candidate_actions: List[Dict[str, Any]], current_robot_pos: list, hybrid_pred_px: tuple) -> List[Dict[str, Any]]:
        results = []
        for act in candidate_actions:
            res = self.simulate_action(act, current_robot_pos, hybrid_pred_px)
            results.append(res)
        return results
