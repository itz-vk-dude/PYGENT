from typing import List, Tuple

class TrajectorySimulator:
    """
    Interpolates trajectory points for candidate motions.
    """
    def generate_path(self, start_xyz: List[float], target_xyz: List[float], steps: int = 10) -> List[Tuple[float, float, float]]:
        path = []
        for i in range(steps + 1):
            alpha = i / float(steps)
            x = start_xyz[0] + alpha * (target_xyz[0] - start_xyz[0])
            y = start_xyz[1] + alpha * (target_xyz[1] - start_xyz[1])
            z = start_xyz[2] + alpha * (target_xyz[2] - start_xyz[2])
            path.append((round(x, 1), round(y, 1), round(z, 1)))
        return path
