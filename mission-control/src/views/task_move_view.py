"""
Task move view - project picker modal for moving/copying tasks.
"""
import curses
from pathlib import Path
from typing import Optional, List

from .dashboard import COLOR_HEADER, COLOR_ACTIVE, COLOR_STALE


def render_project_picker(stdscr, projects: List, current_project_name: str,
                         action: str = "move") -> Optional[str]:
    """
    Render project picker modal for moving/copying tasks.

    Args:
        stdscr: Curses screen object
        projects: List of Project objects to choose from
        current_project_name: Name of current project (will be excluded)
        action: "move" or "copy"

    Returns:
        Selected project name, or None if cancelled
    """
    # Filter out current project
    available_projects = [p for p in projects if p.name != current_project_name]

    if not available_projects:
        _show_no_projects_message(stdscr, action)
        return None

    # Sort by category then name for easier browsing
    available_projects.sort(key=lambda p: (p.category, p.name))

    selected_idx = 0

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Calculate modal dimensions
        modal_width = min(70, width - 4)
        modal_height = min(30, height - 4)
        start_x = (width - modal_width) // 2
        start_y = (height - modal_height) // 2

        # Draw border
        _draw_modal_border(stdscr, start_x, start_y, modal_width, modal_height)

        # Title
        title = f" {action.capitalize()} Task To... "
        title_x = start_x + (modal_width - len(title)) // 2
        try:
            stdscr.addstr(start_y, title_x, title,
                         curses.color_pair(COLOR_HEADER) | curses.A_BOLD)
        except curses.error:
            pass

        # Instructions
        line_y = start_y + 2
        content_x = start_x + 3

        instructions = f"↑/↓ or j/k: Navigate | Enter: {action.capitalize()} here | q: Cancel"
        try:
            stdscr.addstr(line_y, content_x, instructions[:modal_width-6],
                         curses.color_pair(COLOR_STALE))
            line_y += 2
        except curses.error:
            pass

        # Render project list
        max_visible = modal_height - 8
        scroll_offset = max(0, selected_idx - max_visible + 1)

        last_category = None

        for idx, project in enumerate(available_projects[scroll_offset:scroll_offset + max_visible]):
            actual_idx = idx + scroll_offset
            is_selected = (actual_idx == selected_idx)

            if line_y >= start_y + modal_height - 3:
                break

            try:
                # Show category separator
                if project.category != last_category:
                    if last_category is not None:
                        line_y += 1  # Extra space between categories

                    if line_y < start_y + modal_height - 3:
                        category_line = f"── {project.category.upper()} ──"
                        stdscr.addstr(line_y, content_x, category_line[:modal_width-6],
                                     curses.color_pair(COLOR_HEADER))
                        line_y += 1
                        last_category = project.category

                if line_y >= start_y + modal_height - 3:
                    break

                # Render project entry
                _render_project_entry(
                    stdscr, project, line_y, content_x,
                    modal_width - 6, is_selected
                )
                line_y += 1

            except curses.error:
                pass

        # Footer with count
        footer = f"{len(available_projects)} projects available"
        footer_x = start_x + (modal_width - len(footer)) // 2
        try:
            stdscr.addstr(start_y + modal_height - 2, footer_x, footer,
                         curses.color_pair(COLOR_STALE))
        except curses.error:
            pass

        stdscr.refresh()

        # Handle input
        key = stdscr.getch()

        if key == curses.KEY_UP or key == ord('k'):
            selected_idx = max(0, selected_idx - 1)

        elif key == curses.KEY_DOWN or key == ord('j'):
            selected_idx = min(len(available_projects) - 1, selected_idx + 1)

        elif key == ord('\n') or key == curses.KEY_ENTER or key == 10 or key == 13:
            # Return selected project name
            return available_projects[selected_idx].name

        elif key == ord('q') or key == ord('Q'):
            return None


