import numpy as np
from sklearn.ensemble import IsolationForest
from typing import Dict, Any

class DataQualityChecker:
    def __init__(self, contamination: float = 0.05):
        self.model = IsolationForest(contamination=contamination, random_state=42)
        self.is_fitted = False

    def validate_range(self, data: Dict[str, Any], max_w: float = 1920.0, max_h: float = 1080.0, max_speed: float = 5000.0) -> bool:
        """
        Validates spatial coordinates and physical dynamic bounds.
        """
        x, y = data.get("x", 0.0), data.get("y", 0.0)
        speed = data.get("speed", 0.0)

        if not (0.0 <= x <= max_w and 0.0 <= y <= max_h):
            return False
        if abs(speed) > max_speed:
            return False
        return True

    def check_quality(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates data quality. Returns status 'NORMAL' or 'ANOMALY'.
        """
        if not self.validate_range(data):
            return {"status": "ANOMALY", "reason": "out_of_bounds", "confidence": 0.0}

        if self.is_fitted:
            features = np.array([[
                data.get("x", 0.0), data.get("y", 0.0),
                data.get("vx", 0.0), data.get("vy", 0.0),
                data.get("speed", 0.0), data.get("direction", 0.0)
            ]])
            pred = self.model.predict(features)
            if pred[0] == -1:
                return {"status": "ANOMALY", "reason": "isolation_forest_outlier", "confidence": 0.3}

        return {"status": "NORMAL", "reason": "valid", "confidence": 0.95}

    def fit_baseline(self, dataset: np.ndarray):
        """Fits Isolation Forest baseline model on historical normal dataset."""
        if len(dataset) >= 10:
            self.model.fit(dataset)
            self.is_fitted = True
