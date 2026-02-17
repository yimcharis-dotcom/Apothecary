import os
import requests
import yaml
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print
import sys

# Configuration
CONFIG_PATH = r"C:\Users\YC\LiteLLM\litellm-config\config.yaml"
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

console = Console()

def fetch_openrouter_models():
    """Fetch available models from OpenRouter, filtering for Anthropic."""
    if not OPENROUTER_API_KEY:
        console.print("[yellow]Warning: OPENROUTER_API_KEY not found. Skipping OpenRouter discovery.[/yellow]")
        return []

    url = "https://openrouter.ai/api/v1/models"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        models = []
        for model in data.get("data", []):
            model_id = model.get("id", "")
            # Filter for Anthropic models as requested
            if "anthropic" in model_id.lower():
                 models.append({
                    "model_name": model_id.split("/")[-1], 
                    "litellm_params": {
                        "model": f"openrouter/{model_id}",
                        "api_key": "os.environ/OPENROUTER_API_KEY"
                    }
                })
        
        return models

    except Exception as e:
        console.print(f"[red]Error fetching OpenRouter models: {e}[/red]")
        return []

def update_config(discovered_models):
    """Update the config.yaml file with discovered models."""
    if not os.path.exists(CONFIG_PATH):
        console.print(f"[red]Config file not found at {CONFIG_PATH}[/red]")
        return

    try:
        with open(CONFIG_PATH, 'r') as file:
            config = yaml.safe_load(file)
        
        if config is None:
            config = {}
        
        if "model_list" not in config:
            config["model_list"] = []
        
        existing_models = {m.get("model_name") for m in config["model_list"] if "model_name" in m}
        
        added_count = 0
        for model in discovered_models:
            if model["model_name"] not in existing_models:
                config["model_list"].append(model)
                added_count += 1
        
        # Backup existing config
        backup_path = CONFIG_PATH + ".bak"
        with open(CONFIG_PATH, 'r') as src, open(backup_path, 'w') as dst:
            dst.write(src.read())
            
        # Write new config
        with open(CONFIG_PATH, 'w') as file:
            yaml.dump(config, file, sort_keys=False)
            
        console.print(f"[green]Successfully updated config. Added {added_count} new models.[/green]")

    except Exception as e:
        console.print(f"[red]Error updating config: {e}[/red]")

def main():
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task(description="Discovering models...", total=None)
        openrouter_models = fetch_openrouter_models()
        update_config(openrouter_models)

if __name__ == "__main__":
    main()
