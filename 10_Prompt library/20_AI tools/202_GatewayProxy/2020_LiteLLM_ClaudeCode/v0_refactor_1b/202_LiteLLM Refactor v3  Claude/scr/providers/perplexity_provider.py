from typing import List

import requests


PERPLEXITY_MODELS_URL = "https://api.perplexity.ai/models"
PERPLEXITY_FALLBACK_MODELS = [
    "sonar",
    "sonar-pro",
    "sonar-reasoning-pro",
    "sonar-deep-research",
]


def discover(api_key: str, timeout: int = 8) -> List[str]:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.get(PERPLEXITY_MODELS_URL, headers=headers, timeout=timeout)
        response.raise_for_status()
        payload = response.json()
        models = [m.get("id", "") for m in payload.get("data", []) if m.get("id")]
        return models or PERPLEXITY_FALLBACK_MODELS
    except requests.HTTPError as exc:
        # Perplexity may not expose a list endpoint for all keys/plans.
        status_code = getattr(exc.response, "status_code", None)
        if status_code in (404, 405):
            return PERPLEXITY_FALLBACK_MODELS
        raise
