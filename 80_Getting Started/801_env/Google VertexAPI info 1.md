---
tags:
  - ai/integration
  - google
  - vertex-ai
  - gemini-ai
  - plugin
---
# Google Vertex AI Config
## 🔑 Identity & Secrets (Start Here)  

| Credential Type            | Key Format                   | Linked To                   | Usage                                        |
| :------------------------- | :--------------------------- | :-------------------------- | :------------------------------------------- |
| **Gemini API Key**         | `AIza...`                    | **Personal Google Account** | **Primary.** For Plugins, Cursor, VS Code.   |
| **Vertex Service Account** | `JSON` file or `AQ...` token | `vertex-express@...`        | **Advanced.** For backend apps or Cloud IAM. |


---

## 1. Gemini API (Simple)

> **Best for:** Personal coding, Obsidian plugins, quick scripts.
 
- **API Key:**

```text
AIzaSyCjYO48hmV10fmQP5y-TNKQp9MT7_tJcJc
```

- **Base URL:** `https://generativelanguage.googleapis.com`

## 2. Vertex AI (Enterprise)
>
> **Best for:** High-throughput production apps, specific cloud regions.

```
AQ.Ab8RN6KExNU3gTEZabRxD5p5LUm_6ukRonkVr-hzJohMdCD_2A
```

- **Project ID:** `gen-lang-client-0127739997`
- **Location:** `asia-east2` (Hong Kong), `asia-southeast1` (Singapore), or `us-central1`
- **Service Email:** `vertex-express@gen-lang-client-0127739997.iam.gserviceaccount.com`

**Base URLs:**

- **Hong Kong (Low Latency):** `https://asia-east2-aiplatform.googleapis.com/v1`
- **Singapore (Standard):** `https://asia-southeast1-aiplatform.googleapis.com/v1`
- **US Central:** `https://us-central1-aiplatform.googleapis.com/v1`
**Service Account JSON (Optional):**

```json
{
  "type": "service_account",
  "project_id": "gen-lang-client-0127739997",
  ...
}
```

## Quick Links

- [Google Cloud Console](https://console.cloud.google.com/vertex-ai)
- [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
- [API Documentation](https://cloud.google.com/vertex-ai/docs/reference/rest)

## Usage Snippet

```bash
curl -X POST \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
```

## Vertex AI Usage Snippet

## 🛠️ Connectivity & Troubleshooting

### Connectivity (Hong Kong)

- **Vertex AI**: **Works** without VPN (Region: `us-central1` or `asia-southeast1`).
- **AI Studio (Gemini API)**: May require VPN.

### Common Errors (Smart Composer / Plugins)

| Error | Cause | Fix |
| :--- | :--- | :--- |
| `400 Bad Request` | "Thinking Level" Mismatch | **Turn OFF Thinking** for `gemini-3-pro` (only works on Flash). |
| `401 Unauthorized` | Invalid API Key | Use the **AI Studio Key** (`AIza...`), not the Vertex token (`AQ...`). |
| `ERR_CONNECTION_REFUSED` | Ollama offline | Start the **Ollama** app. |
