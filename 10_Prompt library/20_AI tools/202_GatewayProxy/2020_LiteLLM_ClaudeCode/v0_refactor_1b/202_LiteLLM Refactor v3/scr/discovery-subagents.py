import argparse
import copy
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

import requests
import yaml


@dataclass(frozen=True)
class ModelFamily:
    alias_name: str
    candidates: List[str]
    fallback_prefix: Optional[str] = None


DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.yaml"
OPENROUTER_MODELS_URL = "https://openrouter.ai/api/v1/models"
OPENROUTER_API_KEY_ENV = "OPENROUTER_API_KEY"


FAMILIES: List[ModelFamily] = [
    ModelFamily(
        alias_name="claude-sonnet-4-5",
        candidates=[
            "anthropic/claude-sonnet-4.5",
            "anthropic/claude-sonnet-4",
        ],
        fallback_prefix="anthropic/claude-sonnet-",
    ),
    ModelFamily(
        alias_name="claude-opus-4-5",
        candidates=[
            "anthropic/claude-opus-4.5",
            "anthropic/claude-opus-4",
        ],
        fallback_prefix="anthropic/claude-opus-",
    ),
    ModelFamily(
        alias_name="deepseek-v3-2",
        candidates=[
            "deepseek/deepseek-v3.2",
            "deepseek/deepseek-v3.1",
            "deepseek/deepseek-v3",
        ],
        fallback_prefix="deepseek/deepseek-v3",
    ),
    ModelFamily(
        alias_name="deepseek-r1-0528",
        candidates=[
            "deepseek/deepseek-r1-0528",
            "deepseek/deepseek-r1",
        ],
        fallback_prefix="deepseek/deepseek-r1",
    ),
    ModelFamily(
        alias_name="kimi-k2-5",
        candidates=[
            "moonshotai/kimi-k2.5",
            "moonshotai/kimi-k2",
        ],
        fallback_prefix="moonshotai/kimi-",
    ),
    ModelFamily(
        alias_name="glm-5",
        candidates=[
            "z-ai/glm-5",
        ],
        fallback_prefix="z-ai/glm-5",
    ),
    ModelFamily(
        alias_name="glm-4-7",
        candidates=[
            "z-ai/glm-4.7",
        ],
        fallback_prefix="z-ai/glm-4.7",
    ),
    ModelFamily(
        alias_name="glm-4-7-flash",
        candidates=[
            "z-ai/glm-4.7-flash",
        ],
        fallback_prefix="z-ai/glm-4.7-flash",
    ),
]


def fetch_openrouter_catalog(api_key: str, timeout: int = 8) -> List[dict]:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    response = requests.get(OPENROUTER_MODELS_URL, headers=headers, timeout=timeout)
    response.raise_for_status()
    payload = response.json()
    return payload.get("data", [])


def score_model_id(model_id: str) -> tuple:
    # Stable lexicographic ranking fallback; longer IDs often contain richer version info.
    return (len(model_id), model_id)


def resolve_family(catalog_ids: set, family: ModelFamily) -> Optional[str]:
    for candidate in family.candidates:
        if candidate in catalog_ids:
            return candidate

    if not family.fallback_prefix:
        return None

    matches = [m for m in catalog_ids if m.startswith(family.fallback_prefix)]
    if not matches:
        return None

    return sorted(matches, key=score_model_id, reverse=True)[0]


def resolve_all_families(catalog: List[dict]) -> Dict[str, str]:
    catalog_ids = {m.get("id", "") for m in catalog if m.get("id")}
    resolved: Dict[str, str] = {}

    with ThreadPoolExecutor(max_workers=min(8, len(FAMILIES))) as pool:
        future_map = {pool.submit(resolve_family, catalog_ids, fam): fam for fam in FAMILIES}
        for future in as_completed(future_map):
            family = future_map[future]
            result = future.result()
            if result:
                resolved[family.alias_name] = result
    return resolved


def build_model_list(resolved: Dict[str, str]) -> List[dict]:
    order = [f.alias_name for f in FAMILIES]
    out: List[dict] = []
    for alias_name in order:
        provider_model = resolved.get(alias_name)
        if not provider_model:
            continue
        out.append(
            {
                "model_name": alias_name,
                "litellm_params": {
                    "model": f"openrouter/{provider_model}",
                    "api_key": f"os.environ/{OPENROUTER_API_KEY_ENV}",
                },
            }
        )
    return out


def build_aliases(resolved: Dict[str, str]) -> dict:
    # Keep alias keys stable; map to discovered model_name keys.
    aliases = {
        "default": "claude-sonnet-4-5",
        "claude": "claude-sonnet-4-5",
        "claude-strong": "claude-opus-4-5",
        "reasoning": "deepseek-r1-0528",
        "cheap": "deepseek-v3-2",
        "kimi": "kimi-k2-5",
        "glm": "glm-4-7",
    }
    for key, target in copy.deepcopy(aliases).items():
        if target not in resolved:
            del aliases[key]
    return aliases


def update_config(config_path: Path, model_list: List[dict], aliases: dict, dry_run: bool) -> None:
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with config_path.open("r", encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh) or {}

    cfg["model_list"] = model_list
    cfg.setdefault("router_settings", {})
    cfg["router_settings"]["model_group_alias"] = aliases

    if dry_run:
        print(f"[dry-run] Would write {len(model_list)} models to {config_path}")
        print(f"[dry-run] Aliases: {sorted(aliases.keys())}")
        return

    backup_path = config_path.with_suffix(config_path.suffix + ".bak")
    with config_path.open("r", encoding="utf-8") as src, backup_path.open("w", encoding="utf-8") as dst:
        dst.write(src.read())

    with config_path.open("w", encoding="utf-8") as fh:
        yaml.dump(cfg, fh, sort_keys=False)

    print(f"Updated {config_path} with {len(model_list)} models.")
    print(f"Backup created at {backup_path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Subagent-style curated discovery for OpenRouter models.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Path to config.yaml")
    parser.add_argument("--dry-run", action="store_true", help="Compute and print without writing")
    args = parser.parse_args()

    api_key = os.environ.get(OPENROUTER_API_KEY_ENV)
    if not api_key:
        print(f"Missing required env var: {OPENROUTER_API_KEY_ENV}")
        return 1

    try:
        catalog = fetch_openrouter_catalog(api_key)
        resolved = resolve_all_families(catalog)
        model_list = build_model_list(resolved)
        aliases = build_aliases(resolved)
        update_config(Path(args.config), model_list, aliases, args.dry_run)
        return 0
    except Exception as exc:
        print(f"Discovery failed: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

