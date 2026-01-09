"""
Import processor for meeting summaries and transcripts.

Watches .import directory and routes files to appropriate projects.
Uses AI to analyze content and extract structured data.
"""
import re
import os
from pathlib import Path
from typing import List, Tuple, Dict, Optional
from datetime import datetime
from dataclasses import dataclass

try:
    # Try relative imports first (when used as package)
    from .content_analyzer import ContentAnalyzer
    from .content_router import ContentRouter
    # from .staging import StagingManager  # PHASE 1: No longer needed
    from .file_reader import read_file_content
    AI_ENABLED = True
except ImportError:
    try:
        # Fall back to absolute imports (when used as standalone module)
        from content_analyzer import ContentAnalyzer
        from content_router import ContentRouter
        # from staging import StagingManager  # PHASE 1: No longer needed
        from file_reader import read_file_content
        AI_ENABLED = True
    except ImportError:
        AI_ENABLED = False
        # Try to import just the file reader
        try:
            from .file_reader import read_file_content
        except ImportError:
            from file_reader import read_file_content


@dataclass
class ProjectMention:
    """Represents a detected mention of a project in content"""
    project_name: str
    confidence: float  # 0.0 - 1.0
    context: str  # Surrounding text snippet
    source: str  # 'filename' or 'content'


@dataclass
class ImportFile:
    """Represents a file in the import directory"""
    path: Path
    filename: str
    mentions: List[ProjectMention]
    created: datetime
    processed: bool = False


