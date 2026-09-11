import numpy as np
from data.database import DatabaseManager
from typing import Tuple

class DatasetManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def prepare_training_matrices(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Loads recorded valid trajectories from SQLite and forms feature matrix X and target matrix y.
        X = [x, y, vx, vy, speed, direction, ax, ay]
        y = [future_x, future_y]
        """
        rows = self.db.get_all_training_data()
        if len(rows) < 5:
            return np.empty((0, 8)), np.empty((0, 2))

        data = np.array(rows)
        X = data[:-1]
        y = data[1:, :2]
        return X, y
