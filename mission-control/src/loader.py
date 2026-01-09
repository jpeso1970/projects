"""
Project loader - discovers and parses PROJECT.md files.
"""
import re
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import date

from .models import Project
from .utils.date_utils import parse_date


def discover_projects(root_dir: Path, exclude_patterns: Optional[List[str]] = None) -> List[Path]:
    """
    Discover all PROJECT.md files under root_dir.

    Args:
        root_dir: Root directory to search (e.g., ~/projects)
        exclude_patterns: List of directory names to exclude (e.g., [".templates", "_archived"])

    Returns:
        List of Path objects pointing to PROJECT.md files
    """
    if exclude_patterns is None:
        exclude_patterns = [".templates", "_archived", ".git", ".agents", ".docs"]

    project_files = []

    # Use glob to find all PROJECT.md files
    for project_file in root_dir.rglob("PROJECT.md"):
        # Check if any excluded pattern is in the path
        if any(pattern in str(project_file) for pattern in exclude_patterns):
            continue

        project_files.append(project_file)

    return sorted(project_files)


def extract_yaml_frontmatter(content: str) -> Optional[str]:
    """
    Extract YAML frontmatter from PROJECT.md content.

    YAML frontmatter is between two `---` markers.

    Args:
        content: Full PROJECT.md file content

    Returns:
        YAML frontmatter string (without ---), or None if not found
    """
    # Match YAML frontmatter between --- markers
    pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.search(pattern, content, re.DOTALL | re.MULTILINE)

    if match:
        return match.group(1)

    return None


def extract_overview_description(content: str) -> Optional[str]:
    """
    Extract Purpose and Context from the Overview section.

    Args:
        content: Full PROJECT.md file content

    Returns:
        Combined Purpose and Context text, or None if not found
    """
    # Look for ## Overview section
    overview_pattern = r'## Overview\s*\n\n(.*?)(?=\n##|\Z)'
    overview_match = re.search(overview_pattern, content, re.DOTALL)

    if not overview_match:
        return None

    overview_text = overview_match.group(1)

    # Extract Purpose and Context lines
    purpose_pattern = r'\*\*Purpose\*\*:\s*(.+?)(?:\n|$)'
    context_pattern = r'\*\*Context\*\*:\s*(.+?)(?:\n|$)'

    purpose_match = re.search(purpose_pattern, overview_text)
    context_match = re.search(context_pattern, overview_text)

    parts = []
    if purpose_match:
        parts.append(purpose_match.group(1).strip())
    if context_match:
        parts.append(context_match.group(1).strip())

    return ' '.join(parts) if parts else None


def extract_recent_updates(content: str) -> tuple[list[str], list[str]]:
    """
    Extract recent decisions and updates from ### Recent Updates section.

    Updates have emoji (✓, ⚠️, •, -) at the start after the date.
    Decisions don't have emoji.

    Args:
        content: Full PROJECT.md file content

    Returns:
        Tuple of (decisions list, updates list)
    """
    decisions = []
    updates = []

    # Look for ### Recent Updates section
    updates_pattern = r'### Recent Updates\s*\n(.*?)(?=\n##|\Z)'
    updates_match = re.search(updates_pattern, content, re.DOTALL)

    if not updates_match:
        return ([], [])

    updates_text = updates_match.group(1)

    # Parse bullet points: - DATE: text (from source)
    # We'll look for lines starting with "- " followed by a date
    line_pattern = r'^- (\d{4}-\d{2}-\d{2}): (.+?)(?:\(from .+?\))?$'

    for line in updates_text.split('\n'):
        line = line.strip()
        if not line or not line.startswith('- '):
            continue

        match = re.match(line_pattern, line)
        if not match:
            continue

        date_str = match.group(1)
        text = match.group(2).strip()

        # Check if text starts with emoji (updates) or plain text (decisions)
        # Common emojis: ✓ ⚠️ • - and other unicode symbols
        emoji_chars = ['✓', '⚠️', '•', '✅', '❌', '⚡', '🔴', '🟡', '🟢']

        # Check if starts with emoji
        is_update = any(text.startswith(emoji) for emoji in emoji_chars)

        if is_update:
            # Remove emoji and leading space for cleaner display
            for emoji in emoji_chars:
                if text.startswith(emoji):
                    text = text[len(emoji):].strip()
                    break
            # Truncate if too long
            if len(text) > 100:
                text = text[:97] + "..."
            updates.append(f"{date_str}: {text}")
        else:
            # Decision - truncate if too long
            if len(text) > 100:
                text = text[:97] + "..."
            decisions.append(f"{date_str}: {text}")

    # Return most recent 10 of each
    return (decisions[:10], updates[:10])


