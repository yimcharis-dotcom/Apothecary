import argparse
import copy
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Optional, Set

import yaml

from providers import gemini_provider, openrouter_provider, perplexity_provider, xai_provider


@dataclass(frozen=True)
class ProviderSpec:
    name: str
    api_key_env: str
    discover: Callable[[str, int], List[str]]
    litellm_prefix: str


@dataclass(frozen=True)
class ModelTarget:
    model_name: str
    provider: str
    candidates: List[str]
    fallback_prefixes: List[str]


PROVIDERS: Dict[str, ProviderSpec] = {
    "openrouter": ProviderSpec(
        name="openrouter",
        api_key_env="OPENROUTER_API_KEY",
        discover=openrouter_provider.discover,
        litellm_prefix="openrouter/",
    ),
    "xai": ProviderSpec(
        name="xai",
        api_key_env="XAI_API_KEY",
        discover=xai_provider.discover,
        litellm_prefix="xai/",
    ),
    "gemini": ProviderSpec(
        name="gemini",
        api_key_env="GEMINI_API_KEY",
        discover=gemini_provider.discover,
        litellm_prefix="gemini/",
    ),
    "perplexity": ProviderSpec(
        name="perplexity",
        api_key_env="PERPLEXITY_API_KEY",
        discover=perplexity_provider.discover,
        litellm_prefix="perplexity/",
    ),
}

TARGETS: List[ModelTarget] = [
    ModelTarget(
        model_name="claude-sonnet-4-5",
        provider="openrouter",
        candidates=["anthropic/claude-sonnet-4.5", "anthropic/claude-sonnet-4"],
        fallback_prefixes=["anthropic/claude-sonnet-"],
    ),
    ModelTarget(
        model_name="claude-opus-4-5",
        provider="openrouter",
        candidates=["anthropic/claude-opus-4.5", "anthropic/claude-opus-4"],
        fallback_prefixes=["anthropic/claude-opus-"],
    ),
    ModelTarget(
        model_name="deepseek-v3-2",
        provider="openrouter",
        candidates=["deepseek/deepseek-v3.2", "deepseek/deepseek-v3.1", "deepseek/deepseek-v3"],
        fallback_prefixes=["deepseek/deepseek-v3"],
    ),
    ModelTarget(
        model_name="deepseek-r1-0528",
        provider="openrouter",
        candidates=["deepseek/deepseek-r1-0528", "deepseek/deepseek-r1"],
        fallback_prefixes=["deepseek/deepseek-r1"],
    ),
    ModelTarget(
        model_name="kimi-k2-5",
        provider="openrouter",
        candidates=["moonshotai/kimi-k2.5", "moonshotai/kimi-k2"],
        fallback_prefixes=["moonshotai/kimi-"],
    ),
    ModelTarget(
        model_name="glm-5",
        provider="openrouter",
        candidates=["z-ai/glm-5"],
        fallback_prefixes=["z-ai/glm-5"],
    ),
    ModelTarget(
        model_name="glm-4-7",
        provider="openrouter",
        candidates=["z-ai/glm-4.7"],
        fallback_prefixes=["z-ai/glm-4.7"],
    ),
    ModelTarget(
        model_name="glm-4-7-flash",
        provider="openrouter",
        candidates=["z-ai/glm-4.7-flash"],
        fallback_prefixes=["z-ai/glm-4.7-flash"],
    ),
    ModelTarget(
        model_name="xai-grok-4-1-fast-reasoning",
        provider="xai",
        candidates=["grok-4-1-fast-reasoning", "grok-4-fast-reasoning"],
        fallback_prefixes=["grok-4-"],
    ),
    ModelTarget(
        model_name="xai-grok-code-fast-1",
        provider="xai",
        candidates=["grok-code-fast-1"],
        fallback_prefixes=["grok-code-"],
    ),
    ModelTarget(
        model_name="gemini-2-5-pro",
        provider="gemini",
        candidates=["gemini-2.5-pro", "gemini-2.5-pro-latest"],
        fallback_prefixes=["gemini-2.5-pro"],
    ),
    ModelTarget(
        model_name="gemini-2-5-flash",
        provider="gemini",
        candidates=["gemini-2.5-flash", "gemini-2.5-flash-latest"],
        fallback_prefixes=["gemini-2.5-flash"],
    ),
    ModelTarget(
        model_name="perplexity-sonar",
        provider="perplexity",
        candidates=["sonar"],
        fallback_prefixes=["sonar"],
    ),
    ModelTarget(
        model_name="perplexity-sonar-pro",
        provider="perplexity",
        candidates=["sonar-pro"],
        fallback_prefixes=["sonar-pro"],
    ),
    ModelTarget(
        model_name="perplexity-sonar-reasoning-pro",
        provider="perplexity",
        candidates=["sonar-reasoning-pro"],
        fallback_prefixes=["sonar-reasoning"],
    ),
]

