import subprocess
import os
from pathlib import Path
from typing import Optional

def get_staged_diff() -> Optional[str]:
    """
    Captures staged changes using 'git diff --staged'.
    """
    try:
        diff_output = subprocess.check_output(
            ["git", "diff", "--staged", "--no-color"],
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8"
        )
        return diff_output.strip() or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

def generate_agent_prompt(diff_text: str) -> str:
    """
    Formats the prompt and diff into a Markdown string for manual chatbot use.
    """
    prompt = (f"""
## Role
You are a specialized Principal Software Engineer.

## Context (Git Diff)
{diff_text}

## Objective
Extract all critical "diff insights" from the code changes above.

## Diff Insight Definition
- Core logic modifications and behavioral changes (what was actually altered).
- Added, removed, or updated dependencies and imports.
- Structural refactoring, scope changes, or function signature alterations.
- Potential regressions, unhandled edge cases, or security vulnerabilities introduced.
- Performance implications (new bottlenecks or optimizations).
- New architectural constraints or logic boundaries.

## Output Format
Return the insights STRICTLY as a valid JSON array of strings.
Save the file at: `./sdlc/diff_analysis.json`
Do not include any other text.
""")
    return prompt

def save_to_agent_folder(content: str, filename: str = "diff_analysis_prompt.md"):
    """
    Appends the prompt into ./.agent/tasks/ folder as a Markdown file.
    """
    output_path = Path("./.agent/tasks/")
    output_path.mkdir(parents=True, exist_ok=True)
    target_file = output_path / filename

    # Check if file exists to determine if we need a separator
    file_exists = target_file.exists()

    # Changed "w" to "a" to append content
    with open(target_file, "a", encoding="utf-8") as f:
        if file_exists:
            # Add a separator if appending to an existing file
            f.write("\n\n---\n\n")
        f.write(content)
    
    print(f"Success! Agent prompt appended to: {target_file}")
    print("You can now pass this file's contents to an agent with file-writing capabilities.")

if __name__ == "__main__":
    diff = get_staged_diff()
    if diff:
        prompt_content = generate_agent_prompt(diff)
        save_to_agent_folder(prompt_content)
    else:
        print("No staged changes to process.")