def parse_yaml_simple(yaml_str: str) -> Dict[str, Any]:
    """
    Simple YAML parser for PROJECT.md frontmatter.

    This parser handles the simple key: value format used in PROJECT.md files.
    It does NOT support full YAML spec, but works for our predictable structure.

    Args:
        yaml_str: YAML frontmatter string

    Returns:
        Parsed YAML as dictionary
    """
    data = {}
    current_list_key = None

    for line in yaml_str.split('\n'):
        # Skip comments and empty lines
        if line.strip().startswith('#') or not line.strip():
            continue

        # Check for list items (lines starting with - )
        if line.strip().startswith('- ') and current_list_key:
            value = line.strip()[2:].strip()  # Remove '- ' prefix
            # Remove quotes if present
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            data[current_list_key].append(value)
            continue

        # Check for key: value pairs
        if ': ' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()

            # Handle null/None values
            if value in ['null', 'None', '']:
                data[key] = None
            # Handle boolean values
            elif value.lower() == 'true':
                data[key] = True
            elif value.lower() == 'false':
                data[key] = False
            # Handle quoted strings
            elif value.startswith('"') and value.endswith('"'):
                data[key] = value[1:-1]
            # Handle numbers
            elif value.isdigit():
                data[key] = int(value)
            # Handle empty lists
            elif value == '[]':
                data[key] = []
                current_list_key = None
            # Plain string
            else:
                data[key] = value

            # Check if this starts a list (key: with no value or [])
            if value == '' or value == '[]':
                if key not in data:
                    data[key] = []
                current_list_key = key

    return data


def parse_project_file(project_file: Path) -> Optional[Project]:
    """
    Parse a single PROJECT.md file into a Project object.

    Args:
        project_file: Path to PROJECT.md file

    Returns:
        Project object, or None if parsing fails
    """
    try:
        content = project_file.read_text()

        # Extract YAML frontmatter
        yaml_str = extract_yaml_frontmatter(content)
        if not yaml_str:
            print(f"Warning: No YAML frontmatter found in {project_file}")
            return None

        # Parse YAML
        data = parse_yaml_simple(yaml_str)

        # Validate required fields
        required_fields = ["title", "category", "container", "status", "priority"]
        for field in required_fields:
            if field not in data:
                print(f"Warning: Missing required field '{field}' in {project_file}")
                return None

        # Parse dates
        created = parse_date(str(data.get("created")))
        if not created:
            print(f"Warning: Invalid or missing 'created' date in {project_file}")
            return None

        due = parse_date(str(data.get("due")))
        completed = parse_date(str(data.get("completed")))
        last_updated = parse_date(str(data.get("last_updated"))) or date.today()
        hubspot_last_sync = parse_date(str(data.get("hubspot_last_sync")))

        # Parse tags (can be list or None)
        tags = data.get("tags", [])
        if tags is None:
            tags = []
        elif not isinstance(tags, list):
            tags = []

        # Extract description from Overview section
        description = extract_overview_description(content)

        # Extract recent decisions and updates
        recent_decisions, recent_updates = extract_recent_updates(content)

        # Create Project object
        project = Project(
            title=data["title"],
            category=data["category"],
            container=data["container"],
            status=data["status"],
            priority=data["priority"],
            project_dir=project_file.parent,
            project_md_path=project_file,
            created=created,
            due=due,
            completed=completed,
            last_updated=last_updated,
            progress_percent=int(data.get("progress_percent", 0)),
            tasks_total=int(data.get("tasks_total", 0)),
            tasks_completed=int(data.get("tasks_completed", 0)),
            estimated_hours=int(data.get("estimated_hours", 0)),
            actual_hours=int(data.get("actual_hours", 0)),
            blocked=bool(data.get("blocked", False)),
            needs_review=bool(data.get("needs_review", False)),
            hubspot_company_id=data.get("hubspot_company_id"),
            hubspot_deal_id=data.get("hubspot_deal_id"),
            hubspot_last_sync=hubspot_last_sync,
            tags=tags,
            owner=data.get("owner"),
            description=description,
            recent_decisions=recent_decisions,
            recent_updates=recent_updates
        )

        return project

    except Exception as e:
        print(f"Error parsing {project_file}: {e}")
        return None


