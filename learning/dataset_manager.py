import numpy as np
from typing import Tuple

class DatasetManager:
    """
    Prepares dataset X (features) and y (targets) from database trajectory logs.
    """
    def prepare_dataset(self, db_rows: list) -> Tuple[np.ndarray, np.ndarray]:
        if not db_rows or len(db_rows) < 5:
            return np.array([]), np.array([])

        X, y = [], []
        for i in range(len(db_rows) - 1):
            row = db_rows[i]
            next_row = db_rows[i + 1]
            
            # Features: [x, y, vx, vy, speed, direction, ax, ay]
            feat = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]]
            # Target: [next_x, next_y]
            target = [next_row[0], next_row[1]]
            
            X.append(feat)
            y.append(target)

        return np.array(X), np.array(y)
