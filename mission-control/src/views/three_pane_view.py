"""
Three-pane view: [Projects | Summary] (top), Tasks (bottom)
"""
import curses
from typing import List
from pathlib import Path

from ..models import Project
from ..task_parser import Task
from ..utils.date_utils import format_date, format_days_ago, format_relative_date
from .dashboard import (
    COLOR_ACTIVE, COLOR_HOLD, COLOR_BLOCKED, COLOR_COMPLETED,
    COLOR_STALE, COLOR_HEADER, get_status_color, get_status_emoji,
    draw_progress_bar, get_risk_indicator
)


def render_three_pane_view(stdscr, projects: List[Project], tasks: List[Task],
                           selected_project_idx: int, selected_task_idx: int,
                           active_pane: str, sort_by: str, summary_scroll_offset: int = 0,
                           filter_by: str = "all", total_projects: int = 0):
    """
    Render three-pane view: Top split into Projects (left) | Summary (right), Tasks (bottom)

    Args:
        stdscr: Curses window object
        projects: List of Project objects
        tasks: List of Task objects for selected project
        selected_project_idx: Index of selected project
        selected_task_idx: Index of selected task
        active_pane: "projects", "summary", or "tasks"
        sort_by: Current sort criterion for projects
        summary_scroll_offset: Scroll offset for summary pane
        filter_by: Current filter criterion
        total_projects: Total number of projects before filtering
    """
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    # Calculate splits
    top_height = int(height * 0.5)  # Top half for projects + summary
    top_split_x = int(width * 0.5)  # Split top half 50/50

    # === TOP-LEFT: PROJECTS ===
    draw_projects_pane(stdscr, projects, selected_project_idx, sort_by,
                       active_pane == "projects", 0, 0, top_split_x, top_height,
                       filter_by, total_projects)

    # === TOP-RIGHT: PROJECT SUMMARY ===
    selected_project = projects[selected_project_idx] if projects and selected_project_idx < len(projects) else None
    draw_summary_pane(stdscr, selected_project, active_pane == "summary",
                     top_split_x, 0, width - top_split_x, top_height, summary_scroll_offset)

    # === SEPARATOR LINE (horizontal) ===
    try:
        stdscr.addstr(top_height, 0, "═" * width, curses.color_pair(COLOR_HEADER))
    except curses.error:
        pass

    # === BOTTOM: TASKS (full width) ===
    draw_tasks_pane(stdscr, tasks, selected_task_idx, active_pane == "tasks",
                   0, top_height + 1, width, height, selected_project)

    # === FOOTER ===
    draw_footer(stdscr, height, width, active_pane)

    stdscr.refresh()


