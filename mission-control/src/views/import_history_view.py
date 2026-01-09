"""
Import history view - shows recent imports with undo functionality.
"""
import curses
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict

from .dashboard import COLOR_HEADER, COLOR_ACTIVE, COLOR_STALE, COLOR_BLOCKED


def render_import_history_modal(stdscr, projects_dir: Path) -> Optional[str]:
    """
    Render modal showing recent imports with undo functionality.

    Args:
        stdscr: Curses screen object
        projects_dir: Root projects directory

    Returns:
        Import ID to undo, or None if cancelled
    """
    try:
        from ..import_history import ImportHistory
    except ImportError:
        from import_history import ImportHistory

    history_dir = projects_dir / ".mission-control" / "history"
    history = ImportHistory(history_dir)

    # Get recent imports
    recent_imports = history.get_recent_imports(include_undone=False)

    if not recent_imports:
        # No imports to undo
        _show_no_imports_message(stdscr)
        return None

    # Show interactive list
    selected_idx = 0

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Calculate modal dimensions
        modal_width = min(80, width - 4)
        modal_height = min(25, height - 4)
        start_x = (width - modal_width) // 2
        start_y = (height - modal_height) // 2

        # Draw border
        _draw_modal_border(stdscr, start_x, start_y, modal_width, modal_height)

        # Title
        title = " Recent Imports - Undo History "
        title_x = start_x + (modal_width - len(title)) // 2
        try:
            stdscr.addstr(start_y, title_x, title,
                         curses.color_pair(COLOR_HEADER) | curses.A_BOLD)
        except curses.error:
            pass

        # Instructions
        line_y = start_y + 2
        content_x = start_x + 3

        try:
            stdscr.addstr(line_y, content_x,
                         "↑/↓: Navigate | Enter: Undo selected | q: Cancel",
                         curses.color_pair(COLOR_STALE))
            line_y += 2
        except curses.error:
            pass

        # Render import list
        max_visible = modal_height - 8
        scroll_offset = max(0, selected_idx - max_visible + 1)

        for idx, import_entry in enumerate(recent_imports[scroll_offset:scroll_offset + max_visible]):
            actual_idx = idx + scroll_offset
            is_selected = (actual_idx == selected_idx)

            if line_y >= start_y + modal_height - 3:
                break

            try:
                _render_import_entry(
                    stdscr, import_entry, line_y, content_x,
                    modal_width - 6, is_selected
                )
                line_y += 3

            except curses.error:
                pass

        # Footer
        footer = f"Showing {len(recent_imports)} recent imports"
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
            selected_idx = min(len(recent_imports) - 1, selected_idx + 1)

        elif key == ord('\n') or key == curses.KEY_ENTER or key == 10 or key == 13:
            # Confirm undo
            import_id = recent_imports[selected_idx]['id']
            if _confirm_undo(stdscr, recent_imports[selected_idx]):
                return import_id
            # If not confirmed, continue loop

        elif key == ord('q') or key == ord('Q'):
            return None


def _show_no_imports_message(stdscr):
    """Show message when no imports available to undo"""
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    y = height // 2
    x_center = width // 2

    message = "No recent imports to undo"
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


def _render_import_entry(stdscr, entry: Dict, y: int, x: int,
                        max_width: int, is_selected: bool):
    """Render a single import entry"""
    # Parse timestamp
    timestamp_str = entry.get('timestamp', '')
    try:
        dt = datetime.fromisoformat(timestamp_str)
        time_ago = _format_time_ago(dt)
    except Exception:
        time_ago = "Unknown time"

    # First line: filename and time
    filename = entry.get('source_file', 'Unknown file')
    first_line = f"{time_ago}: {filename}"
    if len(first_line) > max_width:
        first_line = first_line[:max_width-3] + "..."

    attr = curses.A_REVERSE if is_selected else curses.A_NORMAL
    if is_selected:
        attr |= curses.color_pair(COLOR_ACTIVE)

    try:
        stdscr.addstr(y, x, first_line, attr)
    except curses.error:
        pass

    # Second line: changes summary
    changes = entry.get('changes', [])
    total_tasks = sum(len(c.get('tasks_added', [])) for c in changes)
    total_decisions = sum(len(c.get('decisions_added', [])) for c in changes)
    total_updates = sum(len(c.get('updates_added', [])) for c in changes)
    projects = {c.get('project_name') for c in changes}

    summary_parts = []
    if total_tasks:
        summary_parts.append(f"{total_tasks} task(s)")
    if total_decisions:
        summary_parts.append(f"{total_decisions} decision(s)")
    if total_updates:
        summary_parts.append(f"{total_updates} update(s)")

    summary = f"  → {', '.join(summary_parts)} to {len(projects)} project(s)"

    try:
        stdscr.addstr(y + 1, x, summary[:max_width],
                     curses.color_pair(COLOR_STALE) if not is_selected else attr)
    except curses.error:
        pass


