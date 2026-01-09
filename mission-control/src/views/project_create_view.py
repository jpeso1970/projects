"""
Project creation modal view - form for creating new projects.
"""
import curses
from pathlib import Path
from typing import Optional, Dict, List

from .dashboard import COLOR_HEADER, COLOR_ACTIVE, COLOR_STALE, COLOR_BLOCKED


def render_project_create_modal(stdscr, projects_dir: Path) -> Optional[Dict]:
    """
    Render project creation form modal.

    Args:
        stdscr: Curses screen object
        projects_dir: Root projects directory

    Returns:
        Dict with project parameters, or None if cancelled
    """
    # Get available categories and containers
    from ..project_creator import ProjectCreator
    creator = ProjectCreator(projects_dir)

    categories = ["work", "personal", "development", "family"]
    priorities = ["high", "medium", "low"]

    # Form state
    fields = {
        "title": "",
        "category": "work",
        "container": "",
        "priority": "medium",
        "owner": "Jason Pace",
        "description": ""
    }

    field_order = ["title", "category", "container", "priority", "owner", "description"]
    selected_field_idx = 0
    editing_field = None
    cursor_pos = 0
    error_message = None

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Calculate modal dimensions
        modal_width = min(80, width - 4)
        modal_height = min(28, height - 4)
        start_x = (width - modal_width) // 2
        start_y = (height - modal_height) // 2

        # Draw border
        _draw_modal_border(stdscr, start_x, start_y, modal_width, modal_height)

        # Title
        title = " Create New Project "
        title_x = start_x + (modal_width - len(title)) // 2
        try:
            stdscr.addstr(start_y, title_x, title,
                         curses.color_pair(COLOR_HEADER) | curses.A_BOLD)
        except curses.error:
            pass

        # Instructions
        line_y = start_y + 2
        content_x = start_x + 3

        instructions = "↑/↓: Navigate | Enter: Edit field | Tab: Next field | Ctrl+G: Create | q: Cancel"
        try:
            stdscr.addstr(line_y, content_x, instructions[:modal_width-6],
                         curses.color_pair(COLOR_STALE))
            line_y += 2
        except curses.error:
            pass

        # Render form fields
        for idx, field_name in enumerate(field_order):
            if line_y >= start_y + modal_height - 5:
                break

            is_selected = (idx == selected_field_idx)
            is_editing = (editing_field == field_name)

            try:
                # Field label
                label = _get_field_label(field_name)
                label_display = f"{label}:"

                attr = curses.A_BOLD if is_selected else curses.A_NORMAL
                if is_selected:
                    attr |= curses.color_pair(COLOR_ACTIVE)

                stdscr.addstr(line_y, content_x, label_display, attr)

                # Field value
                value_x = content_x + 18
                max_value_width = modal_width - 25

                if field_name == "category":
                    # Show all categories with current highlighted
                    value_display = " | ".join([
                        f"[{cat}]" if cat == fields[field_name] else cat
                        for cat in categories
                    ])
                elif field_name == "priority":
                    # Show all priorities with current highlighted
                    value_display = " | ".join([
                        f"[{pri}]" if pri == fields[field_name] else pri
                        for pri in priorities
                    ])
                elif field_name == "container":
                    # Show available containers or "root"
                    if fields[field_name]:
                        value_display = fields[field_name]
                    else:
                        available = creator.get_available_containers(fields["category"])
                        if available:
                            value_display = f"(root) - Options: {', '.join(available[:3])}"
                        else:
                            value_display = "(root)"
                else:
                    value_display = fields[field_name] or "(empty)"

                # Truncate if too long
                if len(value_display) > max_value_width:
                    value_display = value_display[:max_value_width-3] + "..."

                # Show cursor if editing
                if is_editing:
                    # Show editable value with cursor
                    edit_value = fields[field_name]
                    if cursor_pos <= len(edit_value):
                        before_cursor = edit_value[:cursor_pos]
                        cursor_char = edit_value[cursor_pos] if cursor_pos < len(edit_value) else " "
                        after_cursor = edit_value[cursor_pos+1:] if cursor_pos < len(edit_value) else ""

                        stdscr.addstr(line_y, value_x, before_cursor)
                        stdscr.addstr(line_y, value_x + len(before_cursor), cursor_char,
                                    curses.A_REVERSE | curses.color_pair(COLOR_ACTIVE))
                        if after_cursor:
                            stdscr.addstr(line_y, value_x + len(before_cursor) + 1, after_cursor)
                    else:
                        stdscr.addstr(line_y, value_x, edit_value)
                        stdscr.addstr(line_y, value_x + len(edit_value), " ",
                                    curses.A_REVERSE | curses.color_pair(COLOR_ACTIVE))
                else:
                    stdscr.addstr(line_y, value_x, value_display)

                line_y += 1

                # Add hint for complex fields
                if is_selected and not is_editing:
                    hint = _get_field_hint(field_name, fields)
                    if hint:
                        stdscr.addstr(line_y, content_x + 2, f"→ {hint}",
                                    curses.color_pair(COLOR_STALE))
                        line_y += 1

                line_y += 1  # Spacing between fields

            except curses.error:
                pass

        # Error message
        if error_message:
            error_y = start_y + modal_height - 4
            error_x = content_x
            try:
                stdscr.addstr(error_y, error_x, f"✗ {error_message[:modal_width-10]}",
                            curses.color_pair(COLOR_BLOCKED) | curses.A_BOLD)
            except curses.error:
                pass

        # Footer
        footer = "Ctrl+G to create project"
        footer_x = start_x + (modal_width - len(footer)) // 2
        try:
            stdscr.addstr(start_y + modal_height - 2, footer_x, footer,
                         curses.color_pair(COLOR_STALE))
        except curses.error:
            pass

        stdscr.refresh()

        # Handle input
        key = stdscr.getch()

        if editing_field:
            # Handle editing mode
            if key == 27:  # ESC - exit editing
                editing_field = None
                error_message = None

            elif key == ord('\n') or key == curses.KEY_ENTER or key == 10 or key == 13:
                # Done editing
                editing_field = None
                error_message = None

            elif key == curses.KEY_BACKSPACE or key == 127 or key == 8:
                # Backspace
                if cursor_pos > 0:
                    field_value = fields[editing_field]
                    fields[editing_field] = field_value[:cursor_pos-1] + field_value[cursor_pos:]
                    cursor_pos -= 1

            elif key == curses.KEY_DC:  # Delete
                field_value = fields[editing_field]
                if cursor_pos < len(field_value):
                    fields[editing_field] = field_value[:cursor_pos] + field_value[cursor_pos+1:]

            elif key == curses.KEY_LEFT:
                cursor_pos = max(0, cursor_pos - 1)

            elif key == curses.KEY_RIGHT:
                cursor_pos = min(len(fields[editing_field]), cursor_pos + 1)

            elif key == curses.KEY_HOME:
                cursor_pos = 0

            elif key == curses.KEY_END:
                cursor_pos = len(fields[editing_field])

            elif 32 <= key <= 126:  # Printable characters
                char = chr(key)
                field_value = fields[editing_field]
                fields[editing_field] = field_value[:cursor_pos] + char + field_value[cursor_pos:]
                cursor_pos += 1

        else:
            # Handle navigation mode
            if key == curses.KEY_UP or key == ord('k'):
                selected_field_idx = max(0, selected_field_idx - 1)
                error_message = None

            elif key == curses.KEY_DOWN or key == ord('j'):
                selected_field_idx = min(len(field_order) - 1, selected_field_idx + 1)
                error_message = None

            elif key == ord('\t'):  # Tab - next field
                selected_field_idx = (selected_field_idx + 1) % len(field_order)
                error_message = None

            elif key == ord('\n') or key == curses.KEY_ENTER or key == 10 or key == 13:
                # Enter - edit selected field or cycle options
                current_field = field_order[selected_field_idx]

                if current_field == "category":
                    # Cycle through categories
                    current_idx = categories.index(fields["category"])
                    fields["category"] = categories[(current_idx + 1) % len(categories)]
                    # Reset container when category changes
                    fields["container"] = ""

                elif current_field == "priority":
                    # Cycle through priorities
                    current_idx = priorities.index(fields["priority"])
                    fields["priority"] = priorities[(current_idx + 1) % len(priorities)]

                elif current_field == "container":
                    # Cycle through available containers or allow typing
                    available = creator.get_available_containers(fields["category"])
                    if available:
                        if not fields["container"]:
                            fields["container"] = available[0]
                        else:
                            try:
                                current_idx = available.index(fields["container"])
                                next_idx = (current_idx + 1) % (len(available) + 1)
                                fields["container"] = available[next_idx] if next_idx < len(available) else ""
                            except ValueError:
                                fields["container"] = ""
                    else:
                        # Allow typing custom container
                        editing_field = current_field
                        cursor_pos = len(fields[current_field])

                else:
                    # Start editing
                    editing_field = current_field
                    cursor_pos = len(fields[current_field])

                error_message = None

            elif key == 7:  # Ctrl+G - Create project
                # Validate and create
                validation_error = _validate_fields(fields)
                if validation_error:
                    error_message = validation_error
                else:
                    return fields

            elif key == ord('q') or key == ord('Q'):
                return None

        stdscr.timeout(100)

    return None


