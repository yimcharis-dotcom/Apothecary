# Discovery Orchestrator: TUI + LLM-Assisted Discovery

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace the headless `discovery-orchestrator.py` with a TUI-first discovery launcher that:
1. Fetches provider catalogs in parallel
2. Uses parallel LLM calls (one per provider) to identify best model per family — replacing `score_model_id()`
3. Loads **all in-scope models** (not just one per role) into config.yaml
4. Shows a live TUI with discovery progress and an interactive model picker
5. Persists the selected model as the launch default
6. Keeps `--headless` mode for CI/scripted use

**Mid-session switching:** Not needed in TUI — Claude Code's built-in `/model` command works since all models are loaded in the proxy already.

**Base directory:** `C:\Vault\Apothecary\10_Prompt library\20_AI tools\202_GatewayProxy\2020_LiteLLM_ClaudeCode\v0_refactor_1b\202_LiteLLM Refactor v3\`

---

## Context

**Current problems:**
1. `score_model_id()` uses string length to pick "newest" model — fragile, picks wrong models with suffixes like `-beta`/`-preview`
2. `TARGETS` is a static hardcoded list requiring manual updates per new model
3. Only one model per named slot gets loaded — can't switch models mid-session via `/model`
4. Headless only — no visibility into what resolved, no interactive control
5. `cfg["model_list"] = model_list` — full replace, loses entries for skipped providers

**New approach:** No TARGETS/ROLES static list. Instead:
- `FAMILIES` dict maps provider → family prefixes to include (e.g. `anthropic/claude-sonnet`, `deepseek/deepseek-v3`)
- All models matching those prefixes load into config
- LLM call per provider returns `{family_prefix: best_model_id}` — used only for setting the default alias, not for filtering
- TUI surfaces everything live

---

## Task 1: Delete Legacy Scripts

**Files to delete:**
- `scr/discovery.py`
- `scr/discovery-subagents.py`
- `scr/run-subagent-discovery.ps1` (orphaned launcher — references `discovery-subagents.py`)

**Step 1:** Verify references
```powershell
Select-String -Path "scr\*.ps1","scr\*.py" -Pattern "discovery\.py|discovery-subagents"
```
Expected: only `run-subagent-discovery.ps1` references `discovery-subagents.py` (known, being deleted too).

**Step 2:** Delete
```powershell
Remove-Item scr\discovery.py, scr\discovery-subagents.py, scr\run-subagent-discovery.ps1
```

**Step 3:** Commit
```
git add -A && git commit -m "chore: remove legacy discovery scripts and orphaned launcher"
```

---

## Task 2: Rewrite `discovery-orchestrator.py`

**File:** `scr/discovery-orchestrator.py` (full rewrite)
**Dependencies:** `rich`, `questionary` (add to requirements if not present); existing `providers/` unchanged

### Section 1: Imports + Constants

```python
import argparse, copy, json, os
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Optional, Set

import requests, yaml
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
import questionary

from providers import gemini_provider, openrouter_provider, perplexity_provider, xai_provider

console = Console()

DISCOVERY_LLM_MODEL = "deepseek/deepseek-v3"
OPENROUTER_CHAT_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.yaml"
PROFILE_PATH = Path(__file__).resolve().parent.parent / "profile.yaml"
```

### Section 2: PROVIDERS (unchanged structure)

```python
@dataclass(frozen=True)
class ProviderSpec:
    name: str
    api_key_env: str
    discover: Callable[[str, int], List[str]]
    litellm_prefix: str

PROVIDERS: Dict[str, ProviderSpec] = {
    "openrouter": ProviderSpec("openrouter", "OPENROUTER_API_KEY", openrouter_provider.discover, "openrouter/"),
    "xai":        ProviderSpec("xai",        "XAI_API_KEY",        xai_provider.discover,        "xai/"),
    "gemini":     ProviderSpec("gemini",     "GEMINI_API_KEY",     gemini_provider.discover,     "gemini/"),
    "perplexity": ProviderSpec("perplexity", "PERPLEXITY_API_KEY", perplexity_provider.discover, "perplexity/"),
}
```

### Section 3: FAMILIES (replaces TARGETS/ROLES)

```python
# Maps provider_name -> list of family prefixes to include from that catalog.
# All models matching any prefix are loaded. LLM picks best per family for aliasing.
FAMILIES: Dict[str, List[str]] = {
    "openrouter": [
        "anthropic/claude-sonnet",
        "anthropic/claude-opus",
        "deepseek/deepseek-v3",
        "deepseek/deepseek-r1",
        "moonshotai/kimi",
        "z-ai/glm",
    ],
    "xai":        [],   # load all (small catalog)
    "gemini":     [],   # load all (small catalog)
    "perplexity": [],   # load all (small catalog)
}