def load_all_projects(root_dir: Optional[Path] = None) -> List[Project]:
    """
    Discover and load all projects from the projects directory.

    Args:
        root_dir: Root directory to search (default: ~/projects)

    Returns:
        List of Project objects
    """
    if root_dir is None:
        root_dir = Path.home() / "projects"

    # Discover PROJECT.md files
    project_files = discover_projects(root_dir)

    # Parse each file
    projects = []
    for project_file in project_files:
        project = parse_project_file(project_file)
        if project:
            projects.append(project)

    return projects


def filter_projects(projects: List[Project],
                    status: Optional[str] = None,
                    category: Optional[str] = None,
                    priority: Optional[str] = None,
                    blocked: Optional[bool] = None) -> List[Project]:
    """
    Filter projects by various criteria.

    Args:
        projects: List of Project objects
        status: Filter by status (active, on-hold, blocked, completed)
        category: Filter by category (personal, development, family, work)
        priority: Filter by priority (high, medium, low)
        blocked: Filter by blocked status

    Returns:
        Filtered list of Project objects
    """
    filtered = projects

    if status:
        filtered = [p for p in filtered if p.status.lower() == status.lower()]

    if category:
        filtered = [p for p in filtered if p.category.lower() == category.lower()]

    if priority:
        filtered = [p for p in filtered if p.priority.lower() == priority.lower()]

    if blocked is not None:
        filtered = [p for p in filtered if p.blocked == blocked]

    return filtered


def sort_projects(projects: List[Project], sort_by: str = "priority") -> List[Project]:
    """
    Sort projects by various criteria.

    Args:
        projects: List of Project objects
        sort_by: Sort criteria - "priority", "category", "due_date", "last_updated", "name", "risk"

    Returns:
        Sorted list of Project objects
    """
    if sort_by == "priority":
        # Sort by priority: high > medium > low
        priority_order = {"high": 0, "medium": 1, "low": 2}
        return sorted(projects, key=lambda p: priority_order.get(p.priority.lower(), 3))

    elif sort_by == "category":
        # Sort by category: work > development > personal > family
        category_order = {"work": 0, "development": 1, "personal": 2, "family": 3}
        return sorted(projects, key=lambda p: (category_order.get(p.category.lower(), 4), p.title.lower()))

    elif sort_by == "due_date":
        # Sort by due date: sooner first, None last
        return sorted(projects, key=lambda p: (p.due is None, p.due))

    elif sort_by == "last_updated":
        # Sort by last updated: most recent first
        return sorted(projects, key=lambda p: p.last_updated, reverse=True)

    elif sort_by == "name":
        # Sort by title alphabetically
        return sorted(projects, key=lambda p: p.title.lower())

    elif sort_by == "risk":
        # Sort by risk score: highest risk first
        return sorted(projects, key=lambda p: p.risk_score, reverse=True)

    else:
        return projects
