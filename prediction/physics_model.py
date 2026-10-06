from typing import Dict, Any, Tuple

class PhysicsPredictor:
    """
    Kinematic Constant-Acceleration Physics Trajectory Predictor.
    """
    def predict(self, features: Dict[str, Any], dt: float = 0.5) -> Tuple[float, float]:
        x = features.get("x", 0.0)
        y = features.get("y", 0.0)
        vx = features.get("vx", 0.0)
        vy = features.get("vy", 0.0)
        ax = features.get("ax", 0.0)
        ay = features.get("ay", 0.0)

        # Kinematic equation: s = ut + 0.5 * a * t^2
        pred_x = x + vx * dt + 0.5 * ax * (dt ** 2)
        pred_y = y + vy * dt + 0.5 * ay * (dt ** 2)

        return float(pred_x), float(pred_y)
