---
Title: AI Usage Analysis – Core Scripts
Created: 2026-01-10
Tags:
  - ai/usage
  - scripts
  - "#pipeline"
  - PPLX
---

This note contains all scripts needed for the **core pipeline**.

---

## Inspect_pplx_md. Py

Purpose: inspect Perplexity Markdown structure.

```python
from pathlib import Path
import re

BASE = Path.cwd()
PPLX_DIR = BASE / "exports" / "pplx"
OUT = BASE / "out" / "pplx_inspect.txt"
OUT.parent.mkdir(exist_ok=True)

HEAD_RE = re.compile(r"^(#{1,6})\\s+(.+)$", re.M)

lines = []
for md in PPLX_DIR.glob("*.md"):
    text = md.read_text(encoding="utf-8", errors="ignore")
    heads = [m.group(0) for m in HEAD_RE.finditer(text)]
    lines.append(f"== {md.name} ==")
    lines.extend(heads[:30] if heads else ["(no headings)"])
    lines.append("")

OUT.write_text("\\n".join(lines), encoding="utf-8")
print(f"Wrote {OUT}")
```
Run:  
`python inspect_pplx_md.py`

## parse_pplx_threads.py

Purpose: model Perplexity usage as thread-level events.

```python
Import csv
From pathlib import Path
Import frontmatter

BASE = Path.Cwd ()
SRC = BASE / "exports" / "pplx"
OUT = BASE / "out" / "pplx_threads. Csv"
OUT.Parent.Mkdir (exist_ok=True)

Rows = []
For md in SRC.Glob ("*. Md"):
    Post = frontmatter.Load (md)
    Rows.Append ({
        "title": post.Get ("title", ""),
        "date": post.Get ("date", ""),
        "uuid": post.Get ("uuid", ""),
        "model": post.Get ("model", ""),
        "mode": post.Get ("mode", ""),
        "content_len": len (post. Content or "")
    })

With OUT.Open ("w", newline="", encoding="utf-8") as f:
    W = csv.DictWriter (f, fieldnames=rows[0]. Keys ())
    w.writeheader ()
    w.writerows (rows)

Print (f"Wrote {OUT}")

```

## parse_chatgpt_and_daily.py

Purpose: extract ChatGPT user turns and daily metrics.
```python
import json, csv, zipfile
from datetime import datetime
from pathlib import Path

BASE = Path.cwd()
ZIP = BASE / "exports" / "chatgpt.zip"
OUT_TURNS = BASE / "out" / "chatgpt_user_turns.csv"
OUT_DAILY = BASE / "out" / "daily_metrics.csv"
OUT_TURNS.parent.mkdir(exist_ok=True)

turns = []
daily = {}

with zipfile.ZipFile(ZIP) as z:
    data = json.loads(z.read("conversations.json"))
    for c in data:
        for m in c.get("mapping", {}).values():
            msg = m.get("message")
            if not msg:
                continue
            if msg.get("author", {}).get("role") != "user":
                continue
            ts = msg.get("create_time")
            if not ts:
                continue

            iso = datetime.utcfromtimestamp(ts).isoformat()
            clen = len(msg.get("content", {}).get("parts", [""])[0])

            turns.append({
                "ts_utc": iso,
                "thread_id": c.get("id", ""),
                "content_len": clen
            })

            day = iso[:10]
            daily.setdefault(day, {"chatgpt": 0, "perplexity": 0})
            daily[day]["chatgpt"] += 1

with OUT_TURNS.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=turns[0].keys())
    w.writeheader()
    w.writerows(turns)

with OUT_DAILY.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["date", "platform", "events"])
    w.writeheader()
    for d, v in daily.items():
        for p, n in v.items():
            w.writerow({"date": d, "platform": p, "events": n})

print("ChatGPT parsing complete")

```
---
## analyze_usage_basic.py

Purpose: sessionize ChatGPT usage.
```
import csv
from datetime import datetime, timedelta
from pathlib import Path

BASE = Path.cwd()
CHAT = BASE / "out" / "chatgpt_user_turns.csv"
IDLE_MIN = 30

with CHAT.open(encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

rows.sort(key=lambda r: r["ts_utc"])

sessions = []
cur = None

for r in rows:
    ts = datetime.fromisoformat(r["ts_utc"])
    if not cur or ts - cur["last"] > timedelta(minutes=IDLE_MIN):
        cur = {"start": ts, "last": ts, "turns": 0}
        sessions.append(cur)
    cur["last"] = ts
    cur["turns"] += 1

out = BASE / "out" / "usage_report.txt"
with out.open("w", encoding="utf-8") as f:
    f.write(f"sessions: {len(sessions)}\n")

print(f"Wrote {out}")

```