def show_move_result(stdscr, result: dict, action: str = "move"):
    """
    Show result of move/copy operation.

    Args:
        stdscr: Curses screen object
        result: Result dict from TaskManager
        action: "move" or "copy"
    """
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    y = height // 2 - 4
    x_center = width // 2

    if result.get('success'):
        title = f"✓ Task {action.capitalize()}d Successfully"
        title_color = COLOR_ACTIVE
    else:
        title = f"✗ {action.capitalize()} Failed"
        title_color = COLOR_HEADER

    try:
        stdscr.addstr(y, x_center - len(title) // 2, title,
                     curses.color_pair(title_color) | curses.A_BOLD)
        y += 2

        if result.get('success'):
            # Show task preview
            task_preview = result.get('task_text', 'Task')[:50]
            lines = [
                f"Task: {task_preview}{'...' if len(result.get('task_text', '')) > 50 else ''}",
                "",
                f"From: {result.get('source_project', 'Unknown')}",
                f"To:   {result.get('dest_project', 'Unknown')}"
            ]
        else:
            lines = [
                f"Error: {result.get('error', 'Unknown error')}"
            ]

        for line in lines:
            if y >= height - 3:
                break
            stdscr.addstr(y, x_center - len(line) // 2, line)
            y += 1

        y += 2
        prompt = "Press any key to continue..."
        stdscr.addstr(y, x_center - len(prompt) // 2, prompt,
                     curses.color_pair(COLOR_STALE))

    except curses.error:
        pass

    stdscr.refresh()
    stdscr.getch()


def show_bulk_move_result(stdscr, summary: dict, action: str = "move"):
    """
    Show result of bulk move/copy operation.

    Args:
        stdscr: Curses screen object
        summary: Summary dict from TaskManager.move_multiple_tasks()
        action: "move" or "copy"
    """
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    y = height // 2 - 5
    x_center = width // 2

    if summary.get('moved', 0) > 0:
        title = f"✓ {summary['moved']}/{summary['total']} Tasks {action.capitalize()}d"
        title_color = COLOR_ACTIVE
    else:
        title = f"✗ {action.capitalize()} Failed"
        title_color = COLOR_HEADER

    try:
        stdscr.addstr(y, x_center - len(title) // 2, title,
                     curses.color_pair(title_color) | curses.A_BOLD)
        y += 2

        lines = [
            f"Total: {summary['total']}",
            f"{action.capitalize()}d: {summary['moved']}",
            f"Failed: {summary['failed']}"
        ]

        if summary.get('errors'):
            lines.append("")
            lines.append("Errors:")
            for error in summary['errors'][:3]:  # Show first 3 errors
                lines.append(f"  • {error[:60]}")

        for line in lines:
            if y >= height - 3:
                break
            stdscr.addstr(y, x_center - len(line) // 2, line)
            y += 1

        y += 2
        prompt = "Press any key to continue..."
        stdscr.addstr(y, x_center - len(prompt) // 2, prompt,
                     curses.color_pair(COLOR_STALE))

    except curses.error:
        pass

    stdscr.refresh()
    stdscr.getch()


def _show_no_projects_message(stdscr, action: str):
    """Show message when no projects available"""
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    y = height // 2
    x_center = width // 2

    message = f"No other projects available to {action} to"
    try:
        stdscr.addstr(y, x_center - len(message) // 2, message,
                     curses.color_pair(COLOR_HEADER) | curses.A_BOLD)

        prompt = "Press any key to continue..."
        stdscr.addstr(y + 2, x_center - len(prompt) // 2, prompt,
                     curses.color_pair(COLOR_STALE))
    except curses.error:
        pass

    stdscr.refresh()
    stdscr.getch()


def _draw_modal_border(stdscr, start_x: int, start_y: int,
                       modal_width: int, modal_height: int):
    """Draw modal border"""
    for y in range(start_y, start_y + modal_height):
        try:
            stdscr.addstr(y, start_x, "│", curses.color_pair(COLOR_HEADER))
            stdscr.addstr(y, start_x + modal_width - 1, "│",
                         curses.color_pair(COLOR_HEADER))
        except curses.error:
            pass

    try:
        stdscr.addstr(start_y, start_x, "╭" + "─" * (modal_width - 2) + "╮",
                     curses.color_pair(COLOR_HEADER))
        stdscr.addstr(start_y + modal_height - 1, start_x,
                     "╰" + "─" * (modal_width - 2) + "╯",
                     curses.color_pair(COLOR_HEADER))
    except curses.error:
        pass


def _render_project_entry(stdscr, project, y: int, x: int,
                          max_width: int, is_selected: bool):
    """Render a single project entry"""
    # Format: "  project-name (status)"
    status_indicator = project.status[:4] if hasattr(project, 'status') else ''
    line = f"  {project.name}"

    if status_indicator:
        line += f" ({status_indicator})"

    if len(line) > max_width:
        line = line[:max_width-3] + "..."

    attr = curses.A_REVERSE if is_selected else curses.A_NORMAL
    if is_selected:
        attr |= curses.color_pair(COLOR_ACTIVE)

    try:
        stdscr.addstr(y, x, line, attr)
    except curses.error:
        pass
