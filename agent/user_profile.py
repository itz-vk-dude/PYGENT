from typing import Dict, Any, List

class UserProfile:
    """
    User Profile Manager.
    Stores language choice (Tanglish/English), response style, and user habits.
    """
    def __init__(self):
        self.language = "Tanglish"
        self.response_style = "Warm Companion"
        self.preferences = ["Prefer clear workspace", "Friendly tone"]

    def get_preferences(self) -> List[str]:
        return list(self.preferences)
