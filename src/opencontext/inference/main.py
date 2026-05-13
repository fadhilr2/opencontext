import opencontext.pipeline.vectorizer as v

import os

def create_agent_md_task(feature_question):
    """
    Creates a Task file for Antigravity IDE to generate a feature-specific agent.md.
    Forces the IDE Agent to respect architectural constraints found in RAG data.
    """
    # Assuming 'v' is your context/vector provider defined in your scope
    context = v.retrieve_context(feature_question)    
    
    task_content = f"""# .agent/tasks/generate_agent.md

## Role
You are the **Lead Agent Architect**. Your goal is to synthesize a sub-agent configuration (`agent.md`) that is perfectly aligned with our system's existing architecture.

## Feature Request
{feature_question}

## Input: Architectural Context (RAG)
{context}

## Objective
Generate a new `agent.md` file. This agent will be the dedicated specialist responsible for implementing the **Feature Request** listed above.

## Constraints (Antigravity Skill)
1. **Zero Drift**: The generated agent must NOT suggest libraries, patterns, or file structures that contradict the "Architectural Context" provided. 
2. **Contextual Anchoring**: Explicitly forbid the agent from using technologies that compete with the current stack (e.g., if Context is Tailwind, forbid Bootstrap).
3. **Implicit Knowledge**: Extract naming conventions, error handling styles, and directory patterns from the RAG context and bake them into the agent's "Rules" section.

## Required Output Format
You must output the `agent.md` file using the structure below. Do not provide a preamble, chatty introduction, or summary.

- **Persona**: The mindset and technical specialty of the sub-agent.
- **Rules of Engagement**: Strict "Do's and Don'ts" based on the RAG context.
- **Architectural Guardrails**: Hard constraints extracted from the system state.
- **Definition of Done**: Success criteria specific to the feature.

Write the output directly to the project root as './agent.md'.
"""

    # Ensure the Antigravity task directory exists
    os.makedirs(".agent/tasks", exist_ok=True)
    
    task_path = ".agent/tasks/generate_agent.md"
    with open(task_path, "w", encoding="utf-8") as f:
        f.write(task_content)
    
    return task_path
