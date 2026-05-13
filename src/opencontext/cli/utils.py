from opencontext.pipeline.vectorizer import process_string_to_vector
from opencontext.fetching.spec_fetcher import get_all_specs_markdown, create_antigravity_task
from pathlib import Path
import subprocess
import json
from opencontext.fetching.jira_retriever import format_ticket_for_vectorization, fetch_jira_ticket
import questionary

def fetch_jira():
    global_config = read_global_config()
    local_config = read_local_config()
    ticket = fetch_jira_ticket(local_config["jira_domain"], global_config["jira_token"], global_config["jira_email"], get_branch_ticket())
    formatted = format_ticket_for_vectorization(ticket)
    return formatted

def fetch_spec():
    # mengambil data dari openspec (asumsi openspec dijalankan sebelum opencontext init)
    Path("sdlc").mkdir(exist_ok=True)
    data = get_all_specs_markdown()
    path = create_antigravity_task(data)
    
    # run extract_architecture fact

    # mengubah data spec menjadi vector

# TODO: validasi ke fadiil
def read_json():
    with open("sdlc/architectural_facts.json", "r") as f:
        data = json.load(f)
        
    return data

def _global_config_path() -> Path:
    config_dir = Path.home() / ".opencontext"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "global.config.json"

def read_global_config():
    config_path = _global_config_path()
    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def write_global_config(data):
    config_path = _global_config_path()
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def read_local_config():
    with open("opencontext.config.json", "r") as f:
        data = json.load(f)
    return data

def write_local_config(data):
    with open("opencontext.config.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def get_branch_ticket() -> str:
    try:
        branch = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            check=True
        )

        branchStrip = branch.stdout.strip()

        if(branchStrip == "main"):
            return branchStrip

        result = "-".join(branchStrip.split("-")[:2]) 
        return result
    except Exception as e:
        print(f"Error getting git branch: {e}")
        return ""