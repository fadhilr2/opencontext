# OpenContext

pip install opencontext-refactory-hackathon

CLI tool for architectural context tracking and agent task generation.

## Installation

```bash
pip install -e .
```

## Usage

```bash
# First-time global setup (Jira credentials + git hook)
opencontext setup

# Initialize a project (Jira domain + spec extraction)
opencontext init

# Initialize branch context (vectorize + generate agent task)
opencontext initbranch

# Sync diff analysis and regenerate agent task
opencontext sync
```

## Development

```bash
# Install in editable mode
pip install -e .

# Run directly
python -m opencontext.cli.main
```