def show_project_create_result(stdscr, result: Dict):
    """
    Show result of project creation.

    Args:
        stdscr: Curses screen object
        result: Result dict from ProjectCreator
    """
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    y = height // 2 - 6
    x_center = width // 2

    if result.get('success'):
        title = "✓ Project Created Successfully!"
        title_color = COLOR_ACTIVE
    else:
        title = "✗ Project Creation Failed"
        title_color = COLOR_BLOCKED

    try:
        stdscr.addstr(y, x_center - len(title) // 2, title,
                     curses.color_pair(title_color) | curses.A_BOLD)
        y += 2

        if result.get('success'):
            lines = [
                f"Name: {result.get('project_name', 'Unknown')}",
                "",
                f"Location: {result.get('project_path', 'Unknown')}",
                "",
                "Files created:",
                "  • PROJECT.md",
                "  • tasks.md",
                "  • timeline.md",
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


def _get_field_label(field_name: str) -> str:
    """Get display label for field"""
    labels = {
        "title": "Project Title",
        "category": "Category",
        "container": "Container",
        "priority": "Priority",
        "owner": "Owner",
        "description": "Description"
    }
    return labels.get(field_name, field_name.capitalize())


def _get_field_hint(field_name: str, fields: Dict) -> Optional[str]:
    """Get hint text for field"""
    if field_name == "title":
        return "Human-readable project name"
    elif field_name == "category":
        return "Press Enter to cycle"
    elif field_name == "container":
        from pathlib import Path
        # This is a bit hacky but works for hints
        return "Press Enter to cycle, or type custom name"
    elif field_name == "priority":
        return "Press Enter to cycle"
    elif field_name == "description":
        return "Optional project description"
    return None


def _validate_fields(fields: Dict) -> Optional[str]:
    """
    Validate form fields.

    Args:
        fields: Form field values

    Returns:
        Error message if invalid, None if valid
    """
    if not fields.get("title"):
        return "Title is required"

    if not fields.get("category"):
        return "Category is required"

    if not fields.get("owner"):
        return "Owner is required"

    # Title should not be too short
    if len(fields["title"].strip()) < 3:
        return "Title must be at least 3 characters"

    # Title should not have special characters that would break slugification
    import re
    if not re.match(r'^[a-zA-Z0-9\s\-_]+$', fields["title"]):
        return "Title can only contain letters, numbers, spaces, hyphens, and underscores"

    return None
