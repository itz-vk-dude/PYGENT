import math
from typing import Dict, Any, Tuple

class PredictorEvaluator:
    """
    Evaluates ML-only, Physics-only, and Hybrid prediction accuracy separately
    against ground truth observations for research paper benchmarking.
    """
    def evaluate(self, ml_pred: Tuple[float, float], phys_pred: Tuple[float, float], hybrid_pred: Tuple[float, float], actual_pos: Tuple[float, float]) -> Dict[str, float]:
        ml_err = math.sqrt((ml_pred[0] - actual_pos[0])**2 + (ml_pred[1] - actual_pos[1])**2)
        phys_err = math.sqrt((phys_pred[0] - actual_pos[0])**2 + (phys_pred[1] - actual_pos[1])**2)
        hybrid_err = math.sqrt((hybrid_pred[0] - actual_pos[0])**2 + (hybrid_pred[1] - actual_pos[1])**2)

        return {
            "ml_error_px": round(ml_err, 2),
            "physics_error_px": round(phys_err, 2),
            "hybrid_error_px": round(hybrid_err, 2),
            "hybrid_improvement_pct": round(max(0.0, (min(ml_err, phys_err) - hybrid_err) / (min(ml_err, phys_err) + 1e-5) * 100), 1)
        }
