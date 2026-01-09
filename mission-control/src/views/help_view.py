"""
Help modal view for Mission Control.
"""
import curses

from .dashboard import COLOR_HEADER, COLOR_ACTIVE, COLOR_STALE


def render_help_modal(stdscr):
    """
    Render a help modal showing all keybindings.

    Args:
        stdscr: Curses window object
    """
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    # Calculate modal dimensions
    modal_width = min(70, width - 4)
    modal_height = min(30, height - 4)
    start_x = (width - modal_width) // 2
    start_y = (height - modal_height) // 2

    # Draw border
    for y in range(start_y, start_y + modal_height):
        try:
            stdscr.addstr(y, start_x, "│", curses.color_pair(COLOR_HEADER))
            stdscr.addstr(y, start_x + modal_width - 1, "│", curses.color_pair(COLOR_HEADER))
        except curses.error:
            pass

    try:
        stdscr.addstr(start_y, start_x, "╭" + "─" * (modal_width - 2) + "╮",
                     curses.color_pair(COLOR_HEADER))
        stdscr.addstr(start_y + modal_height - 1, start_x, "╰" + "─" * (modal_width - 2) + "╯",
                     curses.color_pair(COLOR_HEADER))
    except curses.error:
        pass

    # Title
    title = " Mission Control Help "
    title_x = start_x + (modal_width - len(title)) // 2
    try:
        stdscr.addstr(start_y, title_x, title,
                     curses.color_pair(COLOR_HEADER) | curses.A_BOLD)
    except curses.error:
        pass

    # Content
    line_y = start_y + 2
    content_x = start_x + 3

    sections = [
        ("Navigation", [
            ("↑/↓ or k/j", "Navigate list or scroll summary"),
            ("Tab", "Switch between Projects and Tasks panes"),
            ("p", "Switch to Project Summary pane"),
            ("Home/End", "Jump to first/last item"),
        ]),
        ("Projects Pane", [
            ("s", "Cycle sort: priority → category → due → updated → name → risk"),
            ("f", "Cycle filter: all → active → blocked → work → personal → dev → family → high"),
            ("r", "Refresh all data from disk"),
        ]),
        ("Summary Pane", [
            ("↑/↓ or k/j", "Scroll summary content up/down"),
            ("Tab", "Return to Projects pane"),
        ]),
        ("Tasks Pane", [
            ("Space", "Toggle task completion ([ ] ↔ [✓])"),
            ("d", "Delete selected task"),
            ("m", "Move task to another project"),
            ("u", "Undo last task deletion (in tasks pane)"),
        ]),
        ("Import History", [
            ("u", "Undo recent imports (from projects/summary pane)"),
        ]),
        ("Project Management", [
            ("n", "Create new project"),
        ]),
        ("Other", [
            # ("i", "Import files / Review pending analyses"),  # PHASE 1: Disabled, will be inbox later
            ("?", "Show this help screen"),
            ("q", "Quit Mission Control"),
        ]),
    ]

    for section_name, keybindings in sections:
        if line_y >= start_y + modal_height - 3:
            break

        try:
            stdscr.addstr(line_y, content_x, section_name,
                         curses.color_pair(COLOR_ACTIVE) | curses.A_BOLD)
            line_y += 1

            for key, description in keybindings:
                if line_y >= start_y + modal_height - 3:
                    break
                key_display = f"  {key:<12}"
                desc_display = description[:modal_width - 20]
                stdscr.addstr(line_y, content_x, key_display,
                             curses.color_pair(COLOR_HEADER))
                stdscr.addstr(line_y, content_x + 14, desc_display)
                line_y += 1

            line_y += 1  # Space between sections

        except curses.error:
            pass

    # Footer
    footer = "Press any key to close"
    footer_x = start_x + (modal_width - len(footer)) // 2
    try:
        stdscr.addstr(start_y + modal_height - 2, footer_x, footer,
                     curses.color_pair(COLOR_STALE))
    except curses.error:
        pass

    stdscr.refresh()

    # Wait for any key
    stdscr.timeout(-1)  # Block until key pressed
    stdscr.getch()
    stdscr.timeout(100)  # Restore timeout
