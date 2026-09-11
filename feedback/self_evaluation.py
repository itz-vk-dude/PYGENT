from typing import Dict, Any

class SelfEvaluator:
    def __init__(self, success_threshold_px: float = 25.0):
        self.success_threshold_px = success_threshold_px

    def evaluate(self, comparison_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates physical outcome against expectation.
        Returns SUCCESS, PARTIAL_SUCCESS, or FAILURE.
        """
        err = comparison_result.get("error_px", 999.0)
        if err <= self.success_threshold_px:
            status = "SUCCESS"
        elif err <= self.success_threshold_px * 2.0:
            status = "PARTIAL_SUCCESS"
        else:
            status = "FAILURE"

        return {
            "status": status,
            "position_error_px": err,
            "recommendation": "LOG_TO_DATASET"
        }
