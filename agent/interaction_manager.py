from typing import Dict, Any, Optional
from interaction.speech_input import SpeechInputEngine
from interaction.speech_output import SpeechOutputEngine
from interaction.conversation import ConversationEngine

class InteractionManager:
    """
    Connects speech input, conversation engine, agent reasoning, and TTS speech output.
    """
    def __init__(self, conversation_engine: ConversationEngine):
        self.conversation = conversation_engine
        self.speech_in = SpeechInputEngine()
        self.speech_out = SpeechOutputEngine()

    def process_voice_transcript(self, transcript: str, phygent_state: Dict[str, Any]) -> Dict[str, Any]:
        res = self.conversation.handle_user_message(transcript, phygent_state)
        spoken_response = res.get("speech_response", "")
        if spoken_response:
            self.speech_out.speak(spoken_response)
        return res