class ImportProcessor:
    """
    Processes files dropped into the import directory.

    Features:
    - Detects project names in filenames
    - Scans content for project mentions
    - Routes files to appropriate project meeting-notes/ folders
    - Handles multi-project meeting transcripts
    """

    def __init__(self, import_dir: Path, projects_dir: Path):
        """
        Initialize the import processor.

        Args:
            import_dir: Directory to watch for imports (e.g., ~/projects/import/)
            projects_dir: Root projects directory (e.g., ~/projects/)
        """
        self.import_dir = import_dir
        self.projects_dir = projects_dir
        self.archive_dir = projects_dir / ".import-archive"

        # Create directories
        self.import_dir.mkdir(parents=True, exist_ok=True)
        self.archive_dir.mkdir(parents=True, exist_ok=True)

    def scan_import_directory(self) -> List[ImportFile]:
        """
        Scan import directory for new files.

        Returns:
            List of ImportFile objects
        """
        import_files = []

        for file_path in self.import_dir.glob('*'):
            # Skip hidden files and directories
            if file_path.name.startswith('.') or file_path.is_dir():
                continue

            # Skip README
            if file_path.name == 'README.md':
                continue

            # Get file metadata
            stat = file_path.stat()
            created = datetime.fromtimestamp(stat.st_mtime)

            # Detect project mentions
            mentions = self.detect_project_mentions(file_path)

            import_files.append(ImportFile(
                path=file_path,
                filename=file_path.name,
                mentions=mentions,
                created=created,
                processed=False
            ))

        return import_files

    def detect_project_mentions(self, file_path: Path) -> List[ProjectMention]:
        """
        Detect project mentions in filename and content.

        Args:
            file_path: Path to file to analyze

        Returns:
            List of ProjectMention objects
        """
        mentions = []

        # Get all project directories
        project_names = self._get_all_project_names()

        # Check filename
        filename = file_path.name.lower()
        for project_name in project_names:
            # Create searchable pattern (handle hyphens, spaces, etc.)
            pattern = project_name.lower().replace('-', '[-\\s]?')

            if re.search(pattern, filename):
                mentions.append(ProjectMention(
                    project_name=project_name,
                    confidence=0.9,
                    context=f"Filename: {file_path.name}",
                    source='filename'
                ))

        # Check content
        try:
            content = read_file_content(file_path)
            if content:
                content_lower = content.lower()

                for project_name in project_names:
                    # Create searchable pattern
                    pattern = project_name.lower().replace('-', '[-\\s]?')

                    # Find all matches in content
                    for match in re.finditer(pattern, content_lower):
                        # Extract context (50 chars before and after)
                        start = max(0, match.start() - 50)
                        end = min(len(content), match.end() + 50)
                        context = content[start:end].strip()

                        # Check if already found in filename
                        already_found = any(
                            m.project_name == project_name and m.source == 'filename'
                            for m in mentions
                        )

                        if not already_found:
                            mentions.append(ProjectMention(
                                project_name=project_name,
                                confidence=0.7,
                                context=f"...{context}...",
                                source='content'
                            ))
                            break  # Only add once per project

        except Exception as e:
            print(f"Error reading file {file_path}: {e}")

        return mentions

    def _get_all_project_names(self) -> List[str]:
        """
        Get all project directory names from projects directory.

        Returns:
            List of project directory names
        """
        project_names = []

        # Find all PROJECT.md files
        for project_file in self.projects_dir.rglob("PROJECT.md"):
            # Skip excluded directories
            if any(pattern in str(project_file) for pattern in
                   [".templates", "_archived", ".git", ".agents", ".docs", ".import"]):
                continue

            # Get directory name
            project_dir = project_file.parent
            project_name = project_dir.name
            project_names.append(project_name)

        return project_names

    def route_file(self, import_file: ImportFile, project_name: str,
                   copy: bool = True) -> Optional[Path]:
        """
        Route a file to a specific project's meeting-notes/ directory.

        Args:
            import_file: ImportFile to route
            project_name: Target project name
            copy: If True, copy file; if False, move file

        Returns:
            Path to destination file, or None if failed
        """
        # Find project directory
        project_dir = self._find_project_dir(project_name)
        if not project_dir:
            print(f"Project directory not found for: {project_name}")
            return None

        # Ensure meeting-notes directory exists
        meeting_notes_dir = project_dir / "meeting-notes"
        meeting_notes_dir.mkdir(exist_ok=True)

        # Generate destination filename with timestamp
        timestamp = import_file.created.strftime("%Y-%m-%d")
        base_name = import_file.filename
        dest_name = f"{timestamp}-{base_name}"
        dest_path = meeting_notes_dir / dest_name

        # Handle duplicate filenames
        counter = 1
        while dest_path.exists():
            name_parts = base_name.rsplit('.', 1)
            if len(name_parts) == 2:
                dest_name = f"{timestamp}-{name_parts[0]}-{counter}.{name_parts[1]}"
            else:
                dest_name = f"{timestamp}-{base_name}-{counter}"
            dest_path = meeting_notes_dir / dest_name
            counter += 1

        # Copy or move file
        try:
            if copy:
                import shutil
                shutil.copy2(import_file.path, dest_path)
            else:
                import_file.path.rename(dest_path)

            print(f"Routed {import_file.filename} -> {dest_path}")
            return dest_path

        except Exception as e:
            print(f"Error routing file: {e}")
            return None

    def _find_project_dir(self, project_name: str) -> Optional[Path]:
        """
        Find project directory by name.

        Args:
            project_name: Project directory name to find

        Returns:
            Path to project directory, or None if not found
        """
        for project_file in self.projects_dir.rglob("PROJECT.md"):
            if project_file.parent.name == project_name:
                return project_file.parent
        return None

    def process_file(self, import_file: ImportFile,
                     auto_route: bool = True) -> Dict[str, any]:
        """
        Process a single import file.

        Args:
            import_file: ImportFile to process
            auto_route: If True, automatically route high-confidence matches

        Returns:
            Processing result dictionary
        """
        result = {
            'filename': import_file.filename,
            'mentions': len(import_file.mentions),
            'routed_to': [],
            'requires_manual': False
        }

        if not import_file.mentions:
            result['requires_manual'] = True
            result['reason'] = 'No project mentions detected'
            return result

        # High confidence mentions (from filename)
        high_confidence = [m for m in import_file.mentions if m.confidence >= 0.9]

        if auto_route and high_confidence:
            # Route to all high-confidence projects
            for mention in high_confidence:
                dest = self.route_file(import_file, mention.project_name, copy=True)
                if dest:
                    result['routed_to'].append(mention.project_name)

            # Archive processed file
            if result['routed_to']:
                self._archive_file(import_file)
        else:
            result['requires_manual'] = True
            result['reason'] = 'Multiple projects or low confidence'

        return result

    def _archive_file(self, import_file: ImportFile):
        """
        Move a processed file to the archive directory.

        Args:
            import_file: ImportFile object to archive
        """
        # Create timestamped archive filename
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        archive_filename = f"{timestamp}-{import_file.filename}"
        archive_path = self.archive_dir / archive_filename

        # Move file to archive
        import_file.path.rename(archive_path)

    def process_all(self, auto_route: bool = True, use_ai: bool = False) -> Dict[str, any]:
        """
        Process all files in import directory.

        Args:
            auto_route: If True, automatically route high-confidence matches
            use_ai: If True, use AI to analyze content and extract structured data

        Returns:
            Summary of processing results
        """
        if use_ai:
            return self.process_all_with_ai()

        import_files = self.scan_import_directory()

        summary = {
            'total_files': len(import_files),
            'auto_routed': 0,
            'manual_review': 0,
            'no_mentions': 0,
            'results': []
        }

        for import_file in import_files:
            result = self.process_file(import_file, auto_route=auto_route)
            summary['results'].append(result)

            if result['routed_to']:
                summary['auto_routed'] += 1
            elif result['requires_manual']:
                if 'No project mentions' in result.get('reason', ''):
                    summary['no_mentions'] += 1
                else:
                    summary['manual_review'] += 1

        return summary

    def process_all_with_ai(self) -> Dict[str, any]:
        """
        Process all files using AI content analysis.

        Extracts tasks, decisions, and updates from content and applies them immediately.

        Returns:
            Summary of AI processing results
        """
        if not AI_ENABLED:
            raise RuntimeError("AI processing not available. Install: pip install anthropic")

        # Check for API key
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY environment variable not set. "
                "AI processing requires Claude API access."
            )

        # Initialize AI components
        analyzer = ContentAnalyzer(api_key)
        router = ContentRouter(self.projects_dir)

        # Get all project names
        known_projects = self._get_all_project_names()

        # Scan import directory
        import_files = self.scan_import_directory()

        summary = {
            'total_files': len(import_files),
            'analyzed': 0,
            'tasks_added': 0,
            'decisions_added': 0,
            'updates_applied': 0,
            'projects_updated': set(),
            'holding_items': 0,
            'errors': [],
            'results': []
        }

        for import_file in import_files:
            try:
                print(f"Analyzing: {import_file.filename}")

                # Analyze content with AI
                analysis = analyzer.analyze_file(import_file.path, known_projects)

                summary['analyzed'] += 1

                # Apply directly to projects
                routing_result = router.route_analysis(analysis, import_file.filename)

                summary['tasks_added'] += routing_result['tasks_added']
                summary['decisions_added'] += routing_result['decisions_added']
                summary['updates_applied'] += routing_result['updates_applied']
                summary['projects_updated'].update(routing_result['projects_updated'])
                summary['holding_items'] += routing_result['holding_items']
                summary['errors'].extend(routing_result['errors'])

                summary['results'].append({
                    'filename': import_file.filename,
                    'tasks': len(analysis.tasks),
                    'decisions': len(analysis.decisions),
                    'updates': len(analysis.updates),
                    'projects': list(analysis.project_mentions.keys()),
                    'routing': routing_result
                })

                # Archive file after processing
                self._archive_file(import_file)

            except Exception as e:
                error_msg = f"Error processing {import_file.filename}: {e}"
                summary['errors'].append(error_msg)
                print(f"ERROR: {error_msg}")

        # Convert set to list for JSON serialization
        summary['projects_updated'] = list(summary['projects_updated'])

        return summary

    def apply_approved_analyses(self) -> Dict[str, any]:
        """
        Apply approved staged analyses to project files.

        Returns:
            Summary of application results
        """
        if not AI_ENABLED:
            raise RuntimeError("AI processing not available")

        # Initialize components
        staging_dir = self.projects_dir / ".mission-control" / "staging"
        staging_manager = StagingManager(staging_dir)
        router = ContentRouter(self.projects_dir)

        summary = {
            'total_approved': 0,
            'tasks_added': 0,
            'decisions_added': 0,
            'updates_applied': 0,
            'projects_updated': set(),
            'holding_items': 0,
            'errors': [],
            'results': []
        }

        # Find all approved staging files
        for staging_file in staging_dir.glob("*.json"):
            try:
                data = staging_manager.load_analysis(staging_file)

                if data.get('status') != 'approved':
                    continue

                summary['total_approved'] += 1

                # Get approved items
                approved = staging_manager.get_approved_items(staging_file)

                # Reconstruct analysis objects
                from .content_analyzer import ExtractedTask, ExtractedDecision, ExtractedUpdate

                # Build lists of approved items only
                tasks = [ExtractedTask(**t) for t in approved['tasks']]
                decisions = [ExtractedDecision(**d) for d in approved['decisions']]
                updates = [ExtractedUpdate(**u) for u in approved['updates']]

                # Create a minimal ContentAnalysis-like dict for routing
                analysis_data = {
                    'tasks': tasks,
                    'decisions': decisions,
                    'updates': updates
                }

                # Route each type separately
                source_filename = data['original_file']

                for task in tasks:
                    try:
                        if task.project == "HOLDING":
                            router._add_to_holding(task, source_filename)
                            summary['holding_items'] += 1
                        else:
                            router._add_task_to_project(task, source_filename)
                            summary['tasks_added'] += 1
                            summary['projects_updated'].add(task.project)
                    except Exception as e:
                        summary['errors'].append(f"Task routing error: {e}")

                for decision in decisions:
                    try:
                        if decision.project == "HOLDING":
                            router._add_to_holding(decision, source_filename)
                            summary['holding_items'] += 1
                        else:
                            router._add_decision_to_project(decision, source_filename)
                            summary['decisions_added'] += 1
                            summary['projects_updated'].add(decision.project)
                    except Exception as e:
                        summary['errors'].append(f"Decision routing error: {e}")

                for update in updates:
                    try:
                        if update.project == "HOLDING":
                            router._add_to_holding(update, source_filename)
                            summary['holding_items'] += 1
                        else:
                            router._add_update_to_project(update, source_filename)
                            summary['updates_applied'] += 1
                            summary['projects_updated'].add(update.project)
                    except Exception as e:
                        summary['errors'].append(f"Update routing error: {e}")

                summary['results'].append({
                    'filename': source_filename,
                    'tasks': len(tasks),
                    'decisions': len(decisions),
                    'updates': len(updates)
                })

                # Archive the processed staging file
                staging_manager.archive_processed(staging_file)

            except Exception as e:
                error_msg = f"Error applying {staging_file.name}: {e}"
                summary['errors'].append(error_msg)
                print(f"ERROR: {error_msg}")

        # Convert set to list
        summary['projects_updated'] = list(summary['projects_updated'])

        return summary


