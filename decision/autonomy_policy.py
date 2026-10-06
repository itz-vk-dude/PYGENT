from typing import Dict, Any, Tuple
import config

class AutonomyPolicy:
    """
    Evaluates whether autonomous execution is authorized.
    High confidence + allowed task + safe -> ACT
    Unclear intent -> ASK
    Unsafe -> PAUSE / STOP
    Low confidence -> WAIT
    """
    def check_authorization(self, confidence: float, task_name: str, is_safe: bool) -> Tuple[str, str]:
        if not is_safe:
            return "PAUSE", "Safety gate rejected action"

        if confidence < config.CONFIDENCE_THRESHOLD:
            return "WAIT", f"Perception confidence {confidence:.2f} below threshold {config.CONFIDENCE_THRESHOLD}"

        if task_name == "UNCLEAR_INTENT":
            return "ASK", "Task intent requires human clarification"

        return "ACT", "Authorized for autonomous execution"
