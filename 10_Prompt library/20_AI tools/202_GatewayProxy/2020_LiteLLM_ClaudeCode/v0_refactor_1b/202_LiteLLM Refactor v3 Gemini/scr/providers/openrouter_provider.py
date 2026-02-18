from typing import List

import requests


OPENROUTER_MODELS_URL = "https://openrouter.ai/api/v1/models"


def discover(api_key: str, timeout: int = 8) -> List[str]:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    response = requests.get(OPENROUTER_MODELS_URL, headers=headers, timeout=timeout)
    response.raise_for_status()
    payload = response.json()
    return [m.get("id", "") for m in payload.get("data", []) if m.get("id")]

