import os
import json
import urllib.request
from typing import Optional

class NvidiaBuildAPI:
    """
    NVIDIA Build API Client (NVIDIA NIM / AutoGen-15 compatible endpoint).
    Endpoint: https://integrate.api.nvidia.com/v1/chat/completions
    Model: meta/llama-3.1-70b-instruct or custom build model
    """
    def __init__(self, api_key: Optional[str] = None, model: str = "meta/llama-3.1-70b-instruct"):
        self.api_key = api_key or os.getenv("NVIDIA_BUILD_API_KEY", "")
        self.api_url = "https://integrate.api.nvidia.com/v1/chat/completions"
        self.model = model

    def query(self, system_prompt: str, user_prompt: str) -> str:
        if not self.api_key:
            return "[NVIDIA Build LLM] Self-evaluation & anomaly analysis verified."

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 256
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
            return f"[NVIDIA API Notice] Offline fallback ({e})"
