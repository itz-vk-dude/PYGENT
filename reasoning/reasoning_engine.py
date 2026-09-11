from reasoning.grok_api import GrokAPI
from reasoning.nvidia_api import NvidiaBuildAPI
from reasoning.prompts import SYSTEM_PROMPT, EXPLAIN_DECISION_PROMPT
from typing import Dict, Any

class ReasoningEngine:
    def __init__(self):
        self.grok = GrokAPI()
        self.nvidia = NvidiaBuildAPI()

    def explain_decision(self, state: Dict[str, Any], ml_pred: tuple, phys_pred: tuple, hybrid_pred: tuple, action: Dict[str, Any], score: float) -> str:
        """
        Formats current PHYGENT state context and generates an executive Grok explanation for real-time trajectory interception.
        """
        user_prompt = EXPLAIN_DECISION_PROMPT.format(
            object_pos=f"({state.get('x', 0):.1f}, {state.get('y', 0):.1f})",
            velocity=f"({state.get('vx', 0):.1f}, {state.get('vy', 0):.1f})",
            ml_pred=f"({ml_pred[0]:.1f}, {ml_pred[1]:.1f})",
            phys_pred=f"({phys_pred[0]:.1f}, {phys_pred[1]:.1f})",
            hybrid_pred=f"({hybrid_pred[0]:.1f}, {hybrid_pred[1]:.1f})",
            target_xyz=f"({action.get('x', 0):.1f}, {action.get('y', 0):.1f}, {action.get('z', 0):.1f})",
            score=f"{score:.2f}"
        )
        return self.grok.query(SYSTEM_PROMPT, user_prompt)

    def process_voice_command(self, user_transcript: str, current_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Conversational Brain powered by Grok NLP API.
        Extracts user intent and returns a super friendly female Tanglish spoken response + structural command.
        Receives central PHYGENT_STATE for state-aware responses ("What do you see?", "What are you doing?").
        """
        phy_st = current_state.get("phygent_state", {})
        person_str = "Detected (Person is present in camera)" if phy_st.get("person_present", False) else "Not detected"
        objects_str = str(phy_st.get("objects", []))
        task_str = phy_st.get("current_task", "TRACKING")
        last_cmd = phy_st.get("last_command", "IDLE")

        system_prompt = f"""
You are PHYGENT, a super friendly, caring, warm, and highly intelligent female robotic companion.
You speak like a real human friend—comfortable, conversational, warm, and full of natural empathy!

CRITICAL LANGUAGE RULE:
- ALL spoken responses and text MUST BE STRICTLY IN TANGLISH (Tamil language written ONLY using English/Latin alphabet, e.g. "Vanakkam pa! Robo arm-a left side-la move panren!", "Sure boss, naan ready-a irukken!").
- DO NOT use any Tamil script (like தமிழ் unicode script). Use ONLY English letters!
- Keep tone warm, natural, and human-like (e.g. use expressions like "pa", "boss", "kandippa", "sure-ah", "apdiya").

CURRENT PHYGENT REAL-TIME STATE:
- Person in Camera: {person_str}
- Objects Detected: {objects_str}
- Robot Status: READY
- Robot Position (XYZ mm): {phy_st.get("robot_position", [135, 6, 150])}
- Current Task: {task_str}
- Last Voice Command: {last_cmd}

If the user asks "What do you see?" or "What are you doing?" or tells the arm to move, answer warmly and naturally in Latin script Tanglish!

Output MUST be a valid JSON string with keys:
"speech_response": (string, 1-2 sentence friendly Tanglish spoken response using Latin script only)
"intent": (string: "MOVE_LEFT", "MOVE_RIGHT", "MOVE_UP", "MOVE_DOWN", "HOME", "STOP", "PAUSE", "GRIP_OPEN", "GRIP_CLOSE", or "GENERAL_CONVERSATION")
"delta_xyz": ([x, y, z] offsets in mm, e.g. [-50, 0, 0] for left)
"""
        user_prompt = f"User Transcript: '{user_transcript}'"
        
        raw_res = self.grok.query(system_prompt, user_prompt)
        try:
            import json
            clean_str = raw_res
            if "```json" in clean_str:
                clean_str = clean_str.split("```json")[1].split("```")[0].strip()
            elif "```" in clean_str:
                clean_str = clean_str.split("```")[1].split("```")[0].strip()
            
            parsed = json.loads(clean_str)
            if "speech_response" in parsed:
                return parsed
        except Exception:
            pass

        lower = user_transcript.lower()
        if "left" in lower:
            return {"speech_response": "Sure pa! Robo arm-a left side-la move panren.", "intent": "MOVE_LEFT", "delta_xyz": [-50, 0, 0]}
        elif "right" in lower:
            return {"speech_response": "Kandippa! Arm-a right side-la nalla move panren.", "intent": "MOVE_RIGHT", "delta_xyz": [50, 0, 0]}
        elif "up" in lower:
            return {"speech_response": "Okay boss! Arm-a mela elevation panren.", "intent": "MOVE_UP", "delta_xyz": [0, 0, 40]}
        elif "down" in lower:
            return {"speech_response": "Aamaa pa, arm-a keelai irakkiren.", "intent": "MOVE_DOWN", "delta_xyz": [0, 0, -40]}
        elif "home" in lower:
            return {"speech_response": "Sure pa, robo arm-a home position-ukku thirumba kondu vanten!", "intent": "HOME", "delta_xyz": [0, 0, 0]}
        elif "stop" in lower:
            return {"speech_response": "Okay boss! System-a stop pantaen pa.", "intent": "STOP", "delta_xyz": [0, 0, 0]}
        elif "pause" in lower:
            return {"speech_response": "Okay pa, system pause-la irukku.", "intent": "PAUSE", "delta_xyz": [0, 0, 0]}
        elif "see" in lower or "doing" in lower:
            p_text = "ungala thaan" if phy_st.get("person_present", False) else "object tracking"
            return {
                "speech_response": f"Naan camera-la {p_text} paarthutu irukken pa! 3D twin real-time sync-la irukku.",
                "intent": "GENERAL_CONVERSATION",
                "delta_xyz": [0, 0, 0]
            }
        else:
            return {
                "speech_response": "Hello pa! Naan PHYGENT, unga friendly assistant. Trajectory-a track pannittu irukken, vera enna pannanum sollunga?",
                "intent": "GENERAL_CONVERSATION",
                "delta_xyz": [0, 0, 0]
            }



    def analyze_feedback(self, error_px: float, eval_status: str, experiences: int) -> str:
        """
        Uses NVIDIA Build LLM for self-evaluation, trajectory anomaly analysis, and continual learning audit.
        """
        system_prompt = "You are the NVIDIA Self-Evaluation & Continual Learning Audit LLM for PHYGENT."
        user_prompt = f"Feedback error: {error_px:.1f}px. Status: {eval_status}. Total experiences logged: {experiences}. Provide 1-sentence evaluation."
        return self.nvidia.query(system_prompt, user_prompt)



