from typing import List

def discover(api_key: str, timeout: int = 8) -> List[str]:
    try:
        from google import genai
    except Exception as exc:
        raise RuntimeError(
            "google-genai SDK is required for Gemini discovery. "
            "Install with: pip install google-genai"
        ) from exc

    client = genai.Client(api_key=api_key)
    out: List[str] = []
    for model in client.models.list():
        name = getattr(model, "name", "")
        if name.startswith("models/"):
            name = name.split("/", 1)[1]
        if name:
            out.append(name)
    return out
