"""
Project creator - scaffolds new projects with templates and structure.
"""
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
import re


class ProjectCreator:
    """
    Creates and scaffolds new projects in the Mission Control structure.

    Handles project directory creation, template generation, and initial files.
    """

    def __init__(self, projects_dir: Path):
        """
        Initialize project creator.

        Args:
            projects_dir: Root projects directory (e.g., ~/projects/)
        """
        self.projects_dir = projects_dir

    def create_project(self, title: str, category: str, container: str,
                      priority: str = "medium", owner: str = "Jason Pace",
                      description: str = "") -> Dict:
        """
        Create a new project with full scaffolding.

        Args:
            title: Project title (human-readable)
            category: Category (work, personal, development, family)
            container: Container directory (e.g., "client-projects")
            priority: Priority level (high, medium, low)
            owner: Project owner name
            description: Project description

        Returns:
            Result dict with success status and project path
        """
        result = {
            'success': False,
            'error': None,
            'project_name': None,
            'project_path': None
        }

        # Validate inputs
        if not title or not category:
            result['error'] = 'Title and category are required'
            return result

        # Generate project directory name from title
        project_name = self._slugify(title)

        if not project_name:
            result['error'] = 'Could not generate valid project name from title'
            return result

        # Determine project path
        if container:
            project_path = self.projects_dir / category / container / project_name
        else:
            project_path = self.projects_dir / category / project_name

        # Check if project already exists
        if project_path.exists():
            result['error'] = f'Project already exists: {project_name}'
            return result

        try:
            # Create project directory
            project_path.mkdir(parents=True, exist_ok=False)

            # Create PROJECT.md
            self._create_project_md(
                project_path, title, category, container,
                priority, owner, description
            )

            # Create tasks.md
            self._create_tasks_md(project_path, title)

            # Create timeline.md
            self._create_timeline_md(project_path, title)

            # Create meeting-notes/ for work projects
            if category == 'work':
                (project_path / 'meeting-notes').mkdir(exist_ok=True)
                self._create_meeting_notes_readme(project_path)

            result['success'] = True
            result['project_name'] = project_name
            result['project_path'] = str(project_path)

        except Exception as e:
            result['error'] = str(e)

            # Cleanup on failure
            if project_path.exists():
                import shutil
                shutil.rmtree(project_path, ignore_errors=True)

        return result

    def _slugify(self, text: str) -> str:
        """
        Convert title to URL-friendly slug.

        Args:
            text: Title text

        Returns:
            Slugified name (lowercase-with-hyphens)
        """
        # Convert to lowercase
        text = text.lower()

        # Replace spaces and underscores with hyphens
        text = re.sub(r'[\s_]+', '-', text)

        # Remove any non-alphanumeric characters except hyphens
        text = re.sub(r'[^a-z0-9-]', '', text)

        # Remove leading/trailing hyphens
        text = text.strip('-')

        # Collapse multiple hyphens
        text = re.sub(r'-+', '-', text)

        return text

    def _create_project_md(self, project_path: Path, title: str,
                          category: str, container: str, priority: str,
                          owner: str, description: str):
        """Create PROJECT.md with YAML frontmatter and template structure"""
        today = datetime.now().strftime('%Y-%m-%d')

        content = f"""---
title: {title}
category: {category}
status: active
priority: {priority}
owner: {owner}
created: {today}
last_updated: {today}
due_date:
estimated_hours:
actual_hours:
progress_percent: 0
tasks_total: 0
tasks_completed: 0
needs_review: false
tags: []
related_projects: []
collaborators: []
stakeholders: []
external_links: []
repository:
description: {description if description else ''}
---

# {title}

**Category**: {category.capitalize()}
**Status**: Active
**Priority**: {priority.capitalize()}
**Owner**: {owner}

---

## Overview

{description if description else 'Project description pending.'}

---

## Goals

### Primary Objectives
- [ ] Define primary objective
- [ ] Set measurable success criteria

### Success Criteria
- TBD

---

## Scope

### In Scope
- TBD

### Out of Scope
- TBD

---

## Timeline

**Start Date**: {today}
**Target Completion**: TBD

Key milestones tracked in [timeline.md](./timeline.md).

---

## Resources

### Team
- **Owner**: {owner}

### Tools & Systems
- TBD

### Documentation
- Tasks: [tasks.md](./tasks.md)
- Timeline: [timeline.md](./timeline.md)

---

## Decisions

Key decisions will be recorded here with dates.

---

## Recent Updates

- {today}: Project created

---

## Risks

### Current Risks
- TBD

---

## Notes

Additional project notes and context.

---

**Last Updated**: {today}
"""

        (project_path / 'PROJECT.md').write_text(content)

    def _create_tasks_md(self, project_path: Path, title: str):
        """Create tasks.md with standard structure"""
        today = datetime.now().strftime('%Y-%m-%d')

        content = f"""# Tasks - {title}

**Project**: [Link to PROJECT.md](./PROJECT.md)
**Last Updated**: {today}

---

## Active Tasks

### High Priority

### Medium Priority

### Low Priority

---

## Completed Tasks

---

## Backlog

---

**Last Updated**: {today}
"""

        (project_path / 'tasks.md').write_text(content)

    def _create_timeline_md(self, project_path: Path, title: str):
        """Create timeline.md with standard structure"""
        today = datetime.now().strftime('%Y-%m-%d')

        content = f"""# Timeline - {title}

**Project**: [Link to PROJECT.md](./PROJECT.md)
**Last Updated**: {today}

---

## Milestones

### Upcoming

### Completed

---

## Timeline

**{today}**: Project created

---

**Last Updated**: {today}
"""

        (project_path / 'timeline.md').write_text(content)

    def _create_meeting_notes_readme(self, project_path: Path):
        """Create README in meeting-notes directory"""
        content = """# Meeting Notes

Store meeting notes, transcripts, and summaries in this directory.

## Naming Convention

Use the format: `YYYY-MM-DD-description.md`

Examples:
- `2026-01-09-kickoff-meeting.md`
- `2026-01-15-weekly-sync.md`

---

**Note**: You can also drop files into `~/projects/import/` and the AI will automatically route them here.
"""

        (project_path / 'meeting-notes' / 'README.md').write_text(content)

    def get_available_containers(self, category: str) -> list:
        """
        Get list of available container directories for a category.

        Args:
            category: Category name (work, personal, development, family)

        Returns:
            List of container directory names
        """
        category_path = self.projects_dir / category

        if not category_path.exists():
            return []

        containers = []
        for item in category_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                containers.append(item.name)

        return sorted(containers)
