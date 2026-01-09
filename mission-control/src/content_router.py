"""
Content router - applies analyzed content to project files.

Updates:
- tasks.md (adds new tasks)
- PROJECT.md (adds decisions to Recent Updates)
- meeting-notes/ (saves original file)
"""
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import re

try:
    from .content_analyzer import (
        ContentAnalysis, ExtractedTask, ExtractedDecision, ExtractedUpdate
    )
except ImportError:
    from content_analyzer import (
        ContentAnalysis, ExtractedTask, ExtractedDecision, ExtractedUpdate
    )


class ContentRouter:
    """
    Routes analyzed content to appropriate project files.
    """

    def __init__(self, projects_dir: Path):
        """
        Initialize content router.

        Args:
            projects_dir: Root projects directory
        """
        self.projects_dir = projects_dir

    def route_analysis(self, analysis: ContentAnalysis,
                      source_filename: str) -> Dict[str, any]:
        """
        Route all analyzed content to appropriate locations.

        Args:
            analysis: ContentAnalysis object
            source_filename: Original filename for reference

        Returns:
            Routing summary
        """
        summary = {
            "tasks_added": 0,
            "decisions_added": 0,
            "updates_applied": 0,
            "projects_updated": set(),
            "holding_items": 0,
            "errors": []
        }

        # Route tasks
        for task in analysis.tasks:
            try:
                if task.project == "HOLDING":
                    self._add_to_holding(task, source_filename)
                    summary["holding_items"] += 1
                else:
                    self._add_task_to_project(task, source_filename)
                    summary["tasks_added"] += 1
                    summary["projects_updated"].add(task.project)
            except Exception as e:
                summary["errors"].append(f"Task routing error: {e}")

        # Route decisions
        for decision in analysis.decisions:
            try:
                if decision.project == "HOLDING":
                    self._add_to_holding(decision, source_filename)
                    summary["holding_items"] += 1
                else:
                    self._add_decision_to_project(decision, source_filename)
                    summary["decisions_added"] += 1
                    summary["projects_updated"].add(decision.project)
            except Exception as e:
                summary["errors"].append(f"Decision routing error: {e}")

        # Route updates
        for update in analysis.updates:
            try:
                if update.project == "HOLDING":
                    self._add_to_holding(update, source_filename)
                    summary["holding_items"] += 1
                else:
                    self._add_update_to_project(update, source_filename)
                    summary["updates_applied"] += 1
                    summary["projects_updated"].add(update.project)
            except Exception as e:
                summary["errors"].append(f"Update routing error: {e}")

        # Route unmatched content to holding
        if analysis.unmatched_content:
            for content in analysis.unmatched_content:
                self._add_to_holding(content, source_filename)
                summary["holding_items"] += len(analysis.unmatched_content)

        return summary

    def _find_project_dir(self, project_name: str) -> Optional[Path]:
        """Find project directory by name"""
        for project_file in self.projects_dir.rglob("PROJECT.md"):
            if project_file.parent.name == project_name:
                return project_file.parent
        return None

    def _add_task_to_project(self, task: ExtractedTask, source: str):
        """Add a task to project's tasks.md"""
        project_dir = self._find_project_dir(task.project)
        if not project_dir:
            raise ValueError(f"Project not found: {task.project}")

        tasks_file = project_dir / "tasks.md"
        if not tasks_file.exists():
            raise ValueError(f"tasks.md not found in {project_dir}")

        # Read current content
        content = tasks_file.read_text()
        original_content = content  # Keep backup to detect if changes were made

        # Build task text
        task_text = f"- [ ] {task.text}"
        if task.assignee:
            task_text += f"\n  - Assignee: {task.assignee}"
        if task.due_date:
            task_text += f"\n  - Due: {task.due_date}"
        if task.context:
            task_text += f"\n  - Context: {task.context} (from {source})"
        else:
            task_text += f"\n  - Source: {source}"
        task_text += "\n\n"

        # Strategy 1: Try to find standard priority section
        priority_map = {
            "high": "### High Priority",
            "medium": "### Medium Priority",
            "low": "### Low Priority"
        }
        section_header = priority_map.get(task.priority.lower(), "### Medium Priority")

        if section_header in content:
            # Insert after section header
            pattern = f"({re.escape(section_header)}.*?\n)"
            replacement = f"\\1{task_text}"
            content = re.sub(pattern, replacement, content, count=1)

        # Strategy 2: If standard sections don't exist, try to add to Active Tasks section
        elif "## Active Tasks" in content:
            # Find where Active Tasks section ends (next ## section or end of file)
            lines = content.split('\n')
            active_tasks_idx = None
            insert_idx = None

            for i, line in enumerate(lines):
                if line.strip() == "## Active Tasks":
                    active_tasks_idx = i
                elif active_tasks_idx is not None and line.startswith("##") and not line.startswith("###"):
                    # Found next major section
                    insert_idx = i
                    break

            if active_tasks_idx is not None:
                if insert_idx is None:
                    # No next section found, add at end
                    insert_idx = len(lines)

                # Insert task before the next section
                priority_label = f"\n### {task.priority.capitalize()} Priority (from imports)"
                task_block = f"{priority_label}\n{task_text}"

                # Check if we already have an "imports" priority section
                imports_section_exists = False
                for i in range(active_tasks_idx, insert_idx):
                    if "from imports" in lines[i].lower():
                        # Found existing imports section, add after it
                        lines.insert(i + 1, task_text.rstrip())
                        imports_section_exists = True
                        break

                if not imports_section_exists:
                    # Add new section before the next major section
                    lines.insert(insert_idx, task_block.rstrip())

                content = '\n'.join(lines)

        # Strategy 3: Last resort - append to end of file
        if content == original_content:
            # Nothing was added, append to end
            content += f"\n\n## Imported Tasks\n\n### {task.priority.capitalize()} Priority\n{task_text}"

        # Write back
        tasks_file.write_text(content)

    def _add_decision_to_project(self, decision: ExtractedDecision, source: str):
        """Add a decision to project's PROJECT.md Recent Updates"""
        project_dir = self._find_project_dir(decision.project)
        if not project_dir:
            raise ValueError(f"Project not found: {decision.project}")

        project_file = project_dir / "PROJECT.md"
        if not project_file.exists():
            raise ValueError(f"PROJECT.md not found in {project_dir}")

        # Read current content
        content = project_file.read_text()

        # Update last_updated in YAML
        today = datetime.now().strftime("%Y-%m-%d")
        content = re.sub(
            r'(last_updated:\s*)\d{4}-\d{2}-\d{2}',
            f'\\g<1>{today}',
            content
        )

        # Add to Recent Updates section
        update_text = f"- {decision.date}: {decision.text} (from {source})"

        # Check for duplicates - look for same decision text (ignore date and source)
        # Normalize for comparison: extract just the decision text
        decision_text_normalized = decision.text.lower().strip()
        if decision_text_normalized in content.lower():
            # Already exists, skip adding duplicate
            return

        if "### Recent Updates" in content:
            # Insert after Recent Updates header
            pattern = "(### Recent Updates.*?\n)"
            replacement = f"\\1{update_text}\n"
            content = re.sub(pattern, replacement, content, count=1)
        else:
            # Create Recent Updates section after Current Status
            if "## Current Status" in content:
                pattern = "(## Current Status.*?\n\n)"
                replacement = f"\\1### Recent Updates\n{update_text}\n\n"
                content = re.sub(pattern, replacement, content, count=1, flags=re.DOTALL)

        # Write back
        project_file.write_text(content)

    def _add_update_to_project(self, update: ExtractedUpdate, source: str):
        """Add a narrative update to project's PROJECT.md"""
        project_dir = self._find_project_dir(update.project)
        if not project_dir:
            raise ValueError(f"Project not found: {update.project}")

        project_file = project_dir / "PROJECT.md"
        if not project_file.exists():
            raise ValueError(f"PROJECT.md not found in {project_dir}")

        # Read current content
        content = project_file.read_text()

        # Update last_updated in YAML
        today = datetime.now().strftime("%Y-%m-%d")
        content = re.sub(
            r'(last_updated:\s*)\d{4}-\d{2}-\d{2}',
            f'\\g<1>{today}',
            content
        )

        # Add to Recent Updates section
        sentiment_emoji = {
            "positive": "✓",
            "negative": "⚠️",
            "mixed": "•",
            "neutral": "-"
        }
        emoji = sentiment_emoji.get(update.sentiment.lower(), "-")

        update_text = f"- {today}: {emoji} {update.summary}"
        if update.details:
            update_text += f" - {update.details}"
        update_text += f" (from {source})"

        # Check for duplicates - look for same summary text (ignore date and emoji)
        # Normalize for comparison: extract just the summary text
        summary_normalized = update.summary.lower().strip()
        if summary_normalized in content.lower():
            # Already exists, skip adding duplicate
            return

        if "### Recent Updates" in content:
            pattern = "(### Recent Updates.*?\n)"
            replacement = f"\\1{update_text}\n"
            content = re.sub(pattern, replacement, content, count=1)
        else:
            # Create Recent Updates section
            if "## Current Status" in content:
                pattern = "(## Current Status.*?\n\n)"
                replacement = f"\\1### Recent Updates\n{update_text}\n\n"
                content = re.sub(pattern, replacement, content, count=1, flags=re.DOTALL)

        # Write back
        project_file.write_text(content)

    def _add_to_holding(self, item: any, source: str):
        """Add item to holding project for unmatched content"""
        # Find or create holding project
        holding_dir = self.projects_dir / "work" / "internal" / "_holding-unprocessed-content"
        holding_dir.mkdir(parents=True, exist_ok=True)

        # Ensure PROJECT.md exists
        project_md = holding_dir / "PROJECT.md"
        if not project_md.exists():
            self._create_holding_project(holding_dir)

        # Append to holding file
        holding_file = holding_dir / "unprocessed-content.md"

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        entry = f"\n## {timestamp} - From: {source}\n\n"

        if isinstance(item, str):
            entry += f"{item}\n"
        elif hasattr(item, 'text'):
            entry += f"{item.text}\n"
            if hasattr(item, 'context') and item.context:
                entry += f"\n*Context: {item.context}*\n"
        elif hasattr(item, 'summary'):
            entry += f"{item.summary}\n\n{item.details}\n"

        entry += "\n---\n"

        # Append to file
        if holding_file.exists():
            content = holding_file.read_text()
            holding_file.write_text(content + entry)
        else:
            holding_file.write_text(f"# Unprocessed Content\n\n{entry}")

    def _create_holding_project(self, holding_dir: Path):
        """Create the holding project structure"""
        project_md = holding_dir / "PROJECT.md"

        today = datetime.now().strftime("%Y-%m-%d")

        content = f"""---
# Required Fields
title: "Holding - Unprocessed Content"
category: "work"
container: "internal"
status: "active"
priority: "low"

# Dates (ISO 8601 format)
created: {today}
due: null
completed: null
last_updated: {today}

# Tags (array)
tags:
  - holding
  - internal
  - unprocessed

# People (optional, can be null)
owner: "Jason Pace"
collaborators: []
stakeholders: []

# Metrics (for agent tracking)
progress_percent: 0
estimated_hours: 0
actual_hours: 0
tasks_total: 0
tasks_completed: 0

# Links (optional)
related_projects: []
external_links: []
repository: null

# Flags (for agent automation)
needs_review: true
blocked: false
auto_archive_on_complete: false
---

# Holding - Unprocessed Content

## Overview

**Purpose**: Temporary holding area for content that couldn't be automatically matched to existing projects.

**Context**: Content from meeting notes, transcripts, and emails that mentions entities or topics without clear project associations.

## Instructions

1. Review unprocessed-content.md regularly
2. Manually route content to appropriate projects
3. Create new projects if needed
4. Archive processed items

## Files

- **unprocessed-content.md**: All unmatched content with timestamps and sources

---

**Project Created**: {today}
**Last Updated**: {today}
**Project Owner**: Jason Pace
"""

        project_md.write_text(content)

        # Create unprocessed-content.md
        content_md = holding_dir / "unprocessed-content.md"
        content_md.write_text("# Unprocessed Content\n\nContent that needs manual routing.\n\n---\n\n")
