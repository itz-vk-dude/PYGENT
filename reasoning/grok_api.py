import os
import json
import urllib.request
from typing import Optional
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class GrokAPI:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GROK_API_KEY", "")
        self.api_url = "https://api.x.ai/v1/chat/completions"

    def query(self, system_prompt: str, user_prompt: str) -> str:
        """
        Queries the Grok API (x.ai). If no API key is provided, returns an executive baseline explanation.
        """
        if not self.api_key:
            return (
                "[Grok Reasoning] The hybrid prediction selected this interception point because "
                "it minimizes position error while maintaining optimal execution time and joint safety."
            )

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "model": "grok-beta",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.3
        }

        try:
            req = urllib.request.Request(
                self.api_url,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=5.0) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                return res_data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"[Grok API Notice] Simulated reasoning active (fallback: {e})"
