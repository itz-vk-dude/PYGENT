from typing import Tuple, Dict, Any

class PhysicsPredictor:
    def __init__(self, g: float = 9.81):
        self.g = g

    def predict(self, features: Dict[str, Any], dt: float = 0.5) -> Tuple[float, float]:
        """
        Calculates future (x, y) coordinates using classical kinematics equations:
        x(t) = x0 + vx*t + 0.5*ax*t^2
        y(t) = y0 + vy*t + 0.5*ay*t^2
        """
        x = features.get("x", 0.0)
        y = features.get("y", 0.0)
        vx = features.get("vx", 0.0)
        vy = features.get("vy", 0.0)
        ax = features.get("ax", 0.0)
        ay = features.get("ay", 0.0)

        future_x = x + vx * dt + 0.5 * ax * (dt ** 2)
        future_y = y + vy * dt + 0.5 * ay * (dt ** 2)

        return float(future_x), float(future_y)
