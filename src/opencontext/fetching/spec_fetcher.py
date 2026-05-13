from pathlib import Path
import json
import os

def get_all_specs_markdown(target_directory="openspec/specs"):
    """Reads all .md files in the target directory."""
    dir_path = Path(target_directory)
    if not dir_path.exists() or not dir_path.is_dir():
        return f"Error: The directory '{target_directory}' does not exist."

    combined_markdown = []
    for file_path in dir_path.rglob("*.md"):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                combined_markdown.append(f"--- FILE: {file_path} ---\n{file.read()}\n")
        except Exception as e:
            print(f"Failed to read {file_path}: {e}")

    return "".join(combined_markdown)

def create_antigravity_task(data):
    """
    Creates a Task file for Antigravity IDE pointing to the ./sdlc folder.
    """
    
    # 1. Update the prompt to tell the Agent to save inside ./sdlc
    task_content = f"""# .agent/tasks/extract_architecture.md

## Role
You are a specialized System Architect.

## Context (Architectural Specs)
{data}

## Objective
Extract all "architectural facts" from the context above.

## Architectural Fact Definition
- System boundaries, core components, and responsibilities.
- Technology stack choices (languages, frameworks, databases).
- Data models and flow paths.
- APIs and communication protocols.
- Non-functional constraints (security, scaling).
- Design patterns.

## Output Format
Return the facts STRICTLY as a valid JSON array of strings.
Save the file at: `./sdlc/architectural_facts.json`
Do not include any other text.
"""

    # 2. Ensure both the task directory and the target sdlc directory exist
    os.makedirs(".agent/tasks", exist_ok=True)
    os.makedirs("sdlc", exist_ok=True) 
    
    task_path = ".agent/tasks/extract_architecture.md"
    with open(task_path, "w", encoding="utf-8") as f:
        f.write(task_content)
    
    return task_path

# if __name__ == "__main__":
#     print("🔍 Reading local specifications...")
#     data = get_all_specs_markdown()
    
#     if not data.startswith("Error"):
#         print("🛠️ Generating Antigravity Agent Task...")
#         path = create_antigravity_task(data)
        
#         print("-" * 30)
#         print(f"✅ Task created at: {path}")
#         print("📁 Output directory initialized: ./sdlc")
#         print("🚀 NEXT STEP: Open Antigravity IDE and type: run extract_architecture")
#         print("-" * 30)
#     else:
#         print(data)