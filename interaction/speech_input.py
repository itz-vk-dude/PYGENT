from typing import Optional, Callable

class SpeechInputEngine:
    """
    Decoupled Speech-To-Text Input Engine.
    Supports browser Speech Recognition API endpoints as well as local backend audio listeners.
    """
    def __init__(self):
        self.is_listening = False
        self.callback: Optional[Callable[[str], None]] = None

    def register_callback(self, callback_func: Callable[[str], None]):
        self.callback = callback_func

    def process_transcript(self, user_transcript: str) -> Optional[str]:
        text = user_transcript.strip()
        if text and self.callback:
            self.callback(text)
        return text