def draw_projects_pane(stdscr, projects: List[Project], selected_idx: int,
                      sort_by: str, is_active: bool, x: int, y: int, width: int, height: int,
                      filter_by: str = "all", total_projects: int = 0):
    """Draw the projects pane (top-left)"""
    # Title bar
    title = "PROJECTS" if is_active else "Projects"
    title_attr = curses.color_pair(COLOR_HEADER) | curses.A_BOLD
    if is_active:
        title_attr |= curses.A_REVERSE

    try:
        stdscr.addstr(y, x, f" {title} ", title_attr)
        # Show count, filter, and sort info
        count_str = f"({len(projects)}/{total_projects})" if total_projects > 0 else f"({len(projects)})"
        filter_str = f"[{filter_by}]" if filter_by != "all" else ""
        sort_str = f"[{sort_by[:8]}]"
        info = f"  {count_str}  Filter: {filter_str}  Sort: {sort_str}" if filter_str else f"  {count_str}  Sort: {sort_str}"
        stdscr.addstr(y, x + len(title) + 2, info[:width - len(title) - 4],
                     curses.color_pair(COLOR_HEADER))
    except curses.error:
        pass

    # Header row
    header_y = y + 2
    # Calculate dynamic column widths
    # Fixed columns: emoji(2) + status(3) + priority(3) + progress(4) + owner(10) + spacing(5) = 27
    fixed_width = 27
    owner_width = 10
    name_width = max(20, width - fixed_width - 4)  # At least 20 chars for name

    header = f"{'Project':<{name_width}} {'Owner':<{owner_width}} {'St':<3} {'Pri':<3} {'Prg':<4}"
    try:
        stdscr.addstr(header_y, x + 1, header[:width - 3], curses.color_pair(COLOR_HEADER) | curses.A_BOLD)
        stdscr.addstr(header_y + 1, x + 1, "─" * (width - 3))
    except curses.error:
        pass

    # Vertical separator (right edge)
    for line_y in range(y, y + height):
        try:
            stdscr.addstr(line_y, x + width - 1, "│", curses.color_pair(COLOR_HEADER))
        except curses.error:
            pass

    # Projects list
    start_y = header_y + 2
    visible_height = height - (start_y - y) - 1

    # Calculate scroll offset
    scroll_offset = 0
    if selected_idx >= visible_height:
        scroll_offset = selected_idx - visible_height + 1

    for i, project in enumerate(projects[scroll_offset:scroll_offset + visible_height]):
        actual_idx = i + scroll_offset
        line_y = start_y + i

        if line_y >= y + height - 1:
            break

        is_selected = (actual_idx == selected_idx)
        color = get_status_color(project)

        # Format row with dynamic width
        emoji = get_status_emoji(project)
        name = project.short_name[:name_width]  # Use dynamic width
        owner = (project.owner or "")[:owner_width]  # Truncate owner to fit
        status = project.status_display[:3]
        priority = project.priority_display[:3]
        progress_pct = f"{project.progress_percent}%"

        row = f"{emoji} {name:<{name_width}} {owner:<{owner_width}} {status:<3} {priority:<3} {progress_pct:>3}"

        attr = curses.color_pair(color)
        if is_selected:
            attr |= curses.A_REVERSE if is_active else curses.A_BOLD

        try:
            stdscr.addstr(line_y, x + 1, row[:width - 3], attr)
        except curses.error:
            pass


