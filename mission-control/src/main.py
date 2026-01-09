#!/usr/bin/env python3
"""
Mission Control - Main application entry point.
"""
import curses
import sys
import time
from pathlib import Path

from .loader import load_all_projects, sort_projects, filter_projects
from .views.dashboard import render_dashboard, init_colors
from .views.split_view import render_split_view
from .views.three_pane_view import render_three_pane_view
from .views.imports_view import render_imports_modal, process_imports_with_feedback
# from .views.review_view import render_review_modal  # PHASE 1: Removed staging/review workflow
from .views.import_history_view import render_import_history_modal, show_undo_result  # PHASE 2: Undo system
from .views.task_move_view import render_project_picker, show_move_result  # PHASE 3: Task move/reassign
from .views.project_create_view import render_project_create_modal, show_project_create_result  # PHASE 4: Create project
from .views.help_view import render_help_modal
from .task_parser import parse_tasks_file, toggle_task_completion, delete_task, undo_task_deletion
from .import_processor import create_import_dir_readme, ImportProcessor
from .import_history import ImportHistory  # PHASE 2: Import history
from .task_manager import TaskManager  # PHASE 3: Task management
from .project_creator import ProjectCreator  # PHASE 4: Project creation
# from .staging import StagingManager  # PHASE 1: Staging system removed


