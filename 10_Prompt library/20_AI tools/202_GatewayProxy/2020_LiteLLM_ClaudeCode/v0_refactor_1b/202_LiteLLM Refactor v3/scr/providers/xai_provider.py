from typing import List

import requests


XAI_MODELS_URLS = (
    "https://api.x.ai/v1/models",
    "https://api.x.ai/v1/language-models",
)


def discover(api_key: str, timeout: int = 8) -> List[str]:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    last_error = None
    for url in XAI_MODELS_URLS:
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            payload = response.json()
            return [m.get("id", "") for m in payload.get("data", []) if m.get("id")]
        except Exception as exc:
            last_error = exc

    raise RuntimeError(f"xAI model discovery failed across endpoints: {last_error}")