def draw_summary_pane(stdscr, project: Project, is_active: bool,
                     x: int, y: int, width: int, height: int, scroll_offset: int = 0):
    """Draw the project summary pane (top-right)"""
    # Title bar
    title = "PROJECT SUMMARY" if is_active else "Project Summary"
    title_attr = curses.color_pair(COLOR_HEADER) | curses.A_BOLD
    if is_active:
        title_attr |= curses.A_REVERSE

    try:
        stdscr.addstr(y, x, f" {title} ".ljust(width), title_attr)
    except curses.error:
        pass

    if not project:
        try:
            stdscr.addstr(y + 3, x + 2, "No project selected", curses.color_pair(COLOR_STALE))
        except curses.error:
            pass
        return

    # Project details - COMPACT to leave room for decisions/updates
    line_y = y + 2
    try:
        # Project name (bold)
        stdscr.addstr(line_y, x + 1, project.title[:width - 3],
                     curses.color_pair(COLOR_HEADER) | curses.A_BOLD)
        line_y += 2

        # Status, Priority, and Risk on same line
        status_color = get_status_color(project)
        emoji = get_status_emoji(project)
        risk_indicator = get_risk_indicator(project.risk_score)
        status_line = f"{emoji} {project.status_display}  {project.priority_display}  {risk_indicator} Risk:{project.risk_score}"
        stdscr.addstr(line_y, x + 1, status_line[:width - 3], curses.color_pair(status_color))
        line_y += 2

        # Progress and Tasks on same line
        progress_bar = draw_progress_bar(project.progress_percent, width=8)
        progress_line = f"{progress_bar} {project.progress_percent}%  Tasks: {project.tasks_completed}/{project.tasks_total}"
        stdscr.addstr(line_y, x + 1, progress_line[:width - 3])
        line_y += 2

        # Due date with days until due (prominent if exists)
        if project.due:
            due_str = format_date(project.due)
            days_until = project.days_until_due
            if days_until is not None:
                if days_until < 0:
                    days_text = f"OVERDUE by {abs(days_until)} days!"
                    due_color = COLOR_BLOCKED
                elif days_until == 0:
                    days_text = "DUE TODAY!"
                    due_color = COLOR_BLOCKED
                elif days_until <= 7:
                    days_text = f"{days_until} days left"
                    due_color = COLOR_HOLD
                else:
                    days_text = f"{days_until} days left"
                    due_color = COLOR_ACTIVE
                stdscr.addstr(line_y, x + 1, f"Due: {due_str} ({days_text})"[:width - 3],
                             curses.color_pair(due_color))
            else:
                stdscr.addstr(line_y, x + 1, f"Due: {due_str}"[:width - 3])
            line_y += 1

        # Last updated (always show)
        if project.last_updated:
            updated_str = format_date(project.last_updated)
            days_ago = format_days_ago(project.last_updated)
            stdscr.addstr(line_y, x + 1, f"Updated: {updated_str} ({days_ago})"[:width - 3])
            line_y += 1

        # Description (purpose/context) if available
        if project.description:
            line_y += 1
            # Word wrap the description
            desc = project.description[:width * 2 - 6]  # Limit total length
            if len(desc) > width - 4:
                # Split into two lines
                split_point = desc[:width - 4].rfind(' ')
                if split_point > 0:
                    stdscr.addstr(line_y, x + 1, desc[:split_point][:width - 3],
                                 curses.color_pair(COLOR_STALE))
                    line_y += 1
                    stdscr.addstr(line_y, x + 1, desc[split_point + 1:][:width - 3],
                                 curses.color_pair(COLOR_STALE))
                else:
                    stdscr.addstr(line_y, x + 1, desc[:width - 3],
                                 curses.color_pair(COLOR_STALE))
            else:
                stdscr.addstr(line_y, x + 1, desc[:width - 3],
                             curses.color_pair(COLOR_STALE))
            line_y += 1

        # Recent Decisions and Updates (scrollable)
        has_decisions = hasattr(project, 'recent_decisions') and project.recent_decisions
        has_updates = hasattr(project, 'recent_updates') and project.recent_updates

        if has_decisions or has_updates:
            line_y += 2

            # Build combined list with section headers
            scrollable_items = []
            if has_decisions:
                scrollable_items.append(("header", "Recent Decisions:"))
                for decision in project.recent_decisions:
                    scrollable_items.append(("decision", f"  • {decision}"))

            if has_updates:
                if has_decisions:
                    scrollable_items.append(("space", ""))
                scrollable_items.append(("header", "Recent Updates:"))
                for update in project.recent_updates:
                    scrollable_items.append(("update", f"  • {update}"))

            # Calculate visible area
            available_lines = height - (line_y - y) - 2  # Leave room for scroll indicator
            total_items = len(scrollable_items)

            # Apply scroll offset (clamp to valid range)
            max_scroll = max(0, total_items - available_lines)
            actual_scroll = min(scroll_offset, max_scroll)

            # Show scroll up indicator
            if actual_scroll > 0:
                stdscr.addstr(line_y, x + width - 4, "↑↑", curses.color_pair(COLOR_HEADER) | curses.A_BOLD)

            # Display visible items
            visible_items = scrollable_items[actual_scroll:actual_scroll + available_lines]
            for item_type, text in visible_items:
                if line_y >= y + height - 2:
                    break

                if item_type == "header":
                    stdscr.addstr(line_y, x + 1, text[:width - 3], curses.color_pair(COLOR_HEADER) | curses.A_BOLD)
                elif item_type == "space":
                    pass  # Empty line
                else:
                    stdscr.addstr(line_y, x + 1, text[:width - 3])
                line_y += 1

            # Show scroll down indicator
            if actual_scroll < max_scroll:
                stdscr.addstr(y + height - 2, x + width - 4, "↓↓", curses.color_pair(COLOR_HEADER) | curses.A_BOLD)

    except curses.error:
        pass


