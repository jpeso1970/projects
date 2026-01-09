"""
Main dashboard view for Mission Control.
"""
import curses
from typing import List

from ..models import Project
from ..utils.date_utils import format_date, format_days_ago


# Color pair constants
COLOR_ACTIVE = 1    # Green
COLOR_HOLD = 2      # Yellow
COLOR_BLOCKED = 3   # Red
COLOR_COMPLETED = 4 # Blue
COLOR_STALE = 5     # Gray/White
COLOR_HEADER = 6    # Cyan


def init_colors():
    """Initialize curses color pairs"""
    curses.init_pair(COLOR_ACTIVE, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(COLOR_HOLD, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(COLOR_BLOCKED, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(COLOR_COMPLETED, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(COLOR_STALE, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(COLOR_HEADER, curses.COLOR_CYAN, curses.COLOR_BLACK)


def get_status_color(project: Project) -> int:
    """Get color pair for project based on status and flags"""
    if project.blocked:
        return COLOR_BLOCKED
    elif project.is_overdue:
        return COLOR_BLOCKED
    elif project.status.lower() == "active":
        return COLOR_ACTIVE if not project.is_stale else COLOR_STALE
    elif project.status.lower() == "on-hold":
        return COLOR_HOLD
    elif project.status.lower() == "completed":
        return COLOR_COMPLETED
    else:
        return COLOR_STALE


def get_status_emoji(project: Project) -> str:
    """Get emoji indicator for project status"""
    if project.blocked:
        return "🚫"
    elif project.is_overdue:
        return "⏰"
    elif project.needs_review:
        return "👀"
    elif project.priority.lower() == "high":
        return "📌"
    elif project.status.lower() == "completed":
        return "✅"
    else:
        return "  "


def get_risk_indicator(risk_score: int) -> str:
    """Get visual indicator for risk score (0-100)"""
    if risk_score >= 50:
        return "🔴"  # High risk
    elif risk_score >= 30:
        return "🟠"  # Medium-high risk
    elif risk_score >= 10:
        return "🟡"  # Low-medium risk
    else:
        return "🟢"  # Low risk


def draw_progress_bar(progress: int, width: int = 6) -> str:
    """
    Draw ASCII progress bar.

    Args:
        progress: Progress percentage (0-100)
        width: Width of progress bar in characters

    Returns:
        ASCII progress bar like "[███░░░]"
    """
    if progress < 0 or progress > 100:
        progress = 0

    filled = int((progress / 100) * width)
    empty = width - filled

    return f"[{'█' * filled}{'░' * empty}]"


def render_dashboard(stdscr, projects: List[Project], selected_idx: int, sort_by: str):
    """
    Render the main dashboard view.

    Args:
        stdscr: Curses window object
        projects: List of Project objects to display
        selected_idx: Index of currently selected project
        sort_by: Current sort criterion
    """
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    # Draw title
    title = "Mission Control"
    stdscr.addstr(0, (width - len(title)) // 2, title,
                  curses.color_pair(COLOR_HEADER) | curses.A_BOLD)

    # Draw project count and sort info
    info_line = f"Projects ({len(projects)})     Sort: [{sort_by.title()}]"
    stdscr.addstr(1, 2, info_line)

    # Draw header row
    header_y = 3
    header = f"{'Project':<62} {'Cat':<5} {'Status':<6} {'Pri':<4} {'Progress':<10} {'Due':<8} {'Updated':<8}"
    stdscr.addstr(header_y, 2, header, curses.color_pair(COLOR_HEADER) | curses.A_BOLD)

    # Draw separator
    stdscr.addstr(header_y + 1, 2, "─" * (width - 4))

    # Draw projects
    start_y = header_y + 2
    visible_height = height - start_y - 6  # Leave room for footer and attention panel

    # Calculate scroll offset
    scroll_offset = 0
    if selected_idx >= visible_height:
        scroll_offset = selected_idx - visible_height + 1

    for i, project in enumerate(projects[scroll_offset:scroll_offset + visible_height]):
        actual_idx = i + scroll_offset
        y = start_y + i

        if y >= height - 6:  # Stop before attention panel
            break

        # Determine if this row is selected
        is_selected = (actual_idx == selected_idx)

        # Get status color
        color = get_status_color(project)

        # Format project row
        emoji = get_status_emoji(project)
        name = project.short_name[:60]
        category = project.category_display
        status = project.status_display
        priority = project.priority_display
        progress_bar = draw_progress_bar(project.progress_percent)
        progress_pct = f"{project.progress_percent}%"
        due_date = format_date(project.due)
        updated = format_days_ago(project.last_updated)

        row = f"{emoji} {name:<60} {category:<5} {status:<6} {priority:<4} {progress_bar} {progress_pct:<3} {due_date:<8} {updated:<8}"

        # Draw the row
        attr = curses.color_pair(color)
        if is_selected:
            attr |= curses.A_REVERSE

        try:
            stdscr.addstr(y, 2, row[:width - 4], attr)
        except curses.error:
            pass  # Ignore errors if we're at the edge of the screen

    # Draw attention panel
    attention_y = height - 5
    stdscr.addstr(attention_y, 2, "⚠ Attention Needed",
                  curses.color_pair(COLOR_HEADER) | curses.A_BOLD)

    # Count attention items
    blocked_projects = [p for p in projects if p.blocked]
    stale_projects = [p for p in projects if p.is_stale and p.status.lower() == "active"]
    overdue_projects = [p for p in projects if p.is_overdue]

    attention_items = []
    if blocked_projects:
        names = ", ".join([p.short_name[:40] for p in blocked_projects[:2]])
        if len(blocked_projects) > 2:
            names += f", +{len(blocked_projects) - 2} more"
        attention_items.append(f"🚫 BLOCKED ({len(blocked_projects)}): {names}")

    if overdue_projects:
        names = ", ".join([p.short_name[:40] for p in overdue_projects[:2]])
        if len(overdue_projects) > 2:
            names += f", +{len(overdue_projects) - 2} more"
        attention_items.append(f"⏰ OVERDUE ({len(overdue_projects)}): {names}")

    if stale_projects:
        names = ", ".join([p.short_name[:40] for p in stale_projects[:2]])
        if len(stale_projects) > 2:
            names += f", +{len(stale_projects) - 2} more"
        attention_items.append(f"📅 STALE ({len(stale_projects)}): {names}")

    if not attention_items:
        stdscr.addstr(attention_y + 1, 2, "All projects on track! ✓", curses.color_pair(COLOR_ACTIVE))
    else:
        for i, item in enumerate(attention_items[:2]):  # Show max 2 items
            try:
                stdscr.addstr(attention_y + 1 + i, 2, item[:width - 4], curses.color_pair(COLOR_BLOCKED))
            except curses.error:
                pass

    # Draw footer with keybindings
    footer_y = height - 2
    footer = "[↑↓] Navigate  [s] Sort  [r] Refresh  [q] Quit"
    try:
        stdscr.addstr(footer_y, 2, footer, curses.color_pair(COLOR_HEADER))
    except curses.error:
        pass

    stdscr.refresh()
