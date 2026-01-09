#!/usr/bin/env python3
"""
Mission Control - Main application entry point.
"""
import curses
import sys
import time
from pathlib import Path

from .loader import load_all_projects, sort_projects
from .views.dashboard import render_dashboard, init_colors
from .views.split_view import render_split_view
from .views.three_pane_view import render_three_pane_view
from .views.imports_view import render_imports_modal, process_imports_with_feedback
from .views.review_view import render_review_modal
from .task_parser import parse_tasks_file, toggle_task_completion, delete_task, undo_task_deletion
from .import_processor import create_import_dir_readme, ImportProcessor
from .staging import StagingManager


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
    active_pane = "projects"  # Can be: "projects" or "tasks" (summary is view-only)
    sort_by = "priority"  # Can be: priority, category, due_date, last_updated, name, risk
    deletion_history = []  # Stack of deleted tasks for undo
    last_import_check = time.time()  # Track last auto-import check
    auto_import_interval = 30  # Check for imports every 30 seconds
    summary_scroll_offset = 0  # Scroll position for summary pane

    # Sort projects initially
    projects = sort_projects(projects, sort_by)

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
                        projects = load_all_projects()
                        projects = sort_projects(projects, sort_by)
                        needs_render = True  # Need to re-render after import
                except Exception as e:
                    # Silent fail - don't interrupt user
                    pass

        # Only render if something changed
        if needs_render:
            render_three_pane_view(stdscr, projects, tasks, selected_project_idx,
                                  selected_task_idx, active_pane, sort_by, summary_scroll_offset)
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
            # Toggle between projects and tasks (summary is view-only)
            if active_pane == "projects":
                active_pane = "tasks"
            else:  # tasks or summary
                active_pane = "projects"
            needs_render = True

        elif key == curses.KEY_UP or key == ord('k'):
            # Move selection up
            if active_pane == "projects":
                if selected_project_idx > 0:
                    selected_project_idx -= 1
                    # Load tasks for new selection
                    tasks_file = projects[selected_project_idx].project_dir / "tasks.md"
                    tasks = parse_tasks_file(tasks_file)
                    selected_task_idx = 0
                    summary_scroll_offset = 0  # Reset summary scroll
                    needs_render = True
            else:  # tasks pane
                if selected_task_idx > 0:
                    selected_task_idx -= 1
                    needs_render = True

        elif key == curses.KEY_DOWN or key == ord('j'):
            # Move selection down
            if active_pane == "projects":
                if selected_project_idx < len(projects) - 1:
                    selected_project_idx += 1
                    # Load tasks for new selection
                    tasks_file = projects[selected_project_idx].project_dir / "tasks.md"
                    tasks = parse_tasks_file(tasks_file)
                    selected_task_idx = 0
                    summary_scroll_offset = 0  # Reset summary scroll
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

        elif key == ord('u') or key == ord('U'):  # Undo key
            # Undo last deletion
            if deletion_history:
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
                # No deletions to undo
                stdscr.clear()
                height, width = stdscr.getmaxyx()
                msg = "No deletions to undo"
                stdscr.addstr(height // 2, (width - len(msg)) // 2, msg, curses.A_BOLD)
                stdscr.refresh()
                curses.napms(500)
                needs_render = True

        elif key == ord('s') or key == ord('S'):
            # Cycle through sort options (only in projects pane)
            if active_pane == "projects":
                sort_options = ["priority", "category", "due_date", "last_updated", "name", "risk"]
                current_idx = sort_options.index(sort_by)
                next_idx = (current_idx + 1) % len(sort_options)
                sort_by = sort_options[next_idx]

                # Re-sort projects
                projects = sort_projects(projects, sort_by)

                # Reset selection if needed
                if selected_project_idx >= len(projects):
                    selected_project_idx = len(projects) - 1
                needs_render = True

        elif key == ord('r') or key == ord('R'):
            # Refresh data
            try:
                projects = load_all_projects()
                projects = sort_projects(projects, sort_by)

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

        elif key == ord('[') or key == curses.KEY_PPAGE:
            # Scroll summary pane up (when in projects pane)
            if active_pane == "projects":
                if summary_scroll_offset > 0:
                    summary_scroll_offset -= 1
                    needs_render = True

        elif key == ord(']') or key == curses.KEY_NPAGE:
            # Scroll summary pane down (when in projects pane)
            if active_pane == "projects":
                # Allow scrolling down (will be bounds-checked in render function)
                summary_scroll_offset += 1
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

        elif key == ord('i') or key == ord('I'):
            # Review workflow: Check for pending staged analyses first
            staging_dir = projects_root / ".mission-control" / "staging"
            staging_manager = StagingManager(staging_dir)
            pending = staging_manager.get_pending_analyses()

            if pending:
                # Show review modal for pending analyses
                try:
                    result = render_review_modal(stdscr, staging_manager)

                    if result == 'processed':
                        # Apply approved analyses
                        stdscr.clear()
                        height, width = stdscr.getmaxyx()
                        stdscr.addstr(height // 2, (width - 30) // 2,
                                     "Applying approved changes...",
                                     curses.A_BOLD)
                        stdscr.refresh()

                        processor = ImportProcessor(import_dir, projects_root)
                        apply_summary = processor.apply_approved_analyses()

                        # Show results
                        stdscr.clear()
                        y = height // 2 - 5
                        x_center = width // 2

                        title = "✓ Changes Applied"
                        stdscr.addstr(y, x_center - len(title) // 2, title,
                                     curses.A_BOLD)
                        y += 2

                        results = [
                            f"Tasks added: {apply_summary['tasks_added']}",
                            f"Decisions added: {apply_summary['decisions_added']}",
                            f"Updates applied: {apply_summary['updates_applied']}",
                            f"Projects updated: {len(apply_summary['projects_updated'])}"
                        ]

                        for result_text in results:
                            stdscr.addstr(y, x_center - len(result_text) // 2, result_text)
                            y += 1

                        y += 2
                        prompt = "Press any key to continue..."
                        stdscr.addstr(y, x_center - len(prompt) // 2, prompt)
                        stdscr.refresh()
                        stdscr.getch()

                        # Refresh projects
                        projects = load_all_projects()
                        projects = sort_projects(projects, sort_by)
                        needs_render = True

                except Exception as e:
                    stdscr.clear()
                    height, width = stdscr.getmaxyx()
                    stdscr.addstr(height // 2, (width - 40) // 2,
                                 f"Error: {str(e)[:40]}", curses.A_BOLD)
                    stdscr.refresh()
                    curses.napms(2000)
                    needs_render = True
            else:
                # No pending analyses, show import processing modal
                should_process = render_imports_modal(stdscr, import_dir, projects_root)
                if should_process:
                    process_imports_with_feedback(stdscr, import_dir, projects_root)
                    # Refresh projects in case new meeting notes were added
                    projects = load_all_projects()
                    projects = sort_projects(projects, sort_by)
                if selected_project_idx >= len(projects):
                    selected_project_idx = max(0, len(projects) - 1)
                needs_render = True

        elif key == ord('?'):
            # Show help (future)
            pass


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
