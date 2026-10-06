import json
from typing import Dict, Any

class ResponseParser:
    """
    Parses structured JSON outputs from Grok reasoning responses.
    """
    def parse_json_response(self, raw_text: str) -> Dict[str, Any]:
        if not raw_text:
            return {}

        clean_text = raw_text.strip()
        if "```json" in clean_text:
            clean_text = clean_text.split("```json")[1].split("```")[0].strip()
        elif "```" in clean_text:
            clean_text = clean_text.split("```")[1].split("```")[0].strip()

        try:
            parsed = json.loads(clean_text)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            pass

        return {
            "understanding": raw_text,
            "speech_response": raw_text,
            "requested_action": None
        }
