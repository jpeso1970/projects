"""
Import history tracking and rollback system.

Tracks the last N imports with full rollback data to enable undo functionality.
"""
import json
import shutil
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from dataclasses import dataclass, asdict


@dataclass
class TaskChange:
    """Represents a task that was added during import"""
    text: str
    project: str
    assignee: Optional[str] = None


@dataclass
class DecisionChange:
    """Represents a decision that was added during import"""
    date: str
    text: str
    project: str


@dataclass
class UpdateChange:
    """Represents an update that was added during import"""
    date: str
    text: str
    project: str


@dataclass
class ProjectChanges:
    """Changes made to a single project"""
    project_name: str
    tasks_added: List[TaskChange]
    decisions_added: List[DecisionChange]
    updates_added: List[UpdateChange]


@dataclass
class ImportHistoryEntry:
    """A single import history entry with rollback data"""
    id: str  # Unique ID
    timestamp: str  # ISO format
    source_file: str
    changes: List[ProjectChanges]
    can_undo: bool = True
    undone: bool = False
    original_file_backup: Optional[str] = None


class ImportHistory:
    """
    Manages import history and rollback functionality.

    Stores the last N imports with complete rollback data.
    """

    def __init__(self, history_dir: Path, max_entries: int = 10):
        """
        Initialize import history manager.

        Args:
            history_dir: Directory to store history data
            max_entries: Maximum number of history entries to keep
        """
        self.history_dir = history_dir
        self.max_entries = max_entries
        self.history_file = history_dir / "import-history.json"
        self.backup_dir = history_dir / "backups"

        # Create directories
        self.history_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def add_entry(self, source_file: str, source_path: Path,
                  routing_result: Dict) -> str:
        """
        Add a new import to history with rollback data.

        Args:
            source_file: Original filename
            source_path: Path to original file (for backup)
            routing_result: Result dict from ContentRouter.route_analysis()

        Returns:
            Import ID
        """
        # Generate unique ID
        import_id = datetime.now().strftime("%Y%m%d-%H%M%S")

        # Backup original file
        backup_path = None
        if source_path and source_path.exists():
            backup_filename = f"{import_id}-{source_file}"
            backup_path = self.backup_dir / backup_filename
            shutil.copy2(source_path, backup_path)

        # Extract project changes from routing result
        changes = self._extract_changes_from_routing(routing_result)

        # Create history entry
        entry = ImportHistoryEntry(
            id=import_id,
            timestamp=datetime.now().isoformat(),
            source_file=source_file,
            changes=changes,
            can_undo=True,
            undone=False,
            original_file_backup=str(backup_path) if backup_path else None
        )

        # Load existing history
        history = self._load_history()

        # Add new entry
        history.append(asdict(entry))

        # Trim to max entries
        if len(history) > self.max_entries:
            # Remove oldest entries
            removed = history[:-self.max_entries]
            history = history[-self.max_entries:]

            # Clean up old backups
            for old_entry in removed:
                backup_file = old_entry.get('original_file_backup')
                if backup_file:
                    try:
                        Path(backup_file).unlink(missing_ok=True)
                    except Exception:
                        pass

        # Save history
        self._save_history(history)

        return import_id

    def _extract_changes_from_routing(self, routing_result: Dict) -> List[ProjectChanges]:
        """
        Extract structured change data from routing result.

        Args:
            routing_result: Result from ContentRouter.route_analysis()

        Returns:
            List of ProjectChanges objects
        """
        changes = []

        # Group changes by project
        projects_data = {}

        # Extract tasks
        for task_data in routing_result.get('task_details', []):
            project = task_data.get('project', 'HOLDING')
            if project not in projects_data:
                projects_data[project] = {
                    'tasks': [],
                    'decisions': [],
                    'updates': []
                }

            projects_data[project]['tasks'].append(TaskChange(
                text=task_data.get('text', ''),
                project=project,
                assignee=task_data.get('assignee')
            ))

        # Extract decisions
        for decision_data in routing_result.get('decision_details', []):
            project = decision_data.get('project', 'HOLDING')
            if project not in projects_data:
                projects_data[project] = {
                    'tasks': [],
                    'decisions': [],
                    'updates': []
                }

            projects_data[project]['decisions'].append(DecisionChange(
                date=decision_data.get('date', ''),
                text=decision_data.get('text', ''),
                project=project
            ))

        # Extract updates
        for update_data in routing_result.get('update_details', []):
            project = update_data.get('project', 'HOLDING')
            if project not in projects_data:
                projects_data[project] = {
                    'tasks': [],
                    'decisions': [],
                    'updates': []
                }

            projects_data[project]['updates'].append(UpdateChange(
                date=update_data.get('date', ''),
                text=update_data.get('summary', update_data.get('text', '')),
                project=project
            ))

        # Convert to ProjectChanges objects
        for project_name, data in projects_data.items():
            changes.append(ProjectChanges(
                project_name=project_name,
                tasks_added=data['tasks'],
                decisions_added=data['decisions'],
                updates_added=data['updates']
            ))

        return changes

    def get_recent_imports(self, include_undone: bool = False) -> List[Dict]:
        """
        Get recent import history.

        Args:
            include_undone: If True, include already-undone imports

        Returns:
            List of import history entries (most recent first)
        """
        history = self._load_history()

        if not include_undone:
            history = [e for e in history if not e.get('undone', False)]

        # Sort by timestamp (newest first)
        history.sort(key=lambda x: x.get('timestamp', ''), reverse=True)

        return history

    def undo_import(self, import_id: str, projects_dir: Path) -> Dict:
        """
        Undo an import by removing all added content.

        Args:
            import_id: ID of import to undo
            projects_dir: Root projects directory

        Returns:
            Summary of undo operation
        """
        history = self._load_history()

        # Find the entry
        entry = None
        entry_idx = None
        for idx, e in enumerate(history):
            if e.get('id') == import_id:
                entry = e
                entry_idx = idx
                break

        if not entry:
            return {
                'success': False,
                'error': f'Import {import_id} not found in history'
            }

        if entry.get('undone'):
            return {
                'success': False,
                'error': 'Import already undone'
            }

        if not entry.get('can_undo'):
            return {
                'success': False,
                'error': 'Import cannot be undone'
            }

        summary = {
            'success': True,
            'import_id': import_id,
            'source_file': entry.get('source_file'),
            'projects_affected': [],
            'tasks_removed': 0,
            'decisions_removed': 0,
            'updates_removed': 0,
            'errors': []
        }

        # Rollback changes for each project
        for change_data in entry.get('changes', []):
            project_name = change_data.get('project_name')

            try:
                result = self._rollback_project_changes(
                    project_name, change_data, projects_dir
                )

                summary['projects_affected'].append(project_name)
                summary['tasks_removed'] += result['tasks_removed']
                summary['decisions_removed'] += result['decisions_removed']
                summary['updates_removed'] += result['updates_removed']
                summary['errors'].extend(result['errors'])

            except Exception as e:
                error_msg = f"Error rolling back {project_name}: {e}"
                summary['errors'].append(error_msg)

        # Restore original file to import directory if backup exists
        backup_path = entry.get('original_file_backup')
        if backup_path and Path(backup_path).exists():
            try:
                import_dir = projects_dir / "import"
                restore_path = import_dir / entry.get('source_file')

                # Don't overwrite if file already exists
                if not restore_path.exists():
                    shutil.copy2(backup_path, restore_path)
                    summary['file_restored'] = True
                else:
                    summary['file_restored'] = False
                    summary['errors'].append(
                        f"File {entry.get('source_file')} already exists in import directory"
                    )
            except Exception as e:
                summary['errors'].append(f"Error restoring file: {e}")

        # Mark as undone
        entry['undone'] = True
        entry['undone_at'] = datetime.now().isoformat()
        history[entry_idx] = entry

        self._save_history(history)

        return summary

    def _rollback_project_changes(self, project_name: str, change_data: Dict,
                                   projects_dir: Path) -> Dict:
        """
        Rollback changes for a single project.

        Args:
            project_name: Project directory name
            change_data: ProjectChanges dict
            projects_dir: Root projects directory

        Returns:
            Summary of rollback for this project
        """
        result = {
            'tasks_removed': 0,
            'decisions_removed': 0,
            'updates_removed': 0,
            'errors': []
        }

        # Find project directory
        project_dir = self._find_project_dir(project_name, projects_dir)
        if not project_dir:
            result['errors'].append(f"Project directory not found: {project_name}")
            return result

        # Rollback tasks
        tasks_file = project_dir / "tasks.md"
        if tasks_file.exists() and change_data.get('tasks_added'):
            try:
                removed = self._remove_tasks_from_file(
                    tasks_file, change_data['tasks_added']
                )
                result['tasks_removed'] = removed
            except Exception as e:
                result['errors'].append(f"Error removing tasks: {e}")

        # Rollback decisions and updates from PROJECT.md
        project_file = project_dir / "PROJECT.md"
        if project_file.exists():
            try:
                # Remove decisions
                if change_data.get('decisions_added'):
                    removed = self._remove_decisions_from_file(
                        project_file, change_data['decisions_added']
                    )
                    result['decisions_removed'] = removed

                # Remove updates
                if change_data.get('updates_added'):
                    removed = self._remove_updates_from_file(
                        project_file, change_data['updates_added']
                    )
                    result['updates_removed'] = removed

            except Exception as e:
                result['errors'].append(f"Error removing decisions/updates: {e}")

        return result

    def _find_project_dir(self, project_name: str, projects_dir: Path) -> Optional[Path]:
        """Find project directory by name"""
        for project_file in projects_dir.rglob("PROJECT.md"):
            if project_file.parent.name == project_name:
                return project_file.parent
        return None

    def _remove_tasks_from_file(self, tasks_file: Path, tasks_to_remove: List[Dict]) -> int:
        """
        Remove specific tasks from tasks.md file.

        Args:
            tasks_file: Path to tasks.md
            tasks_to_remove: List of task dicts to remove

        Returns:
            Number of tasks removed
        """
        content = tasks_file.read_text()
        lines = content.split('\n')

        # Extract task texts to remove
        task_texts = {task.get('text', '') for task in tasks_to_remove}

        # Filter out matching tasks
        new_lines = []
        removed_count = 0

        for line in lines:
            # Check if this line is a task that should be removed
            is_task_line = line.strip().startswith('- [ ]') or line.strip().startswith('- [✓]')

            if is_task_line:
                # Extract task text (after checkbox)
                task_text = line.strip()[5:].strip()  # Remove "- [ ] " or "- [✓] "

                # Check if this task should be removed
                if task_text in task_texts:
                    removed_count += 1
                    continue  # Skip this line

            new_lines.append(line)

        # Write back
        tasks_file.write_text('\n'.join(new_lines))

        return removed_count

    def _remove_decisions_from_file(self, project_file: Path,
                                     decisions_to_remove: List[Dict]) -> int:
        """
        Remove specific decisions from PROJECT.md file.

        Args:
            project_file: Path to PROJECT.md
            decisions_to_remove: List of decision dicts to remove

        Returns:
            Number of decisions removed
        """
        content = project_file.read_text()
        lines = content.split('\n')

        # Extract decision texts to remove
        decision_texts = {d.get('text', '') for d in decisions_to_remove}

        new_lines = []
        removed_count = 0
        in_decisions_section = False

        for line in lines:
            # Track if we're in decisions section
            if line.strip().startswith('## Decisions') or line.strip().startswith('### Decisions'):
                in_decisions_section = True
                new_lines.append(line)
                continue

            # Exit decisions section
            if in_decisions_section and line.strip().startswith('#'):
                in_decisions_section = False

            # Check if this is a decision to remove
            if in_decisions_section and line.strip().startswith('- '):
                decision_text = line.strip()[2:].strip()
                # Remove date prefix if present
                if ': ' in decision_text:
                    decision_text = decision_text.split(': ', 1)[1]

                if decision_text in decision_texts:
                    removed_count += 1
                    continue  # Skip this line

            new_lines.append(line)

        project_file.write_text('\n'.join(new_lines))

        return removed_count

    def _remove_updates_from_file(self, project_file: Path,
                                   updates_to_remove: List[Dict]) -> int:
        """
        Remove specific updates from PROJECT.md file.

        Args:
            project_file: Path to PROJECT.md
            updates_to_remove: List of update dicts to remove

        Returns:
            Number of updates removed
        """
        content = project_file.read_text()
        lines = content.split('\n')

        # Extract update texts to remove
        update_texts = {u.get('text', '') for u in updates_to_remove}

        new_lines = []
        removed_count = 0
        in_updates_section = False

        for line in lines:
            # Track if we're in recent updates section
            if 'Recent Updates' in line or 'recent_updates' in line.lower():
                in_updates_section = True
                new_lines.append(line)
                continue

            # Exit updates section
            if in_updates_section and line.strip().startswith('#'):
                in_updates_section = False

            # Check if this is an update to remove
            if in_updates_section and line.strip().startswith('- '):
                update_text = line.strip()[2:].strip()
                # Remove date prefix if present
                if ': ' in update_text:
                    update_text = update_text.split(': ', 1)[1]

                if update_text in update_texts:
                    removed_count += 1
                    continue  # Skip this line

            new_lines.append(line)

        project_file.write_text('\n'.join(new_lines))

        return removed_count

    def _load_history(self) -> List[Dict]:
        """Load history from JSON file"""
        if not self.history_file.exists():
            return []

        try:
            return json.loads(self.history_file.read_text())
        except Exception:
            return []

    def _save_history(self, history: List[Dict]):
        """Save history to JSON file"""
        self.history_file.write_text(json.dumps(history, indent=2))
