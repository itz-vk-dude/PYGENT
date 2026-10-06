from typing import List, Tuple

class MotionPlanner:
    """
    Interpolates joint trajectories for smooth physical servo motion.
    """
    def plan_joint_path(self, start_joints: List[float], target_joints: List[float], steps: int = 5) -> List[List[float]]:
        path = []
        for i in range(1, steps + 1):
            alpha = i / float(steps)
            step_j = [
                round(start_joints[j] + alpha * (target_joints[j] - start_joints[j]), 1)
                for j in range(min(len(start_joints), len(target_joints)))
            ]
            path.append(step_j)
        return path
