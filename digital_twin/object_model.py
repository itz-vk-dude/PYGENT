from typing import List, Tuple

class ObjectModel:
    def __init__(self):
        self.position = [0.0, 0.0, 0.0]
        self.velocity = [0.0, 0.0, 0.0]
        self.predicted_trajectory: List[Tuple[float, float]] = []

    def update_state(self, pos: list, vel: list):
        self.position = pos
        self.velocity = vel

    def set_predicted_trajectory(self, trajectory: List[Tuple[float, float]]):
        self.predicted_trajectory = trajectory
