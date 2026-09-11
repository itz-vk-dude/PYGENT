from prediction.ml_model import MLPredictor
from prediction.physics_model import PhysicsPredictor
from typing import Dict, Any, Tuple

class HybridPredictor:
    def __init__(self, ml_weight: float = 0.5, physics_weight: float = 0.5):
        self.ml_predictor = MLPredictor()
        self.physics_predictor = PhysicsPredictor()
        self.ml_weight = ml_weight
        self.physics_weight = physics_weight

    def predict(self, state: Dict[str, Any], dt: float = 0.5) -> Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]]:
        """
        Returns (ml_pred, physics_pred, hybrid_pred)
        """
        ml_pred = self.ml_predictor.predict(state, dt)
        phys_pred = self.physics_predictor.predict(state, dt)

        hybrid_x = self.ml_weight * ml_pred[0] + self.physics_weight * phys_pred[0]
        hybrid_y = self.ml_weight * ml_pred[1] + self.physics_weight * phys_pred[1]

        return ml_pred, phys_pred, (float(hybrid_x), float(hybrid_y))
