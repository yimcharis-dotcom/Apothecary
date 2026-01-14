import os
import requests
import pandas as pd

MANIFEST_FILE = "hkicpa_manifest.csv"
DOWNLOAD_DIR = "downloads"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

df = pd.read_csv(MANIFEST_FILE)

if "url" not in df.columns:
    raise SystemExit("ERROR: No 'url' column in manifest. Run python_attach_urls.py first.")

for _, row in df.iterrows():
    url = row["url"]
    filename = row["filename"]
    try:
        print(f"Downloading: {filename}")
        r = requests.get(url, allow_redirects=True, timeout=60)
        r.raise_for_status()
        with open(os.path.join(DOWNLOAD_DIR, filename), "wb") as out:
            out.write(r.content)
    except Exception as e:
        print(f"Failed: {filename} → {e}")

print(f"✓ Done. Output: {DOWNLOAD_DIR}/")