def main_loop(stdscr):
    """
    Main curses event loop.

    Args:
        stdscr: Curses window object
    """
    # Initialize colors and disable mouse
    curses.curs_set(0)  # Hide cursor
    curses.mousemask(0)  # Disable mouse events to prevent corruption
    init_colors()

    # Setup import directory (visible, not hidden)
    projects_root = Path.home() / "projects"
    import_dir = projects_root / "import"
    import_dir.mkdir(parents=True, exist_ok=True)

    # Create README if needed
    readme_path = import_dir / "README.md"
    if not readme_path.exists():
        create_import_dir_readme(import_dir)

    # Load projects
    try:
        projects = load_all_projects()
    except Exception as e:
        stdscr.addstr(0, 0, f"Error loading projects: {e}")
        stdscr.addstr(1, 0, "Press any key to exit...")
        stdscr.getch()
        return

    if not projects:
        stdscr.addstr(0, 0, "No projects found!")
        stdscr.addstr(1, 0, "Create a project with: /new-project")
        stdscr.addstr(2, 0, "Press any key to exit...")
        stdscr.getch()
        return

    # Application state
    selected_project_idx = 0
    selected_task_idx = 0
    active_pane = "projects"  # Can be: "projects", "tasks", or "summary"
    sort_by = "priority"  # Can be: priority, category, due_date, last_updated, name, risk
    filter_by = "all"  # Can be: all, active, blocked, work, personal, development, family, high
    deletion_history = []  # Stack of deleted tasks for undo
    last_import_check = time.time()  # Track last auto-import check
    auto_import_interval = 30  # Check for imports every 30 seconds
    summary_scroll_offset = 0  # Scroll position for summary pane
    all_projects = projects  # Keep unfiltered list

    # Apply initial filter and sort
    def apply_filter_and_sort(all_projs, filt, sort):
        """Apply filter then sort to projects"""
        if filt == "all":
            filtered = all_projs
        elif filt == "active":
            filtered = filter_projects(all_projs, status="active")
        elif filt == "blocked":
            filtered = filter_projects(all_projs, blocked=True)
        elif filt == "work":
            filtered = filter_projects(all_projs, category="work")
        elif filt == "personal":
            filtered = filter_projects(all_projs, category="personal")
        elif filt == "development":
            filtered = filter_projects(all_projs, category="development")
        elif filt == "family":
            filtered = filter_projects(all_projs, category="family")
        elif filt == "high":
            filtered = filter_projects(all_projs, priority="high")
        else:
            filtered = all_projs
        return sort_projects(filtered, sort)

    projects = apply_filter_and_sort(all_projects, filter_by, sort_by)

    # Load tasks for selected project
    tasks = []
    if projects:
        tasks_file = projects[selected_project_idx].project_dir / "tasks.md"
        tasks = parse_tasks_file(tasks_file)

    # Render tracking
    needs_render = True  # Initial render

    # Main loop
    while True:
        # Check for auto-import (every 30 seconds)
        current_time = time.time()
        if current_time - last_import_check >= auto_import_interval:
            last_import_check = current_time

            # Check if there are files to process
            processor = ImportProcessor(import_dir, projects_root)
            import_files = processor.scan_import_directory()

            if import_files:
                # Auto-process files with AI
                try:
                    summary = processor.process_all(auto_route=False, use_ai=True, stage_for_review=True)

                    if summary['analyzed'] > 0:
                        # Show brief notification
                        stdscr.clear()
                        height, width = stdscr.getmaxyx()
                        msg = f"✓ Auto-imported {summary['analyzed']} file(s) - Press [i] to review"
                        stdscr.addstr(height // 2, (width - len(msg)) // 2, msg, curses.A_BOLD)
                        stdscr.refresh()
                        curses.napms(2000)  # Show for 2 seconds

                        # Refresh projects in case new data
                        all_projects = load_all_projects()
                        projects = apply_filter_and_sort(all_projects, filter_by, sort_by)
                        needs_render = True  # Need to re-render after import
                except Exception as e:
                    # Silent fail - don't interrupt user
                    pass

        # Only render if something changed
        if needs_render:
            render_three_pane_view(stdscr, projects, tasks, selected_project_idx,
                                  selected_task_idx, active_pane, sort_by, summary_scroll_offset,
                                  filter_by, len(all_projects))
            needs_render = False

        # Get user input with timeout (100ms) to allow auto-import checks
        stdscr.timeout(100)
        try:
            key = stdscr.getch()
            if key == -1:  # No key pressed (timeout)
                continue
        except KeyboardInterrupt:
            break

        # Handle input (set needs_render = True after state changes)
        if key == ord('q') or key == ord('Q'):
            # Quit
            break

        elif key == ord('\t'):  # Tab key
            # Toggle between projects and tasks (use 'p' for summary)
            if active_pane == "projects":
                active_pane = "tasks"
            else:  # tasks or summary
                active_pane = "projects"
            needs_render = True

        elif key == ord('p') or key == ord('P'):
            # Switch to summary pane
            active_pane = "summary"
            needs_render = True

        elif key == curses.KEY_UP or key == ord('k') or key == ord('K'):
            # Move selection up or scroll summary
            if active_pane == "projects":
                if selected_project_idx > 0:
                    selected_project_idx -= 1
                    # Load tasks for new selection
                    tasks_file = projects[selected_project_idx].project_dir / "tasks.md"
                    tasks = parse_tasks_file(tasks_file)
                    selected_task_idx = 0
                    summary_scroll_offset = 0  # Reset summary scroll
                    needs_render = True
            elif active_pane == "summary":
                # Scroll summary pane up
                if summary_scroll_offset > 0:
                    summary_scroll_offset -= 1
                    needs_render = True
            else:  # tasks pane
                if selected_task_idx > 0:
                    selected_task_idx -= 1
                    needs_render = True

        elif key == curses.KEY_DOWN or key == ord('j') or key == ord('J'):
            # Move selection down or scroll summary
            if active_pane == "projects":
                if selected_project_idx < len(projects) - 1:
                    selected_project_idx += 1
                    # Load tasks for new selection
                    tasks_file = projects[selected_project_idx].project_dir / "tasks.md"
                    tasks = parse_tasks_file(tasks_file)
                    selected_task_idx = 0
                    summary_scroll_offset = 0  # Reset summary scroll
                    needs_render = True
            elif active_pane == "summary":
                # Scroll summary pane down (bounds-checked in render function)
                summary_scroll_offset += 1
                needs_render = True
            else:  # tasks pane
                if selected_task_idx < len(tasks) - 1:
                    selected_task_idx += 1
                    needs_render = True

        elif key == ord(' '):  # Space key
            # Toggle task completion (only in tasks pane)
            if active_pane == "tasks" and tasks and selected_task_idx < len(tasks):
                task = tasks[selected_task_idx]
                tasks_file = projects[selected_project_idx].project_dir / "tasks.md"
                if toggle_task_completion(tasks_file, task.line_number):
                    # Reload tasks
                    tasks = parse_tasks_file(tasks_file)
                    needs_render = True

        elif key == ord('d') or key == ord('D'):  # Delete key
            # Delete task (only in tasks pane)
            if active_pane == "tasks" and tasks and selected_task_idx < len(tasks):
                task = tasks[selected_task_idx]
                tasks_file = projects[selected_project_idx].project_dir / "tasks.md"

                # Delete the task and store for undo
                deleted_task = delete_task(tasks_file, task.line_number)

                if deleted_task:
                    # Add to deletion history
                    deletion_history.append(deleted_task)

                    # Reload tasks
                    tasks = parse_tasks_file(tasks_file)

                    # Adjust selection if needed
                    if selected_task_idx >= len(tasks):
                        selected_task_idx = max(0, len(tasks) - 1)

                    # Show feedback
                    stdscr.clear()
                    height, width = stdscr.getmaxyx()
                    msg = f"✓ Task deleted: {task.text[:50]}..."
                    stdscr.addstr(height // 2, (width - len(msg)) // 2, msg, curses.A_BOLD)
                    stdscr.refresh()
                    curses.napms(800)  # Show for 800ms
                    needs_render = True

        elif key == ord('u') or key == ord('U'):  # Undo key (context-aware)
            # PHASE 2: Context-aware undo - task deletion when in tasks pane, import undo otherwise
            if active_pane == "tasks" and deletion_history:
                # Undo last task deletion (original behavior)
                deleted_task = deletion_history.pop()

                if undo_task_deletion(deleted_task):
                    # Reload tasks
                    if projects:
                        tasks_file = projects[selected_project_idx].project_dir / "tasks.md"
                        tasks = parse_tasks_file(tasks_file)

                    # Show feedback
                    stdscr.clear()
                    height, width = stdscr.getmaxyx()
                    task_preview = deleted_task.content[0] if deleted_task.content else "Task"
                    # Extract task text from the line
                    import re
                    match = re.search(r'- \[.?\] (.+)', task_preview)
                    task_text = match.group(1)[:50] if match else task_preview[:50]
                    msg = f"✓ Task restored: {task_text}..."
                    stdscr.addstr(height // 2, (width - len(msg)) // 2, msg, curses.A_BOLD)
                    stdscr.refresh()
                    curses.napms(800)  # Show for 800ms
                    needs_render = True
            else:
                # Show import undo modal (new Phase 2 functionality)
                import_id_to_undo = render_import_history_modal(stdscr, projects_root)

                if import_id_to_undo:
                    # Perform undo
                    history_dir = projects_root / ".mission-control" / "history"
                    history = ImportHistory(history_dir)

                    result = history.undo_import(import_id_to_undo, projects_root)

                    # Show result
                    show_undo_result(stdscr, result)

                    if result.get('success'):
                        # Refresh projects after undo
                        all_projects = load_all_projects()
                        projects = apply_filter_and_sort(all_projects, filter_by, sort_by)

                        # Refresh tasks if in tasks pane
                        if projects and selected_project_idx < len(projects):
                            tasks_file = projects[selected_project_idx].project_dir / "tasks.md"
                            tasks = parse_tasks_file(tasks_file)

                needs_render = True

        elif key == ord('m') or key == ord('M'):  # Move task key
            # PHASE 3: Move task to another project (only in tasks pane)
            if active_pane == "tasks" and tasks and selected_task_idx < len(tasks):
                current_project = projects[selected_project_idx]
                task = tasks[selected_task_idx]
                tasks_file = current_project.project_dir / "tasks.md"

                # Show project picker
                dest_project_name = render_project_picker(
                    stdscr, all_projects, current_project.project_dir.name, action="move"
                )

                if dest_project_name:
                    # Initialize task manager
                    task_manager = TaskManager(projects_root)

                    # Get full task info for moving
                    task_to_move = task_manager.get_task_from_line(
                        tasks_file, task.text, current_project.project_dir.name
                    )

                    if task_to_move:
                        # Perform move
                        result = task_manager.move_task(task_to_move, dest_project_name)

                        # Show result
                        show_move_result(stdscr, result, action="move")

                        if result.get('success'):
                            # Reload projects and tasks
                            all_projects = load_all_projects()
                            projects = apply_filter_and_sort(all_projects, filter_by, sort_by)

                            # Reload tasks for current project
                            if projects and selected_project_idx < len(projects):
                                tasks_file = projects[selected_project_idx].project_dir / "tasks.md"
                                tasks = parse_tasks_file(tasks_file)

                                # Adjust selection
                                if selected_task_idx >= len(tasks):
                                    selected_task_idx = max(0, len(tasks) - 1)

                    needs_render = True

        elif key == ord('s') or key == ord('S'):
            # Cycle through sort options (only in projects pane)
            if active_pane == "projects":
                sort_options = ["priority", "category", "due_date", "last_updated", "name", "risk"]
                current_idx = sort_options.index(sort_by)
                next_idx = (current_idx + 1) % len(sort_options)
                sort_by = sort_options[next_idx]

                # Re-apply filter and sort
                projects = apply_filter_and_sort(all_projects, filter_by, sort_by)

                # Reset selection if needed
                if selected_project_idx >= len(projects):
                    selected_project_idx = max(0, len(projects) - 1)
                needs_render = True

        elif key == ord('f') or key == ord('F'):
            # Cycle through filter options (only in projects pane)
            if active_pane == "projects":
                filter_options = ["all", "active", "blocked", "work", "personal", "development", "family", "high"]
                current_idx = filter_options.index(filter_by)
                next_idx = (current_idx + 1) % len(filter_options)
                filter_by = filter_options[next_idx]

                # Re-apply filter and sort
                projects = apply_filter_and_sort(all_projects, filter_by, sort_by)

                # Reset selection
                selected_project_idx = 0
                if projects:
                    tasks_file = projects[selected_project_idx].project_dir / "tasks.md"
                    tasks = parse_tasks_file(tasks_file)
                    selected_task_idx = 0
                    summary_scroll_offset = 0
                needs_render = True

        elif key == ord('r') or key == ord('R'):
            # Refresh data
            try:
                all_projects = load_all_projects()
                projects = apply_filter_and_sort(all_projects, filter_by, sort_by)

                # Reset project selection if needed
                if selected_project_idx >= len(projects):
                    selected_project_idx = max(0, len(projects) - 1)

                # Reload tasks for selected project
                if projects:
                    tasks_file = projects[selected_project_idx].project_dir / "tasks.md"
                    tasks = parse_tasks_file(tasks_file)
                    selected_task_idx = 0

                # Show brief confirmation
                stdscr.addstr(0, 0, "Refreshed!", curses.A_BOLD)
                stdscr.refresh()
                curses.napms(500)  # Show for 500ms
                needs_render = True

            except Exception as e:
                stdscr.addstr(0, 0, f"Error refreshing: {e}", curses.A_BOLD)
                stdscr.refresh()
                curses.napms(2000)
                needs_render = True

        elif key == curses.KEY_HOME:
            # Go to first item in active pane
            if active_pane == "projects":
                selected_project_idx = 0
                # Reload tasks for new selection
                if projects:
                    tasks_file = projects[selected_project_idx].project_dir / "tasks.md"
                    tasks = parse_tasks_file(tasks_file)
                    selected_task_idx = 0
                    summary_scroll_offset = 0  # Reset summary scroll
                needs_render = True
            else:
                selected_task_idx = 0
                needs_render = True

        elif key == curses.KEY_END:
            # Go to last item in active pane
            if active_pane == "projects":
                selected_project_idx = len(projects) - 1
                # Reload tasks for new selection
                if projects:
                    tasks_file = projects[selected_project_idx].project_dir / "tasks.md"
                    tasks = parse_tasks_file(tasks_file)
                    selected_task_idx = 0
                    summary_scroll_offset = 0  # Reset summary scroll
                needs_render = True
            else:
                selected_task_idx = max(0, len(tasks) - 1)
                needs_render = True

        # [i] key disabled - will be repurposed for inbox in future phase
        # elif key == ord('i') or key == ord('I'):
        #     # PHASE 1: Staging/review workflow removed - imports now apply automatically
        #     # FUTURE: This key will be repurposed to open the inbox for unmatched content
        #     pass

        elif key == ord('n') or key == ord('N'):  # PHASE 4: Create new project
            # Show project creation modal
            project_params = render_project_create_modal(stdscr, projects_root)

            if project_params:
                # Create the project
                creator = ProjectCreator(projects_root)
                result = creator.create_project(
                    title=project_params['title'],
                    category=project_params['category'],
                    container=project_params['container'],
                    priority=project_params['priority'],
                    owner=project_params['owner'],
                    description=project_params['description']
                )

                # Show result
                show_project_create_result(stdscr, result)

                # Refresh project list if successful
                if result.get('success'):
                    all_projects = load_all_projects()
                    projects = apply_filter_and_sort(all_projects, filter_by, sort_by)

                    # Try to select the newly created project
                    new_project_name = result.get('project_name')
                    if new_project_name:
                        for i, proj in enumerate(projects):
                            if proj.project_dir.name == new_project_name:
                                selected_project_idx = i
                                # Load tasks for new project
                                tasks_file = projects[selected_project_idx].project_dir / "tasks.md"
                                tasks = parse_tasks_file(tasks_file)
                                selected_task_idx = 0
                                summary_scroll_offset = 0
                                break

                needs_render = True

        elif key == ord('?'):
            # Show help modal
            render_help_modal(stdscr)
            needs_render = True


def main():
    """Main entry point"""
    try:
        curses.wrapper(main_loop)
    except KeyboardInterrupt:
        print("\nExiting Mission Control...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
