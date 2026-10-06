from typing import Dict, Any
from reasoning.reasoning_engine import ReasoningEngine

class ConversationEngine:
    """
    Natural English & Tanglish Dialogue State Engine.
    Handles conversation history, context continuation, and user preferences.
    """
    def __init__(self, reasoning_engine: ReasoningEngine = None):
        self.reasoning = reasoning_engine or ReasoningEngine()
        self.conversation_history = []

    def handle_user_message(self, user_transcript: str, phygent_state: Dict[str, Any]) -> Dict[str, Any]:
        result = self.reasoning.process_natural_interaction(user_transcript, phygent_state)
        
        self.conversation_history.append({
            "user": user_transcript,
            "agent": result.get("speech_response", ""),
            "timestamp": phygent_state.get("timestamp", 0.0)
        })
        if len(self.conversation_history) > 20:
            self.conversation_history.pop(0)

        return result
