from typing import Dict, Any

class SelfEvaluator:
    """
    Evaluates physical action success status based on actual position error thresholds.
    SUCCESS: < 15 px / mm
    PARTIAL: 15 - 30 px / mm
    FAILURE: > 30 px / mm
    """
    def evaluate(self, comp_result: Dict[str, Any]) -> Dict[str, Any]:
        error = comp_result.get("error_px", 0.0)

        if error < 15.0:
            status = "SUCCESS"
            score = 1.0
        elif error < 30.0:
            status = "PARTIAL"
            score = 0.5
        else:
            status = "FAILURE"
            score = 0.0

        return {
            "status": status,
            "score": score,
            "error_px": error
        }
