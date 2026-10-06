import os
import json
from typing import Dict, Any
import config

class UserMemoryManager:
    """
    Persistent User Memory & Profile Manager.
    Stores user preferences, language choice (Tanglish/English), and confirmed interaction habits.
    """
    def __init__(self, memory_file: str = None):
        self.memory_file = memory_file or str(config.BASE_DIR / "user_memory.json")
        self.memory: Dict[str, Any] = {
            "user_id": "default_user",
            "preferred_language": "Tanglish",
            "approved_preferences": [],
            "corrections": []
        }
        self.load_memory()

    def load_memory(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    self.memory = json.load(f)
            except Exception as e:
                print(f"[UserMemoryManager] Could not load memory: {e}")

    def save_memory(self):
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, indent=2)
        except Exception as e:
            print(f"[UserMemoryManager] Could not save memory: {e}")

    def add_preference(self, preference: str):
        if preference not in self.memory["approved_preferences"]:
            self.memory["approved_preferences"].append(preference)
            self.save_memory()