DEFAULT_ALIASES = {
    "default": "claude-sonnet-4-5",
    "claude": "claude-sonnet-4-5",
    "claude-strong": "claude-opus-4-5",
    "reasoning": "deepseek-r1-0528",
    "cheap": "deepseek-v3-2",
    "kimi": "kimi-k2-5",
    "glm": "glm-4-7",
}

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.yaml"


def score_model_id(model_id: str) -> tuple:
    return (len(model_id), model_id)


def resolve_target(available_ids: Set[str], target: ModelTarget) -> Optional[str]:
    for candidate in target.candidates:
        if candidate in available_ids:
            return candidate

    for prefix in target.fallback_prefixes:
        matches = [m for m in available_ids if m.startswith(prefix)]
        if matches:
            return sorted(matches, key=score_model_id, reverse=True)[0]
    return None


def fetch_provider_catalogs(timeout: int) -> Dict[str, Set[str]]:
    catalogs: Dict[str, Set[str]] = {}
    futures = {}

    with ThreadPoolExecutor(max_workers=len(PROVIDERS)) as pool:
        for provider_name, provider in PROVIDERS.items():
            api_key = os.environ.get(provider.api_key_env)
            if not api_key:
                print(f"[skip] {provider_name}: missing {provider.api_key_env}")
                continue
            futures[pool.submit(provider.discover, api_key, timeout)] = provider_name

        for future in as_completed(futures):
            provider_name = futures[future]
            try:
                discovered = future.result()
                catalogs[provider_name] = {m for m in discovered if m}
                print(f"[ok] {provider_name}: discovered {len(catalogs[provider_name])} models")
            except Exception as exc:
                print(f"[warn] {provider_name}: discovery failed ({exc})")

    return catalogs


def build_model_list(catalogs: Dict[str, Set[str]]) -> List[dict]:
    result: List[dict] = []
    for target in TARGETS:
        ids = catalogs.get(target.provider, set())
        if not ids:
            continue
        resolved = resolve_target(ids, target)
        if not resolved:
            continue

        provider = PROVIDERS[target.provider]
        result.append(
            {
                "model_name": target.model_name,
                "litellm_params": {
                    "model": f"{provider.litellm_prefix}{resolved}",
                    "api_key": f"os.environ/{provider.api_key_env}",
                },
            }
        )
    return result


def build_aliases(model_list: List[dict]) -> dict:
    available = {m["model_name"] for m in model_list}
    aliases = copy.deepcopy(DEFAULT_ALIASES)
    for alias, target in copy.deepcopy(aliases).items():
        if target not in available:
            del aliases[alias]
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
    parser = argparse.ArgumentParser(description="Multi-provider discovery orchestrator.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Path to config.yaml")
    parser.add_argument("--timeout", type=int, default=8, help="Provider request timeout seconds")
    parser.add_argument("--dry-run", action="store_true", help="Compute and print without writing")
    args = parser.parse_args()

    try:
        catalogs = fetch_provider_catalogs(timeout=args.timeout)
        model_list = build_model_list(catalogs)
        aliases = build_aliases(model_list)
        update_config(Path(args.config), model_list, aliases, args.dry_run)
        return 0
    except Exception as exc:
        print(f"Orchestrator failed: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

