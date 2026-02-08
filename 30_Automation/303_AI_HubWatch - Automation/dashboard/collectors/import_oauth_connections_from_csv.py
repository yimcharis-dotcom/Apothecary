#!/usr/bin/env python3
"""
Import OAuth connections from data/oauth_connections_table.csv into
data/gmail_connections.json.

This lets you fill a table (CSV) and avoid manual JSON array edits.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Dict, List


ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
CSV_PATH = DATA_DIR / "oauth_connections_table.csv"
JSON_PATH = DATA_DIR / "gmail_connections.json"


def _split_scopes(value: str) -> List[str]:
    if not value:
        return []
    # Split on comma; allow semicolon too.
    parts = [p.strip() for p in value.replace(";", ",").split(",")]
    return [p for p in parts if p]


def _row_has_data(row: Dict[str, str]) -> bool:
    keys = ["app_name", "provider", "oauth_scopes", "grant_date", "last_used"]
    return any((row.get(k) or "").strip() for k in keys)


def load_csv_rows(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {path}")

    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for raw in reader:
            row = {k: (v or "").strip() for k, v in raw.items()}
            if not _row_has_data(row):
                continue

            scopes = _split_scopes(row.get("oauth_scopes", ""))

            entry: Dict[str, Any] = {
                "app_name": row.get("app_name", ""),
                "provider": row.get("provider", ""),
                "oauth_scopes": scopes,
                "grant_date": row.get("grant_date", ""),
                "last_used": row.get("last_used", ""),
                "access_type": row.get("access_type", "") or "oauth",
                "source": row.get("source", "") or "csv_import",
            }

            evidence = {
                "domain": row.get("evidence_domain", ""),
                "from_email": row.get("evidence_from_email", ""),
                "last_seen": row.get("evidence_last_seen", ""),
            }
            if any(v for v in evidence.values()):
                entry["evidence"] = evidence

            rows.append(entry)

    return rows


def import_csv_to_json(csv_path: Path, json_path: Path) -> None:
    if not json_path.exists():
        raise FileNotFoundError(f"JSON not found: {json_path}")

    original_text = json_path.read_text(encoding="utf-8")
    data = json.loads(original_text)
    oauth_connections = load_csv_rows(csv_path)

    data["oauth_connections"] = oauth_connections

    # Backup existing JSON before overwrite
    backup_path = json_path.with_suffix(".json.bak")
    backup_path.write_text(original_text, encoding="utf-8")

    json_path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def main() -> None:
    import_csv_to_json(CSV_PATH, JSON_PATH)
    print("Imported OAuth connections from CSV.")
    print(f"CSV:  {CSV_PATH}")
    print(f"JSON: {JSON_PATH}")


if __name__ == "__main__":
    main()
