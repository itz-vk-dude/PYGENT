import json
from typing import Dict, Any
from reasoning.grok import GrokAPI
from reasoning.prompts import SYSTEM_AGENT_REASONING_PROMPT, EXPLAIN_DECISION_PROMPT
from reasoning.response_parser import ResponseParser

class ReasoningEngine:
    """
    PHYGENT Grok Cognition Engine.
    Processes full world context and natural user speech to generate structured task proposals and Tanglish dialogue.
    Enforces strict separation: Reasoning Engine output passes to Autonomy Manager & Safety Engine before execution.
    """
    def __init__(self):
        self.grok = GrokAPI()
        self.parser = ResponseParser()

    def explain_decision(self, state: Dict[str, Any], ml_pred: tuple, phys_pred: tuple, hybrid_pred: tuple, action: Dict[str, Any], score: float) -> str:
        user_prompt = EXPLAIN_DECISION_PROMPT.format(
            object_pos=f"({state.get('x', 0):.1f}, {state.get('y', 0):.1f})",
            velocity=f"({state.get('vx', 0):.1f}, {state.get('vy', 0):.1f})",
            ml_pred=f"({ml_pred[0]:.1f}, {ml_pred[1]:.1f})",
            phys_pred=f"({phys_pred[0]:.1f}, {phys_pred[1]:.1f})",
            hybrid_pred=f"({hybrid_pred[0]:.1f}, {hybrid_pred[1]:.1f})",
            target_xyz=f"({action.get('x', 0):.1f}, {action.get('y', 0):.1f}, {action.get('z', 0):.1f})" if action else "(None)",
            score=f"{score:.2f}"
        )
        return self.grok.query("You are PHYGENT's Decision Explanation Module.", user_prompt)

    def process_natural_interaction(self, user_transcript: str, current_phygent_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process natural user speech + central PHYGENT_STATE context.
        """
        context_str = json.dumps({
            "system_mode": current_phygent_state.get("system_mode", "SIMULATION"),
            "person_present": current_phygent_state.get("person_present", False),
            "objects": current_phygent_state.get("objects", []),
            "robot_position": current_phygent_state.get("robot", {}).get("position", [135, 0, 150]),
            "task": current_phygent_state.get("task", {}).get("name", "IDLE"),
            "autonomy_state": current_phygent_state.get("agent", {}).get("autonomy_state", "OBSERVE")
        })

        user_prompt = f"PHYGENT REAL-TIME WORLD CONTEXT:\n{context_str}\n\nUSER SPEECH: '{user_transcript}'"

        raw_response = self.grok.query(SYSTEM_AGENT_REASONING_PROMPT, user_prompt)
        parsed = self.parser.parse_json_response(raw_response)

        # Ensure minimal structure
        if "speech_response" not in parsed or not parsed["speech_response"]:
            # Tanglish fallback
            lower = user_transcript.lower()
            if "crowded" in lower or "block" in lower or "move" in lower:
                parsed["speech_response"] = "Aamaa pa! Area konjam crowded-a irukku. Naan safe position check pannitu clear panren."
                parsed["task_proposal"] = "CLEAR_WORKSPACE"
                parsed["requested_action"] = {"type": "MOVE_OFFSET", "delta_xyz": [-30, 0, 0]}
            elif "hello" in lower or "hi" in lower or "hey" in lower:
                parsed["speech_response"] = "Vanakkam pa! Naan PHYGENT. Unge workspace-a safe-a monitor panren!"
            else:
                parsed["speech_response"] = "Seri pa! Naan paathutu thaan irukken. Vera enna pannanum sollunga."

        return parsed
