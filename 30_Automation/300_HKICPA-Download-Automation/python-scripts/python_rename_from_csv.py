import os
import shutil
import pandas as pd
from urllib.parse import urlparse

MANIFEST_FILE = "hkicpa_manifest.csv"
RAW_DIR = "downloads_raw"
CLEAN_DIR = "downloads_clean"

os.makedirs(CLEAN_DIR, exist_ok=True)

df = pd.read_csv(MANIFEST_FILE)

if "url" not in df.columns:
    raise SystemExit("ERROR: No 'url' column in manifest. Run python_attach_urls.py first.")

missing = []
for _, row in df.iterrows():
    url = row["url"]
    clean_name = row["filename"]
    raw_name = os.path.basename(urlparse(url).path) or "file.pdf"
    src = os.path.join(RAW_DIR, raw_name)
    dst = os.path.join(CLEAN_DIR, clean_name)

    if not os.path.exists(src):
        missing.append(raw_name)
        continue

    shutil.copy2(src, dst)

if missing:
    print("Missing raw files (download first via python_download_raw.py):")
    for m in missing:
        print(f"  - {m}")

print(f"✓ Done. Output: {CLEAN_DIR}/")