def _format_time_ago(dt: datetime) -> str:
    """Format datetime as relative time"""
    now = datetime.now()
    delta = now - dt

    seconds = delta.total_seconds()

    if seconds < 60:
        return "Just now"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes} min ago"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours} hour(s) ago"
    else:
        days = int(seconds / 86400)
        return f"{days} day(s) ago"


def _confirm_undo(stdscr, import_entry: Dict) -> bool:
    """
    Show confirmation dialog for undo operation.

    Args:
        stdscr: Curses screen object
        import_entry: Import entry to undo

    Returns:
        True if confirmed, False if cancelled
    """
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    # Modal dimensions
    modal_width = min(70, width - 4)
    modal_height = 15
    start_x = (width - modal_width) // 2
    start_y = (height - modal_height) // 2

    # Draw border
    _draw_modal_border(stdscr, start_x, start_y, modal_width, modal_height)

    # Title
    title = " Confirm Undo "
    title_x = start_x + (modal_width - len(title)) // 2
    try:
        stdscr.addstr(start_y, title_x, title,
                     curses.color_pair(COLOR_BLOCKED) | curses.A_BOLD)
    except curses.error:
        pass

    # Content
    line_y = start_y + 2
    content_x = start_x + 3

    lines = [
        f"Undo import: {import_entry.get('source_file', 'Unknown')}",
        "",
        "This will:",
        "  • Remove all tasks, decisions, and updates that were added",
        "  • Restore the original file to the import directory",
        "  • Cannot be undone",
        "",
        "Continue?",
        "",
        "[Y]es    [N]o"
    ]

    for line in lines:
        if line_y >= start_y + modal_height - 2:
            break

        try:
            if line.startswith(" "):
                attr = curses.color_pair(COLOR_STALE)
            elif line.startswith("["):
                attr = curses.color_pair(COLOR_ACTIVE) | curses.A_BOLD
            else:
                attr = curses.A_NORMAL

            stdscr.addstr(line_y, content_x, line[:modal_width-6], attr)
            line_y += 1
        except curses.error:
            pass

    stdscr.refresh()

    # Wait for confirmation
    while True:
        key = stdscr.getch()

        if key == ord('y') or key == ord('Y'):
            return True
        elif key == ord('n') or key == ord('N') or key == ord('q') or key == ord('Q'):
            return False


def show_undo_result(stdscr, result: Dict):
    """
    Show result of undo operation.

    Args:
        stdscr: Curses screen object
        result: Result dict from ImportHistory.undo_import()
    """
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    y = height // 2 - 5
    x_center = width // 2

    if result.get('success'):
        title = "✓ Import Undone Successfully"
        title_color = COLOR_ACTIVE
    else:
        title = "✗ Undo Failed"
        title_color = COLOR_BLOCKED

    try:
        stdscr.addstr(y, x_center - len(title) // 2, title,
                     curses.color_pair(title_color) | curses.A_BOLD)
        y += 2

        if result.get('success'):
            lines = [
                f"File: {result.get('source_file', 'Unknown')}",
                "",
                f"Removed: {result.get('tasks_removed', 0)} tasks",
                f"         {result.get('decisions_removed', 0)} decisions",
                f"         {result.get('updates_removed', 0)} updates",
                "",
                f"Projects affected: {len(result.get('projects_affected', []))}"
            ]

            if result.get('file_restored'):
                lines.append("")
                lines.append("✓ Original file restored to import directory")

            if result.get('errors'):
                lines.append("")
                lines.append("Warnings:")
                for error in result['errors'][:3]:  # Show first 3 errors
                    lines.append(f"  • {error[:60]}")

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
