import os
import requests
from urllib.parse import urlparse

links_file = "hkicpa_links.txt"
download_dir = "downloads_raw"

os.makedirs(download_dir, exist_ok=True)

with open(links_file, "r", encoding="utf-8") as f:
    urls = [u.strip() for u in f if u.strip()]

for url in urls:
    try:
        print(f"Downloading: {url}")
        r = requests.get(url, allow_redirects=True, timeout=60)
        r.raise_for_status()
        fname = os.path.basename(urlparse(url).path) or "file.pdf"
        with open(os.path.join(download_dir, fname), "wb") as out:
            out.write(r.content)
    except Exception as e:
        print(f"Failed: {url} → {e}")

print(f"✓ Done. Output: {download_dir}/")
