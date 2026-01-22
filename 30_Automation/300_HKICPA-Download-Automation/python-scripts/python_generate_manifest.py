import re
import pandas as pd

INPUT_FILE = "contents_raw.txt"
OUTPUT_FILE = "hkicpa_manifest_draft.csv"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    raw = f.read()

lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]

merged = []
i = 0
while i < len(lines):
    if i + 1 < len(lines):
        pair = lines[i] + " " + lines[i + 1]
        if pair in ["CONCEPTUAL FRAMEWORK", "SME-FRF & SME-FRS"]:
            merged.append(pair)
            i += 2
            continue
    merged.append(lines[i])
    i += 1
lines = merged

DATE_TAIL = re.compile(r"(?P<date>\d{1,2}/\d{2}(?:\(\d{1,2}/\d{2}\))?)\s*$")
CODE_FIND = re.compile(
    r"^(HKAS\s+\d+|HKFRS\s+\d+|HK\(IFRIC\)-Int\s+\d+|HK\(SIC\)-Int\s+\d+|HK-Int\s+\d+|"
    r"AG\s+\d+|AB\s+\d+|HKFRS-PE|SME-FRF & SME-FRS|HKFRS Practice Statement\s+\d+|"
    r"Amendments to\s+HKFRS-PE|Amendments to\s+HKFRS\s+\d+|Amendments to\s+HKAS\s+\d+|"
    r"PREFACE|CONCEPTUAL FRAMEWORK|GLOSSARY)\b"
)

HEADING_SKIP = [
    "Section 1:",
    "Section 2:",
    "HONG KONG",
    "ACCOUNTING GUIDELINES",
    "ACCOUNTING BULLETINS",
]

def is_heading(line):
    return any(line.startswith(h) for h in HEADING_SKIP)

def normalize(s):
    s = s.replace("…", " ")
    s = re.sub(r"[.·]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

current_section = None
buf = []
records = []

for ln in lines:
    if ln.startswith("Section 1:"):
        current_section = "Section 1"
        continue
    if ln.startswith("Section 2:"):
        current_section = "Section 2"
        continue
    if is_heading(ln):
        continue

    m = DATE_TAIL.search(ln)
    if not m:
        buf.append(ln)
        continue

    date = m.group("date")
    before = ln[: m.start()].strip(" .·…-")
    if before:
        buf.append(before)

    full = normalize(" ".join(buf))

    cm = CODE_FIND.match(full)
    if cm:
        code = cm.group(1)
        title = full[cm.end() :].strip(" -")
    else:
        code = ""
        title = full

    pm = re.match(r"^(\([^)]+\))\s+(.+)$", title)
    if pm:
        code = f"{code} {pm.group(1)}" if code else pm.group(1)
        title = pm.group(2)

    if code and title.startswith(code + " "):
        title = title[len(code) :].strip()

    if code and title.upper() == code.upper():
        title = ""

    date_fmt = date.replace("/", "-")
    parts = [p for p in [code, title, date_fmt] if p]
    filename = "-".join(parts) + ".pdf"
    filename = re.sub(r'[<>:"/\\|?*]', "-", filename)
    filename = re.sub(r"\s+", " ", filename).strip()

    records.append(
        {
            "section": current_section or "",
            "code": code,
            "title": title,
            "issue_review": date,
            "filename": filename,
        }
    )

    buf = []

df = pd.DataFrame(records)
df.insert(0, "row", range(1, len(df) + 1))
df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

print(f"✓ Generated {len(df)} records → {OUTPUT_FILE}")
print("  Review in Excel, then save as hkicpa_manifest.csv")