def draw_tasks_pane(stdscr, tasks: List[Task], selected_idx: int, is_active: bool,
                   x: int, y: int, width: int, height: int, project: Project):
    """Draw the tasks pane (bottom, full width)"""
    # Title bar
    title = "TASKS" if is_active else "Tasks"
    title_attr = curses.color_pair(COLOR_HEADER) | curses.A_BOLD
    if is_active:
        title_attr |= curses.A_REVERSE

    # Show project name
    project_name = ""
    if project:
        project_name = f" - {project.short_name[:40]}"

    try:
        stdscr.addstr(y, x, f" {title} ", title_attr)
        stdscr.addstr(y, x + len(title) + 2,
                     f"  ({len(tasks)} total){project_name}",
                     curses.color_pair(COLOR_HEADER))
    except curses.error:
        pass

    # Header row
    header_y = y + 2
    assignee_width = 12
    task_width = width - 6 - assignee_width - 6  # status(6) + assignee + padding
    header = f"{'Status':<6} {'Task':<{task_width}} {'Assignee':<{assignee_width}}"
    try:
        stdscr.addstr(header_y, x + 2, header[:width - 4], curses.color_pair(COLOR_HEADER) | curses.A_BOLD)
        stdscr.addstr(header_y + 1, x + 2, "─" * (width - 4))
    except curses.error:
        pass

    # Tasks list
    list_start_y = header_y + 2
    visible_height = height - list_start_y - 2  # Leave room for footer

    if not tasks:
        try:
            stdscr.addstr(list_start_y, x + 2, "No tasks found in tasks.md",
                         curses.color_pair(COLOR_STALE))
        except curses.error:
            pass
        return

    # Calculate scroll offset
    scroll_offset = 0
    if selected_idx >= visible_height:
        scroll_offset = selected_idx - visible_height + 1

    for i, task in enumerate(tasks[scroll_offset:scroll_offset + visible_height]):
        actual_idx = i + scroll_offset
        line_y = list_start_y + i

        if line_y >= y + height - 2:
            break

        is_selected = (actual_idx == selected_idx)

        # Choose color based on task status
        if task.is_completed:
            color = COLOR_COMPLETED
        elif task.status == '[!]':
            color = COLOR_BLOCKED
        elif task.status == '[~]':
            color = COLOR_HOLD
        elif task.status == '[→]':
            color = COLOR_ACTIVE
        else:
            color = COLOR_STALE

        # Format row with assignee
        status_display = task.status_display
        assignee = (task.assignee or "")[:assignee_width]
        task_text = task.text[:task_width]

        row = f"{status_display:<6} {task_text:<{task_width}} {assignee:<{assignee_width}}"

        attr = curses.color_pair(color)
        if is_selected:
            attr |= curses.A_REVERSE if is_active else curses.A_BOLD

        try:
            stdscr.addstr(line_y, x + 2, row[:width - 4], attr)
        except curses.error:
            pass


def draw_footer(stdscr, height: int, width: int, active_pane: str):
    """Draw footer with keybindings"""
    footer_y = height - 1

    if active_pane == "projects":
        footer = "[↑↓] Navigate  [Tab] Tasks  [p] Summary  [s] Sort  [f] Filter  [?] Help  [q] Quit"
    elif active_pane == "summary":
        footer = "[↑↓] Scroll  [Tab] Projects  [p] Stay  [?] Help  [q] Quit"
    else:  # tasks
        footer = "[↑↓] Navigate  [Tab] Projects  [p] Summary  [Space] Toggle  [d] Delete  [u] Undo  [?] Help  [q] Quit"

    try:
        stdscr.addstr(footer_y, 0, footer[:width], curses.color_pair(COLOR_HEADER))
    except curses.error:
        pass
