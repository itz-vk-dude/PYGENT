from decision.scoring import ActionScorer
from decision.safety import SafetyValidator
from typing import List, Dict, Any, Tuple

class DecisionEngine:
    def __init__(self):
        self.scorer = ActionScorer()
        self.safety = SafetyValidator()

    def select_best_action(self, sim_results: List[Dict[str, Any]]) -> Tuple[Dict[str, Any], float, str]:
        """
        Evaluates simulated candidate actions, applies safety validation, and selects lowest scoring approved action.
        Returns (best_action, score, safety_status).
        """
        best_act = None
        best_score = float("inf")
        best_safety_reason = "NO_VALID_ACTION"

        for res in sim_results:
            act = res["action"]
            is_safe, reason = self.safety.validate(act)
            if is_safe:
                score = self.scorer.calculate_score(res)
                if score < best_score:
                    best_score = score
                    best_act = act
                    best_safety_reason = reason

        if best_act is None and len(sim_results) > 0:
            best_act = sim_results[0]["action"]
            best_score = 999.9
            best_safety_reason = "REJECTED_SAFETY_FALLBACK"

        return best_act, best_score, best_safety_reason
