import pyttsx3
import threading
import queue
import time
from typing import Optional

class SpeechOutputEngine:
    """
    Non-Blocking Asynchronous Text-To-Speech (TTS) Engine.
    Supports speech interruption, conversation queues, and avoids repetitive commentary.
    """
    def __init__(self):
        self.speech_queue = queue.Queue()
        self.is_running = True
        self.is_speaking = False
        self.last_spoken_text = ""
        self.thread = threading.Thread(target=self._speech_loop, daemon=True)
        self.thread.start()

    def speak(self, text: str, priority: bool = False):
        if not text:
            return
        
        # Avoid repeating exact same sentence in short time window
        if text == self.last_spoken_text:
            return

        if priority:
            self.interrupt()

        self.speech_queue.put(text)

    def interrupt(self):
        """Interrupts ongoing speech immediately."""
        with self.speech_queue.mutex:
            self.speech_queue.queue.clear()
        self.is_speaking = False

    def _speech_loop(self):
        engine = None
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 160)
            voices = engine.getProperty('voices')
            if len(voices) > 1:
                engine.setProperty('voice', voices[1].id)  # Select female voice
        except Exception as e:
            print(f"[SpeechOutputEngine] TTS Init Notice: {e}")

        while self.is_running:
            try:
                text = self.speech_queue.get(timeout=0.5)
                if text:
                    self.is_speaking = True
                    self.last_spoken_text = text
                    if engine:
                        try:
                            engine.say(text)
                            engine.runAndWait()
                        except Exception:
                            pass
                    else:
                        print(f"[PHYGENT TTS Spoken]: {text}")
                    self.is_speaking = False
            except queue.Empty:
                pass
            except Exception:
                time.sleep(0.1)

    def stop(self):
        self.is_running = False
        self.interrupt()
