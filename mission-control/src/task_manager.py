"""
Task management operations - move, copy, and reassign tasks between projects.
"""
from pathlib import Path
from typing import List, Optional, Dict
from dataclasses import dataclass
import re


@dataclass
class TaskToMove:
    """Represents a task to be moved"""
    text: str  # Full task text including checkboxes
    lines: List[str]  # All lines including sub-items
    completed: bool
    source_project: str
    source_file: Path


class TaskManager:
    """
    Manages task operations across projects.

    Handles moving and copying tasks between projects' tasks.md files.
    """

    def __init__(self, projects_dir: Path):
        """
        Initialize task manager.

        Args:
            projects_dir: Root projects directory
        """
        self.projects_dir = projects_dir

    def move_task(self, task: TaskToMove, dest_project_name: str) -> Dict:
        """
        Move a task from one project to another.

        Args:
            task: TaskToMove object with source info
            dest_project_name: Destination project name

        Returns:
            Result dict with success status and details
        """
        result = {
            'success': False,
            'error': None,
            'task_text': task.text,
            'source_project': task.source_project,
            'dest_project': dest_project_name
        }

        # Don't move if already in destination project
        if task.source_project == dest_project_name:
            result['error'] = 'Task is already in this project'
            return result

        # Find destination project
        dest_project_dir = self._find_project_dir(dest_project_name)
        if not dest_project_dir:
            result['error'] = f'Destination project not found: {dest_project_name}'
            return result

        dest_tasks_file = dest_project_dir / 'tasks.md'
        if not dest_tasks_file.exists():
            result['error'] = f'tasks.md not found in {dest_project_name}'
            return result

        try:
            # Add task to destination
            self._add_task_to_file(dest_tasks_file, task)

            # Remove task from source
            self._remove_task_from_file(task.source_file, task)

            result['success'] = True

        except Exception as e:
            result['error'] = str(e)

        return result

    def copy_task(self, task: TaskToMove, dest_project_name: str) -> Dict:
        """
        Copy a task to another project (keeps original).

        Args:
            task: TaskToMove object with source info
            dest_project_name: Destination project name

        Returns:
            Result dict with success status and details
        """
        result = {
            'success': False,
            'error': None,
            'task_text': task.text,
            'source_project': task.source_project,
            'dest_project': dest_project_name
        }

        # Find destination project
        dest_project_dir = self._find_project_dir(dest_project_name)
        if not dest_project_dir:
            result['error'] = f'Destination project not found: {dest_project_name}'
            return result

        dest_tasks_file = dest_project_dir / 'tasks.md'
        if not dest_tasks_file.exists():
            result['error'] = f'tasks.md not found in {dest_project_name}'
            return result

        try:
            # Add task to destination (don't remove from source)
            self._add_task_to_file(dest_tasks_file, task)

            result['success'] = True

        except Exception as e:
            result['error'] = str(e)

        return result

    def move_multiple_tasks(self, tasks: List[TaskToMove],
                           dest_project_name: str) -> Dict:
        """
        Move multiple tasks to another project.

        Args:
            tasks: List of TaskToMove objects
            dest_project_name: Destination project name

        Returns:
            Summary dict with counts and errors
        """
        summary = {
            'total': len(tasks),
            'moved': 0,
            'failed': 0,
            'errors': []
        }

        for task in tasks:
            result = self.move_task(task, dest_project_name)

            if result['success']:
                summary['moved'] += 1
            else:
                summary['failed'] += 1
                summary['errors'].append(result['error'])

        return summary

    def _find_project_dir(self, project_name: str) -> Optional[Path]:
        """Find project directory by name"""
        for project_file in self.projects_dir.rglob("PROJECT.md"):
            if project_file.parent.name == project_name:
                return project_file.parent
        return None

    def _add_task_to_file(self, tasks_file: Path, task: TaskToMove):
        """
        Add a task to a tasks.md file.

        Args:
            tasks_file: Path to destination tasks.md
            task: TaskToMove object
        """
        content = tasks_file.read_text()
        lines = content.split('\n')

        # Determine task priority from checkbox state or text
        priority = self._guess_task_priority(task.text)

        # Try to find appropriate section
        section_header = f"### {priority.capitalize()} Priority"

        # Look for the section
        insert_idx = None
        for i, line in enumerate(lines):
            if section_header in line or section_header.lower() in line.lower():
                # Found the section, insert after header
                insert_idx = i + 1
                break

        # If section not found, try Active Tasks section
        if insert_idx is None:
            for i, line in enumerate(lines):
                if line.strip() == "## Active Tasks":
                    # Insert at end of Active Tasks section (before next ## section)
                    insert_idx = self._find_section_end(lines, i)

                    # Add section header if needed
                    task_lines = [f"\n{section_header}"] + task.lines + ['']
                    lines[insert_idx:insert_idx] = task_lines
                    tasks_file.write_text('\n'.join(lines))
                    return

        # If we found the priority section, insert there
        if insert_idx is not None:
            # Insert task lines
            task_lines = task.lines + ['']  # Add blank line after
            lines[insert_idx:insert_idx] = task_lines
            tasks_file.write_text('\n'.join(lines))
            return

        # Last resort: append to end
        new_content = content.rstrip() + '\n\n## Moved Tasks\n\n' + \
                     section_header + '\n' + '\n'.join(task.lines) + '\n'
        tasks_file.write_text(new_content)

    def _remove_task_from_file(self, tasks_file: Path, task: TaskToMove):
        """
        Remove a task from a tasks.md file.

        Args:
            tasks_file: Path to source tasks.md
            task: TaskToMove object
        """
        content = tasks_file.read_text()
        lines = content.split('\n')

        # Find and remove the task lines
        task_start_idx = None

        # Look for the main task line
        main_task_line = task.lines[0] if task.lines else task.text

        for i, line in enumerate(lines):
            if line.strip() == main_task_line.strip():
                task_start_idx = i
                break

        if task_start_idx is None:
            raise ValueError(f"Task not found in file: {main_task_line[:50]}")

        # Determine how many lines to remove (including sub-items)
        lines_to_remove = len(task.lines)

        # Remove the lines
        del lines[task_start_idx:task_start_idx + lines_to_remove]

        # Clean up extra blank lines
        while task_start_idx < len(lines) and not lines[task_start_idx].strip():
            del lines[task_start_idx]

        tasks_file.write_text('\n'.join(lines))

    def _find_section_end(self, lines: List[str], section_start: int) -> int:
        """
        Find where a section ends (before next ## header or end of file).

        Args:
            lines: All file lines
            section_start: Index of section header

        Returns:
            Index where section ends
        """
        for i in range(section_start + 1, len(lines)):
            if lines[i].startswith('##') and not lines[i].startswith('###'):
                return i
        return len(lines)

    def _guess_task_priority(self, task_text: str) -> str:
        """
        Guess task priority from text.

        Args:
            task_text: Task text

        Returns:
            'high', 'medium', or 'low'
        """
        task_lower = task_text.lower()

        # Look for priority keywords
        if any(word in task_lower for word in ['urgent', 'critical', 'asap', 'immediately']):
            return 'high'
        elif any(word in task_lower for word in ['low', 'nice to have', 'optional']):
            return 'low'
        else:
            return 'medium'

    def get_task_from_line(self, tasks_file: Path, task_line_content: str,
                          project_name: str) -> Optional[TaskToMove]:
        """
        Extract a TaskToMove object from a specific task line.

        Args:
            tasks_file: Path to tasks.md
            task_line_content: The content of the task line
            project_name: Name of the source project

        Returns:
            TaskToMove object or None if not found
        """
        content = tasks_file.read_text()
        lines = content.split('\n')

        # Find the task line
        task_start_idx = None
        for i, line in enumerate(lines):
            # Match the task content (strip checkbox and whitespace)
            line_content = re.sub(r'^-\s*\[.?\]\s*', '', line.strip())
            if line_content == task_line_content:
                task_start_idx = i
                break

        if task_start_idx is None:
            return None

        # Extract all lines belonging to this task
        task_lines = [lines[task_start_idx]]

        # Check for sub-items (indented lines that follow)
        i = task_start_idx + 1
        while i < len(lines):
            line = lines[i]
            # Sub-items start with spaces or tabs
            if line.startswith('  ') or line.startswith('\t'):
                task_lines.append(line)
                i += 1
            elif not line.strip():
                # Blank line might separate tasks or might be within task
                # Check if next line is also indented
                if i + 1 < len(lines) and (lines[i + 1].startswith('  ') or lines[i + 1].startswith('\t')):
                    task_lines.append(line)
                    i += 1
                else:
                    break
            else:
                # Non-indented, non-blank line - end of task
                break

        # Determine if completed
        completed = '[✓]' in lines[task_start_idx] or '[x]' in lines[task_start_idx].lower()

        return TaskToMove(
            text=task_line_content,
            lines=task_lines,
            completed=completed,
            source_project=project_name,
            source_file=tasks_file
        )
