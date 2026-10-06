import math
from typing import Tuple, Dict, Any

class FeedbackComparator:
    """
    Compares predicted target (hybrid_pred) against verified real outcome.
    Calculates Euclidean error in pixels/mm.
    """
    def compare(self, predicted_pos: Tuple[float, float], actual_pos: Tuple[float, float]) -> Dict[str, Any]:
        error = math.sqrt((predicted_pos[0] - actual_pos[0])**2 + (predicted_pos[1] - actual_pos[1])**2)
        return {
            "predicted_pos": predicted_pos,
            "actual_pos": actual_pos,
            "error_px": round(error, 2)
        }
