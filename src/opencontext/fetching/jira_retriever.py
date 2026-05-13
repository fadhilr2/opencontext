import os
import json
import requests
from typing import Dict, Any, Optional

def fetch_jira_ticket(domain: str, api_token: str, email: str, issue_key: str) -> Optional[Dict[str, Any]]:
    """
    Fetches a Jira ticket from the REST API v3 using provided credentials.
    
    Args:
        domain: The Jira instance subdomain (e.g., 'your-company').
        api_token: Atlassian API token.
        email: User email associated with the API token.
        issue_key: The ticket key (e.g., 'PROJ-123').
    """
    # The base URL should just be the domain
    base_url = f"https://{domain}.atlassian.net"
    
    # Specific fields to request to minimize payload size
    fields = "summary,description,issuetype,components,priority,labels,comment,issuelinks"
    endpoint = f"{base_url}/rest/api/3/issue/{issue_key}?fields={fields}"

    try:
        response = requests.get(
            endpoint,
            auth=(email, api_token),
            headers={"Accept": "application/json"}
        )
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Jira ticket {issue_key}: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response Body: {e.response.text}")
        return None

def _extract_text_from_adf(adf_content: Any) -> str:
    """
    Helper function to extract plain text from Atlassian Document Format (ADF)
    used in Jira REST API v3 for description and comments.
    """
    if not adf_content or not isinstance(adf_content, dict):
        return str(adf_content) if adf_content else ""
    
    texts = []
    
    def traverse(node):
        if not isinstance(node, dict):
            return
        if node.get("type") == "text" and "text" in node:
            texts.append(node["text"])
        
        for item in node.get("content", []):
            traverse(item)
            
    traverse(adf_content)
    return " ".join(texts).strip()

def format_ticket_for_vectorization(ticket_json: Dict[str, Any]) -> str:
    """
    Formats the Jira ticket JSON into a clean, structured Markdown string 
    optimized for vector embeddings.
    """
    if not ticket_json or "fields" not in ticket_json:
        return "Error: Invalid ticket JSON format."

    key = ticket_json.get("key", "Unknown Key")
    fields = ticket_json.get("fields", {})

    # Extract fields with safe defaults
    summary = fields.get("summary") or "No Summary"
    
    issuetype_data = fields.get("issuetype") or {}
    issuetype = issuetype_data.get("name", "Unknown Type")
    
    priority_data = fields.get("priority") or {}
    priority = priority_data.get("name", "Unknown Priority")
    
    # Handle ADF format for description
    description_raw = fields.get("description")
    description = _extract_text_from_adf(description_raw) if description_raw else "No Description"

    # Components
    components_raw = fields.get("components", [])
    components = [c.get("name") for c in components_raw if c.get("name")]
    components_str = ", ".join(components) if components else "None"

    # Labels
    labels_raw = fields.get("labels", [])
    labels_str = ", ".join(labels_raw) if labels_raw else "None"

    # Comments (ADF format)
    comments_data = fields.get("comment", {}).get("comments", [])
    formatted_comments = []
    for idx, c in enumerate(comments_data):
        author = c.get("author", {}).get("displayName", "Unknown Author")
        created = c.get("created", "")
        body_raw = c.get("body")
        body_text = _extract_text_from_adf(body_raw) if body_raw else ""
        if body_text:
            formatted_comments.append(f"Comment {idx + 1} by {author} ({created}): {body_text}")
    
    comments_str = "\n".join(formatted_comments) if formatted_comments else "No Comments"

    # Issue Links
    issuelinks_data = fields.get("issuelinks", [])
    formatted_links = []
    for link in issuelinks_data:
        link_type = link.get("type", {}).get("name", "Related")
        
        if "outwardIssue" in link:
            out_key = link["outwardIssue"].get("key")
            outward_desc = link.get("type", {}).get("outward", "relates to")
            formatted_links.append(f"This issue {outward_desc} {out_key}")
            
        if "inwardIssue" in link:
            in_key = link["inwardIssue"].get("key")
            inward_desc = link.get("type", {}).get("inward", "is related to")
            formatted_links.append(f"This issue {inward_desc} {in_key}")
            
    issuelinks_str = "\n".join(formatted_links) if formatted_links else "No Linked Issues"

    # Construct the Markdown string
    formatted_output = f"""# Jira Ticket: {key}
## Summary: {summary}

**Issue Type:** {issuetype}
**Priority:** {priority}
**Components:** {components_str}
**Labels:** {labels_str}

## Description
{description}

## Comments
{comments_str}

## Issue Links
{issuelinks_str}
"""
    return formatted_output