"""
Task parser - reads and parses tasks from tasks.md files.
"""
import re
from pathlib import Path
from typing import List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Task:
    """Represents a single task from tasks.md"""
    text: str
    status: str  # '[ ]', '[→]', '[✓]', '[!]', '[~]', '[×]'
    line_number: int
    is_completed: bool
    assignee: Optional[str] = None  # Who owns this task

    @property
    def status_display(self) -> str:
        """Returns a clean display version of status"""
        status_map = {
            '[ ]': 'TODO',
            '[→]': 'PROG',
            '[✓]': 'DONE',
            '[!]': 'BLCK',
            '[~]': 'HOLD',
            '[×]': 'CANC'
        }
        return status_map.get(self.status, 'UNKN')


@dataclass
class DeletedTask:
    """Represents a deleted task for undo functionality"""
    file_path: Path
    line_number: int
    content: List[str]  # The task line and all its sub-items
    deleted_at: datetime


def parse_tasks_file(tasks_file: Path) -> List[Task]:
    """
    Parse a tasks.md file and extract all tasks.

    Args:
        tasks_file: Path to tasks.md file

    Returns:
        List of Task objects
    """
    if not tasks_file.exists():
        return []

    try:
        content = tasks_file.read_text()
        lines = content.split('\n')
        tasks = []

        # Match task lines: - [X] Task text
        task_pattern = r'^- (\[.?\]) (.+)$'
        assignee_pattern = r'^\s+- Assignee:\s*(.+)$'

        i = 0
        while i < len(lines):
            line = lines[i]
            match = re.match(task_pattern, line)
            if match:
                status = match.group(1)
                text = match.group(2).strip()
                is_completed = status in ['[✓]', '[×]']
                assignee = None

                # Look ahead for assignee on next lines
                j = i + 1
                while j < len(lines) and lines[j].startswith('  '):
                    assignee_match = re.match(assignee_pattern, lines[j])
                    if assignee_match:
                        assignee = assignee_match.group(1).strip()
                        break
                    j += 1

                tasks.append(Task(
                    text=text,
                    status=status,
                    line_number=i + 1,
                    is_completed=is_completed,
                    assignee=assignee
                ))
            i += 1

        return tasks

    except Exception as e:
        print(f"Error parsing tasks file {tasks_file}: {e}")
        return []


def toggle_task_completion(tasks_file: Path, line_number: int) -> bool:
    """
    Toggle a task's completion status in the tasks.md file.

    Toggles between [ ] and [✓].

    Args:
        tasks_file: Path to tasks.md file
        line_number: Line number of the task to toggle (1-indexed)

    Returns:
        True if successful, False otherwise
    """
    if not tasks_file.exists():
        return False

    try:
        lines = tasks_file.read_text().split('\n')

        # Convert to 0-indexed
        idx = line_number - 1

        if idx < 0 or idx >= len(lines):
            return False

        line = lines[idx]

        # Toggle [ ] <-> [✓]
        if '[ ]' in line:
            lines[idx] = line.replace('[ ]', '[✓]', 1)
        elif '[✓]' in line:
            lines[idx] = line.replace('[✓]', '[ ]', 1)
        else:
            # Line doesn't have a toggleable status
            return False

        # Write back to file
        tasks_file.write_text('\n'.join(lines))
        return True

    except Exception as e:
        print(f"Error toggling task in {tasks_file}: {e}")
        return False


def count_task_stats(tasks: List[Task]) -> Tuple[int, int]:
    """
    Count total and completed tasks.

    Args:
        tasks: List of Task objects

    Returns:
        Tuple of (total_tasks, completed_tasks)
    """
    total = len(tasks)
    completed = sum(1 for t in tasks if t.is_completed)
    return (total, completed)


def delete_task(tasks_file: Path, line_number: int) -> Optional[DeletedTask]:
    """
    Delete a task from the tasks.md file.

    Removes the task line and all its sub-items (lines starting with "  - ").

    Args:
        tasks_file: Path to tasks.md file
        line_number: Line number of the task to delete (1-indexed)

    Returns:
        DeletedTask object for undo, or None if deletion failed
    """
    if not tasks_file.exists():
        return None

    try:
        lines = tasks_file.read_text().split('\n')

        # Convert to 0-indexed
        idx = line_number - 1

        if idx < 0 or idx >= len(lines):
            return None

        line = lines[idx]

        # Verify this is a task line
        if not re.match(r'^- \[.?\] ', line):
            return None

        # Collect the task and all its sub-items
        deleted_lines = [line]
        j = idx + 1

        # Get all following lines that start with "  - " (sub-items)
        while j < len(lines) and lines[j].startswith('  - '):
            deleted_lines.append(lines[j])
            j += 1

        # Create DeletedTask record for undo
        deleted_task = DeletedTask(
            file_path=tasks_file,
            line_number=line_number,
            content=deleted_lines,
            deleted_at=datetime.now()
        )

        # Remove the task and its sub-items
        num_lines_to_remove = len(deleted_lines)
        del lines[idx:idx + num_lines_to_remove]

        # Write back to file
        tasks_file.write_text('\n'.join(lines))

        return deleted_task

    except Exception as e:
        print(f"Error deleting task from {tasks_file}: {e}")
        return None


def undo_task_deletion(deleted_task: DeletedTask) -> bool:
    """
    Restore a previously deleted task.

    Args:
        deleted_task: DeletedTask object from delete_task()

    Returns:
        True if successful, False otherwise
    """
    if not deleted_task.file_path.exists():
        return False

    try:
        lines = deleted_task.file_path.read_text().split('\n')

        # Convert to 0-indexed
        idx = deleted_task.line_number - 1

        # Insert the deleted content back at the original position
        for i, line in enumerate(deleted_task.content):
            lines.insert(idx + i, line)

        # Write back to file
        deleted_task.file_path.write_text('\n'.join(lines))

        return True

    except Exception as e:
        print(f"Error restoring task to {deleted_task.file_path}: {e}")
        return False