def create_import_dir_readme(import_dir: Path):
    """Create a README in the import directory explaining usage"""
    readme_path = import_dir / "README.md"

    readme_content = """# Import Directory

Drop files here for AI-powered import processing and automatic routing to projects.

## How It Works

1. **Drop files** in this directory (images, PDFs, text, markdown, documents, etc.)
2. **Watch Imports** auto-processes every 10 seconds (or process manually)
3. AI analyzes content and routes to appropriate project(s) **automatically**
4. Content is added immediately to project files (tasks.md, PROJECT.md)
5. Files are archived to `../.import-archive/`

## Two Ways to Process

### Method 1: Watch Imports (Recommended)
1. Drop files here
2. Launch Watch Imports: `~/projects/mission-control/watch-imports`
   - Or double-click **Watch Imports.command** in Finder
3. Files are auto-processed every 10 seconds
4. Changes applied automatically - no review needed!

### Method 2: Manual Processing
1. Drop files here
2. Open Mission Control: `~/projects/mission-control/mc`
3. Files will be processed next time watch-imports runs
   - Or process manually: `mc --process-imports`

## Supported File Types

- **Images**: PNG, JPG, HEIC, etc. (OCR text extraction)
- **Documents**: PDF, DOCX, TXT, MD
- **Meeting transcripts**: Any text format
- **Screenshots**: Auto-analyzed for content

## AI Analysis

The AI examines:
- File content and text
- Filename for project mentions
- Context and subject matter
- Related projects in the system

Then automatically:
- Routes to correct project(s)
- Creates tasks
- Records decisions
- Notes updates

## What Happens to Files

1. **Analyzed**: AI extracts tasks, decisions, and updates
2. **Applied**: Content automatically added to project files
3. **Archived**: Files moved to `../.import-archive/` with timestamp

## Trust First, Fix Later

Files are processed automatically. If AI routes something incorrectly, you can:
- Move tasks between projects (coming soon: `[m]` key)
- Edit project files directly to fix mistakes
- Future: Undo recent imports (coming soon: `[u]` key)

---
Last Updated: {date}
"""

    readme_path.write_text(readme_content.format(date=datetime.now().strftime("%Y-%m-%d")))
