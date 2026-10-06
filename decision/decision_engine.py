from typing import List, Dict, Any, Tuple
from decision.scoring import ActionScorer
from decision.safety import SafetyValidator

class DecisionEngine:
    """
    Decision Engine.
    Evaluates simulated candidate actions, applies hard-gate safety validation, and selects the best safe action.
    STRICT RULE: If all candidates are rejected by safety, returns best_act = None. NO UNSAFE FALLBACK IS EVER EXECUTED.
    """
    def __init__(self):
        self.scorer = ActionScorer()
        self.safety = SafetyValidator()

    def select_best_action(
        self,
        sim_results: List[Dict[str, Any]],
        voice_offset: List[float] = None,
        human_info: Dict[str, Any] = None,
        data_quality: Dict[str, Any] = None
    ) -> Tuple[Dict[str, Any], float, str]:
        if voice_offset is None:
            voice_offset = [0.0, 0.0, 0.0]

        best_act = None
        best_score = float("inf")
        best_safety_reason = "NO_CANDIDATE_SUBMITTED"

        for res in sim_results:
            act = dict(res["action"])
            base_xyz = act.get("target_xyz", [act.get("x",0), act.get("y",0), act.get("z",0)])
            
            # Apply voice/context adjustment BEFORE safety validation sequence
            final_xyz = [
                base_xyz[0] + voice_offset[0],
                base_xyz[1] + voice_offset[1],
                base_xyz[2] + voice_offset[2]
            ]
            act["target_xyz"] = final_xyz
            act["x"], act["y"], act["z"] = final_xyz[0], final_xyz[1], final_xyz[2]

            # Sequence: Target -> Voice Offset -> IK -> Final Target & Joint & Human Proximity Safety Check
            is_safe, reason = self.safety.validate_final_target(final_xyz, human_info, data_quality)
            if is_safe:
                score = self.scorer.calculate_score(res)
                if score < best_score:
                    best_score = score
                    best_act = act
                    best_safety_reason = reason
            else:
                best_safety_reason = reason

        # STRICT SAFETY RULE: NO FALLBACK TO UNSAFE CANDIDATE
        if best_act is None:
            return None, 999.9, f"NO_SAFE_ACTION: {best_safety_reason}"

        return best_act, best_score, best_safety_reason
