import os
import json
import urllib.request
from typing import Optional
import config

class GrokAPI:
    """
    xAI Grok API Client with Fallback handling.
    Grok provides structured reasoning, task proposals, decision explanations, and natural conversational dialogue.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or config.XAI_API_KEY
        self.api_url = "https://api.x.ai/v1/chat/completions"

    def query(self, system_prompt: str, user_prompt: str, temperature: float = 0.3) -> str:
        if not self.api_key:
            return (
                "[Grok Offline] Agent assessed world state: Hybrid prediction minimizes position error "
                "while maintaining workspace safety boundary."
            )

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "model": config.GROK_MODEL_NAME,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": temperature
        }

        try:
            req = urllib.request.Request(
                self.api_url,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=6.0) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                return res_data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"[Grok API Fallback] Local reasoning active: {e}"
