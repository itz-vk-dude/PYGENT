from typing import Dict, Any, Tuple
import config

class AutonomyManager:
    """
    PHYGENT Autonomy State Machine Manager.
    States: OBSERVE, UNDERSTAND, PROPOSE, ACT, ASK, WAIT, PAUSE, STOP.
    """
    def __init__(self):
        self.current_state = "OBSERVE"

    def transition(self, new_state: str):
        valid_states = {"OBSERVE", "UNDERSTAND", "PROPOSE", "ACT", "ASK", "WAIT", "PAUSE", "STOP"}
        if new_state in valid_states:
            self.current_state = new_state

    def evaluate_policy(self, perception_data: Dict[str, Any], best_action: Dict[str, Any], safety_reason: str) -> str:
        if self.current_state in ("STOP", "PAUSE"):
            return self.current_state

        if perception_data.get("status") == "CAMERA_OFFLINE":
            self.current_state = "WAIT"
            return "WAIT"

        confidence = perception_data.get("confidence", 0.0)
        if confidence < config.CONFIDENCE_THRESHOLD:
            self.current_state = "WAIT"
            return "WAIT"

        if best_action is None or "NO_SAFE_ACTION" in safety_reason:
            self.current_state = "ASK"
            return "ASK"

        # High confidence + allowed task + safe -> ACT
        self.current_state = "ACT"
        return "ACT"
