import os
import stat
import json
from pathlib import Path

import typer
import questionary
from opencontext.inference.main import create_agent_md_task
from opencontext.cli.utils import fetch_jira, fetch_spec, write_local_config, write_global_config, read_json
from opencontext.pipeline.vectorizer import process_string_to_vector

app = typer.Typer()

@app.command()
def setup():
    print("hello")
    # setup = memuat setting akun pengguna

    jira_email = questionary.text("Jira Email:").ask()
    jira_token = questionary.text("Jira API Token:").ask()

    config_data = {
        "jira_email": jira_email,
        "jira_token": jira_token
    }

    # membuat global config file yang dapat diakses dimanapun CLI dijalankan
    write_global_config(config_data)
    print("Global Config Set")

    # --- Generate Git Hook ---
    git_hook_dir = Path(".git/hooks")
    if git_hook_dir.exists():
        hook_path = git_hook_dir / "pre-commit"  # You can change this to 'post-commit' if preferred
        hook_content = "#!/bin/bash\n\npython3 fetching/git_diff.py"
        
        with open(hook_path, "w") as f:
            f.write(hook_content)
        
        # Make the hook executable (chmod +x)
        st = os.stat(hook_path)
        os.chmod(hook_path, st.st_mode | stat.S_IEXEC)
        print(f"Git hook generated at {hook_path}")
    else:
        print("Warning: .git directory not found. Git hook was not generated.")
    # -------------------------

@app.command()
def init():
    # init = memuat identitas projek jira
    jira_domain = questionary.text("Jira Domain:").ask()

    local_config_data = {
        "jira_domain": jira_domain,
    }
    
    # membuat config file khusus untuk projek tempat CLI dijalankan
    write_local_config(local_config_data)


    print(f"Local Config Set")
    print("execute the following command in chatbot")
    print("run extract_architecture ")

    # mengambil data spec dari openspec
    fetch_spec()

@app.command()
def initbranch():
    #sentence transformer
    # initbranch = dijalankan setelah git branch
    data = read_json()
    for v in data:
        process_string_to_vector(v)
    print("V  E  C  T  O  R   E  D")

    jira = fetch_jira()
    generated_task_path = create_agent_md_task(jira)
    print("Execute the following command in chatbot")
    print("run generate_agent")

@app.command()
def sync():
    with open("sdlc/diff_analysis.json", "r") as f:
        data = json.load(f)
    for v in data:
        process_string_to_vector(v)
    print("V  E  C  T  O  R   E  D")
    jira = fetch_jira()
    generated_task_path = create_agent_md_task(jira)
    print("Execute the following command in chatbot")
    print("run generate_agent")

if __name__ == "__main__":
    app()
