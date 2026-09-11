import math
from typing import Dict, Any

class FeedbackComparator:
    def compare(self, hybrid_pred: tuple, actual_pos: tuple) -> Dict[str, Any]:
        """
        Calculates position error = sqrt((pred_x - actual_x)^2 + (pred_y - actual_y)^2)
        """
        pred_x, pred_y = hybrid_pred
        act_x, act_y = actual_pos
        error = math.sqrt((pred_x - act_x)**2 + (pred_y - act_y)**2)
        return {
            "predicted": hybrid_pred,
            "actual": actual_pos,
            "error_px": error
        }