# Short aliases pointing to the LLM-picked best model per family.
# Keys are alias names; values are family prefixes used to look up the resolved best ID.
ALIAS_TARGETS: Dict[str, tuple] = {
    # alias_name: (provider, family_prefix)
    "default":       ("openrouter", "anthropic/claude-sonnet"),
    "claude":        ("openrouter", "anthropic/claude-sonnet"),
    "claude-strong": ("openrouter", "anthropic/claude-opus"),
    "reasoning":     ("openrouter", "deepseek/deepseek-r1"),
    "cheap":         ("openrouter", "deepseek/deepseek-v3"),
    "kimi":          ("openrouter", "moonshotai/kimi"),
    "glm":           ("openrouter", "z-ai/glm"),
}
```

### Section 4: Family Filtering

```python
def filter_catalog(catalog_ids: Set[str], families: List[str]) -> Set[str]:
    """Return all catalog IDs matching any family prefix. Empty families = all IDs."""
    if not families:
        return set(catalog_ids)
    return {m for m in catalog_ids if any(m.startswith(f) for f in families)}
```

### Section 5: LLM Resolution (best per family)

```python
def resolve_best_per_family(
    provider_name: str,
    filtered_ids: Set[str],
    families: List[str],
    api_key: str,
    timeout: int,
) -> Optional[Dict[str, str]]:
    """
    Ask LLM: given these model IDs and these family prefixes,
    return {family_prefix: best_model_id} for each family.
    Validates response against live catalog — rejects hallucinated IDs.
    """
    if not families:
        return {}  # No aliasing needed for small all-load providers

    catalog_list = "\n".join(sorted(filtered_ids))
    families_list = "\n".join(families)

    system_msg = (
        "You are a model selection assistant. Given a list of available AI model IDs "
        "and a list of family prefixes, return the single best (most capable, most recent) "
        "model ID per family. Only use IDs that appear verbatim in the catalog. "
        "Do not invent, abbreviate, or modify any ID."
    )
    user_msg = (
        f"Provider: {provider_name}\n\n"
        f"Available model IDs:\n{catalog_list}\n\n"
        f"Family prefixes to resolve:\n{families_list}\n\n"
        "Return a JSON object: {\"family_prefix\": \"best_model_id\"}. "
        "Omit families with no good match."
    )

    payload = {
        "model": DISCOVERY_LLM_MODEL,
        "messages": [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0,
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    try:
        resp = requests.post(OPENROUTER_CHAT_URL, json=payload, headers=headers, timeout=timeout)
        resp.raise_for_status()
        raw = json.loads(resp.json()["choices"][0]["message"]["content"])
        # Hallucination guard: only keep IDs that exist in catalog
        validated = {
            family: model_id
            for family, model_id in raw.items()
            if model_id in filtered_ids
        }
        return validated
    except Exception as exc:
        console.print(f"[yellow][warn] LLM resolution failed for {provider_name}: {exc}[/yellow]")
        return None
```

### Section 6: Config Merge Helpers

```python
def build_entries_for_provider(
    filtered_ids: Set[str],
    provider: ProviderSpec,
) -> List[dict]:
    """One config entry per filtered model ID."""
    return [
        {
            "model_name": model_id.replace("/", "-"),
            "litellm_params": {
                "model": f"{provider.litellm_prefix}{model_id}",
                "api_key": f"os.environ/{provider.api_key_env}",
            },
        }
        for model_id in sorted(filtered_ids)
    ]


def build_aliases(
    new_entries_by_provider: Dict[str, List[dict]],
    best_by_family: Dict[str, Dict[str, str]],  # provider -> {family: best_id}
) -> dict:
    available_names = {
        e["model_name"]
        for entries in new_entries_by_provider.values()
        for e in entries
    }
    aliases = {}
    for alias, (provider, family_prefix) in ALIAS_TARGETS.items():
        best_id = (best_by_family.get(provider) or {}).get(family_prefix)
        if best_id:
            model_name = best_id.replace("/", "-")
            if model_name in available_names:
                aliases[alias] = model_name
    return aliases


def group_existing_by_provider(model_list: List[dict]) -> Dict[str, List[dict]]:
    """Preserve existing entries for providers not updated this run."""
    rev = {spec.api_key_env: name for name, spec in PROVIDERS.items()}
    groups: Dict[str, List[dict]] = {name: [] for name in PROVIDERS}
    groups["__unknown__"] = []
    for entry in model_list:
        raw_key = entry.get("litellm_params", {}).get("api_key", "")
        env_var = raw_key.replace("os.environ/", "")
        groups[rev.get(env_var, "__unknown__")].append(entry)
    return groups


def merge_model_list(
    existing: List[dict],
    new_entries_by_provider: Dict[str, List[dict]],
) -> List[dict]:
    existing_groups = group_existing_by_provider(existing)
    result = []
    for provider_name in PROVIDERS:
        if provider_name in new_entries_by_provider:
            result.extend(new_entries_by_provider[provider_name])
        else:
            result.extend(existing_groups.get(provider_name, []))
    result.extend(existing_groups.get("__unknown__", []))
    return result
```

### Section 7: Catalog Fetch (parallel, unchanged logic)

```python
def fetch_provider_catalogs(timeout: int, progress=None) -> Dict[str, Set[str]]:
    catalogs: Dict[str, Set[str]] = {}
    futures = {}
    tasks = {}
    with ThreadPoolExecutor(max_workers=len(PROVIDERS)) as pool:
        for name, provider in PROVIDERS.items():
            api_key = os.environ.get(provider.api_key_env)
            if not api_key:
                if progress:
                    progress.console.print(f"[dim][skip] {name}: missing {provider.api_key_env}[/dim]")
                continue
            if progress:
                tasks[name] = progress.add_task(f"[cyan]{name}[/cyan] fetching...", total=None)
            futures[pool.submit(provider.discover, api_key, timeout)] = name
        for future in as_completed(futures):
            name = futures[future]
            try:
                discovered = future.result()
                catalogs[name] = {m for m in discovered if m}
                if progress and name in tasks:
                    progress.update(tasks[name], description=f"[green]{name}[/green] {len(catalogs[name])} models", completed=1, total=1)
            except Exception as exc:
                if progress and name in tasks:
                    progress.update(tasks[name], description=f"[red]{name}[/red] failed: {exc}", completed=1, total=1)
    return catalogs
```

### Section 8: Config Write

```python
def update_config(
    config_path: Path,
    new_entries_by_provider: Dict[str, List[dict]],
    aliases: dict,
    dry_run: bool,
) -> None:
    if not config_path.exists():
        raise FileNotFoundError(f"Config not found: {config_path}")
    with config_path.open("r", encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh) or {}

    existing = cfg.get("model_list", [])
    merged = merge_model_list(existing, new_entries_by_provider)

    if dry_run:
        console.print(f"[dim][dry-run] Would write {len(merged)} models[/dim]")
        console.print(yaml.dump({"model_list": merged, "aliases": aliases}, sort_keys=False))
        return

    backup_path = config_path.with_suffix(config_path.suffix + ".bak")
    backup_path.write_text(config_path.read_text(encoding="utf-8"), encoding="utf-8")

    cfg["model_list"] = merged
    cfg.setdefault("router_settings", {})
    cfg["router_settings"]["model_group_alias"] = aliases
    with config_path.open("w", encoding="utf-8") as fh:
        yaml.dump(cfg, fh, sort_keys=False)

    console.print(f"[green]Updated {config_path} — {len(merged)} models, {len(aliases)} aliases[/green]")
```

### Section 9: Profile (persist selected launch model)

```python
def load_profile() -> dict:
    if PROFILE_PATH.exists():
        return yaml.safe_load(PROFILE_PATH.read_text(encoding="utf-8")) or {}
    return {}

def save_profile(data: dict) -> None:
    existing = load_profile()
    existing.update(data)
    PROFILE_PATH.write_text(yaml.dump(existing, sort_keys=False), encoding="utf-8")
```

`profile.yaml` stores:
```yaml
default_model: claude-sonnet-4-5   # last picked model name (model_name key in config)
```

### Section 10: TUI + `main()`

```python
def run_tui(
    config_path: Path,
    timeout: int,
    dry_run: bool,
) -> int:
    console.rule("[bold cyan]LiteLLM Discovery[/bold cyan]")

    openrouter_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not openrouter_key:
        console.print("[red][error] OPENROUTER_API_KEY required for LLM resolution[/red]")
        return 1

    # Phase 1: Fetch catalogs (with live progress)
    with Progress(SpinnerColumn(), TextColumn("{task.description}"), console=console) as progress:
        catalogs = fetch_provider_catalogs(timeout, progress)

    # Phase 2: Filter catalogs to in-scope families
    filtered: Dict[str, Set[str]] = {
        name: filter_catalog(ids, FAMILIES.get(name, []))
        for name, ids in catalogs.items()
    }

    # Phase 3: Parallel LLM resolution (best per family, for aliasing)
    best_by_family: Dict[str, Dict[str, str]] = {}
    llm_futures = {}
    with ThreadPoolExecutor(max_workers=len(filtered)) as pool:
        for name, ids in filtered.items():
            families = FAMILIES.get(name, [])
            if families and ids:
                llm_futures[pool.submit(
                    resolve_best_per_family, name, ids, families, openrouter_key, timeout
                )] = name
        with Progress(SpinnerColumn(), TextColumn("{task.description}"), console=console) as progress:
            tasks = {name: progress.add_task(f"[cyan]{name}[/cyan] resolving...", total=None) for name in llm_futures.values()}
            for future in as_completed(llm_futures):
                name = llm_futures[future]
                result = future.result()
                best_by_family[name] = result or {}
                desc = f"[green]{name}[/green] resolved {len(best_by_family[name])} families" if result else f"[yellow]{name}[/yellow] LLM failed (existing preserved)"
                progress.update(tasks[name], description=desc, completed=1, total=1)

    # Phase 4: Build config entries
    new_entries_by_provider = {
        name: build_entries_for_provider(ids, PROVIDERS[name])
        for name, ids in filtered.items()
        if ids
    }
    aliases = build_aliases(new_entries_by_provider, best_by_family)

    # Phase 5: Show summary table
    table = Table(title="Discovered Models", show_lines=True)
    table.add_column("Provider", style="cyan")
    table.add_column("Models loaded")
    table.add_column("Best (aliased)")
    for name, entries in new_entries_by_provider.items():
        bests = best_by_family.get(name, {})
        best_str = "\n".join(f"{f}: {m}" for f, m in bests.items()) or "—"
        table.add_row(name, str(len(entries)), best_str)
    console.print(table)

    # Phase 6: Interactive model picker (skip in headless/dry-run)
    all_model_names = [e["model_name"] for entries in new_entries_by_provider.values() for e in entries]
    profile = load_profile()
    default_model = profile.get("default_model", aliases.get("default", all_model_names[0] if all_model_names else None))

    selected_model = default_model
    if not dry_run and all_model_names:
        selected_model = questionary.select(
            "Select launch model for Claude Code:",
            choices=all_model_names,
            default=default_model if default_model in all_model_names else None,
        ).ask()
        if selected_model:
            aliases["default"] = selected_model
            aliases["claude"] = selected_model
            save_profile({"default_model": selected_model})
            console.print(f"[green]Launch model set to: {selected_model}[/green]")

    # Phase 7: Write config
    update_config(config_path, new_entries_by_provider, aliases, dry_run)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="LiteLLM discovery with TUI.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH))
    parser.add_argument("--timeout", type=int, default=8)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--headless", action="store_true", help="Skip TUI picker, use profile default")
    args = parser.parse_args()

    if args.headless:
        args_dry_run = args.dry_run
        # Run without interactive picker
        return run_tui(Path(args.config), args.timeout, dry_run=True if args_dry_run else False)

    return run_tui(Path(args.config), args.timeout, args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
```

**Step:** Write all sections as one combined file.

**Step:** Commit
```
git add scr/discovery-orchestrator.py
git commit -m "feat: TUI discovery with parallel LLM resolution, all in-scope models, profile-based launch model"
```

---

## Task 3: Update `run-orchestrator-discovery.ps1`

Add `--headless` passthrough flag:
```powershell
if ($Headless) { $argsList += "--headless" }
```

Commit: `"chore: add --headless flag to run-orchestrator-discovery.ps1"`

---

## Dependencies

Check if `rich` and `questionary` are available:
```powershell
python -c "import rich, questionary" 2>&1
```
If missing: `pip install rich questionary`

---

## Verification

**1. Dry-run**
```powershell
. .\scr\set-env.ps1
python scr/discovery-orchestrator.py --dry-run
```
Expected: progress spinners, summary table, no file written.

**2. Headless (CI simulation)**
```powershell
python scr/discovery-orchestrator.py --headless
```
Expected: no interactive prompt, writes config using profile default model.

**3. Interactive run**
```powershell
python scr/discovery-orchestrator.py
```
Expected: TUI shows, model picker appears, selection saved to `profile.yaml`.

**4. Verify config structure**
```powershell
python -c "import yaml; cfg=yaml.safe_load(open('config.yaml')); print(list(cfg.keys())); print(len(cfg['model_list']), 'models')"
```

**5. Smoke test routing**
```powershell
.\scr\test-claude-code.ps1 -Model claude -Prompt "Reply with exactly: OK"
```
Expected: `OK`

---

## Rollback

- Config: `Copy-Item config.yaml.bak config.yaml`
- Code: `git revert HEAD`
- LLM failure at runtime: providers with failed LLM resolution fall back to existing config entries automatically
