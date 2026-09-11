import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from typing import Tuple, Dict, Any

class MLPredictor:
    def __init__(self, model_path: str = r"C:\PYGENT\prediction\model.pkl"):
        self.model_path = model_path
        self.model = RandomForestRegressor(n_estimators=50, random_state=42)
        self.is_trained = False
        self.load_model()

    def train(self, X: np.ndarray, y: np.ndarray):
        """Trains the Random Forest model on feature matrix X and target matrix y."""
        if len(X) > 0 and len(y) > 0:
            self.model.fit(X, y)
            self.is_trained = True
            self.save_model()

    def predict(self, features: Dict[str, Any], dt: float = 0.5) -> Tuple[float, float]:
        """
        Predicts future (x, y) coordinates after dt seconds.
        Uses velocity fallback if model has not been trained yet.
        """
        x = features.get("x", 0.0)
        y = features.get("y", 0.0)
        vx = features.get("vx", 0.0)
        vy = features.get("vy", 0.0)

        if not self.is_trained:
            return float(x + vx * dt), float(y + vy * dt)

        feat_vector = np.array([[
            x, y, vx, vy,
            features.get("speed", 0.0),
            features.get("direction", 0.0),
            features.get("ax", 0.0),
            features.get("ay", 0.0)
        ]])

        pred = self.model.predict(feat_vector)
        return float(pred[0][0]), float(pred[0][1])

    def save_model(self):
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)

    def load_model(self):
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
                self.is_trained = True
            except Exception as e:
                print(f"[MLPredictor] Warning: Could not load model: {e}")
