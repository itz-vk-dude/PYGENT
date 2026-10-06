import numpy as np
from typing import Dict, Any, Tuple

class DataPreprocessor:
    """
    Normalizes feature vectors for ML models.
    """
    def extract_features(self, state: Dict[str, Any]) -> np.ndarray:
        x = float(state.get("x", 0.0))
        y = float(state.get("y", 0.0))
        vx = float(state.get("vx", 0.0))
        vy = float(state.get("vy", 0.0))
        speed = float(state.get("speed", 0.0))
        direction = float(state.get("direction", 0.0))
        ax = float(state.get("ax", 0.0))
        ay = float(state.get("ay", 0.0))

        return np.array([[x, y, vx, vy, speed, direction, ax, ay]])
