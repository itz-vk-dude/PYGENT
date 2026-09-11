import threading
import time

class JARVISVoiceEngine:
    """
    JARVIS Voice Feedback System using offline Text-to-Speech (pyttsx3).
    Provides natural executive spoken status updates without blocking execution.
    """
    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self.engine = None
        if self.enabled:
            try:
                import pyttsx3
                self.engine = pyttsx3.init()
                self.engine.setProperty('rate', 170)
                self.engine.setProperty('volume', 0.9)
            except Exception as e:
                print(f"[JARVIS Voice] TTS initialization warning: {e}")
                self.enabled = False

    def _set_female_voice(self, eng):
        try:
            voices = eng.getProperty('voices')
            for v in voices:
                v_name = v.name.lower()
                if any(kw in v_name for kw in ["zira", "female", "hazel", "catherine", "samantha", "eva", "jenny", "aria"]):
                    eng.setProperty('voice', v.id)
                    break
        except Exception:
            pass

    def speak(self, text: str):
        """Speaks text asynchronously in a non-blocking thread using a female voice."""
        if not self.enabled:
            print(f"🎙 [PHYGENT Voice Simulated]: {text}")
            return

        def _talk():
            try:
                import pyttsx3
                eng = pyttsx3.init()
                eng.setProperty('rate', 165)
                eng.setProperty('volume', 0.95)
                self._set_female_voice(eng)
                eng.say(text)
                eng.runAndWait()
            except Exception as e:
                print(f"[PHYGENT Voice] Speech error: {e}")

        threading.Thread(target=_talk, daemon=True).start()


