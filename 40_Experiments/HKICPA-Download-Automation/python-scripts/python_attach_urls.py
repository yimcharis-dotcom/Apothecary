import pandas as pd

MANIFEST_FILE = "hkicpa_manifest.csv"
LINKS_FILE = "hkicpa_links.txt"

try:
    df = pd.read_csv(MANIFEST_FILE)
except FileNotFoundError:
    raise SystemExit(
        f"ERROR: '{MANIFEST_FILE}' not found. "
        f"Generate it first via python_generate_manifest.py and Excel."
    )

try:
    with open(LINKS_FILE, "r", encoding="utf-8") as f:
        urls = [ln.strip() for ln in f if ln.strip()]
except FileNotFoundError:
    raise SystemExit(
        f"ERROR: '{LINKS_FILE}' not found. "
        f"Run python_extract_links.py first to create it."
    )

if len(urls) != len(df):
    raise SystemExit(
        f"ERROR: {len(urls)} URLs in {LINKS_FILE} vs {len(df)} rows in {MANIFEST_FILE}. "
        "Counts must match before attaching URLs."
    )

df["url"] = urls
df.to_csv(MANIFEST_FILE, index=False, encoding="utf-8")

print(f"✓ Attached {len(urls)} URLs to {MANIFEST_FILE}")
print("  (Only 'url' column was added/updated; code/title/issue_review/filename unchanged.)")
