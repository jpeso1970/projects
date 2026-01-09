"""
Split-pane view with Projects (top) and Tasks (bottom).
"""
import curses
from typing import List
from pathlib import Path

from ..models import Project
from ..task_parser import Task, parse_tasks_file, toggle_task_completion
from ..utils.date_utils import format_date, format_days_ago
from .dashboard import (
    COLOR_ACTIVE, COLOR_HOLD, COLOR_BLOCKED, COLOR_COMPLETED,
    COLOR_STALE, COLOR_HEADER, get_status_color, get_status_emoji,
    draw_progress_bar
)


def render_split_view(stdscr, projects: List[Project], tasks: List[Task],
                      selected_project_idx: int, selected_task_idx: int,
                      active_pane: str, sort_by: str):
    """
    Render split-pane view with projects (top) and tasks (bottom).

    Args:
        stdscr: Curses window object
        projects: List of Project objects
        tasks: List of Task objects for selected project
        selected_project_idx: Index of selected project
        selected_task_idx: Index of selected task
        active_pane: Either "projects" or "tasks"
        sort_by: Current sort criterion for projects
    """
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    # Calculate split point (60% projects, 40% tasks)
    split_y = int(height * 0.6)

    # === TOP PANE: PROJECTS ===
    draw_projects_pane(stdscr, projects, selected_project_idx, sort_by,
                       active_pane == "projects", split_y, width)

    # === SEPARATOR ===
    try:
        stdscr.addstr(split_y, 0, "═" * width, curses.color_pair(COLOR_HEADER))
    except curses.error:
        pass

    # === BOTTOM PANE: TASKS ===
    draw_tasks_pane(stdscr, tasks, selected_task_idx, active_pane == "tasks",
                    split_y + 1, height, width, projects, selected_project_idx)

    # === FOOTER ===
    draw_footer(stdscr, height, width, active_pane)

    stdscr.refresh()


def draw_projects_pane(stdscr, projects: List[Project], selected_idx: int,
                       sort_by: str, is_active: bool, max_y: int, width: int):
    """Draw the projects pane (top half)"""
    # Title
    title = "PROJECTS" if is_active else "Projects"
    title_attr = curses.color_pair(COLOR_HEADER) | curses.A_BOLD
    if is_active:
        title_attr |= curses.A_REVERSE

    try:
        stdscr.addstr(0, 2, f" {title} ", title_attr)
        info = f"  ({len(projects)} total)  Sort: [{sort_by.title()}]"
        stdscr.addstr(0, 2 + len(title) + 2, info, curses.color_pair(COLOR_HEADER))
    except curses.error:
        pass

    # Header row
    header_y = 2
    header = f"{'Project':<62} {'Cat':<5} {'Stat':<5} {'Pri':<4} {'Progress':<10} {'Due':<8} {'Upd':<6}"
    try:
        stdscr.addstr(header_y, 2, header, curses.color_pair(COLOR_HEADER) | curses.A_BOLD)
        stdscr.addstr(header_y + 1, 2, "─" * (width - 4))
    except curses.error:
        pass

    # Projects list
    start_y = header_y + 2
    visible_height = max_y - start_y - 1

    # Calculate scroll offset
    scroll_offset = 0
    if selected_idx >= visible_height:
        scroll_offset = selected_idx - visible_height + 1

    for i, project in enumerate(projects[scroll_offset:scroll_offset + visible_height]):
        actual_idx = i + scroll_offset
        y = start_y + i

        if y >= max_y - 1:
            break

        is_selected = (actual_idx == selected_idx)
        color = get_status_color(project)

        # Format row
        emoji = get_status_emoji(project)
        name = project.short_name[:60]
        category = project.category_display
        status = project.status_display
        priority = project.priority_display
        progress_bar = draw_progress_bar(project.progress_percent, width=4)
        progress_pct = f"{project.progress_percent}%"
        due_date = format_date(project.due)
        updated = format_days_ago(project.last_updated)

        row = f"{emoji} {name:<60} {category:<5} {status:<5} {priority:<4} {progress_bar} {progress_pct:<3} {due_date:<8} {updated:<6}"

        attr = curses.color_pair(color)
        if is_selected and is_active:
            attr |= curses.A_REVERSE

        try:
            stdscr.addstr(y, 2, row[:width - 4], attr)
        except curses.error:
            pass


def draw_tasks_pane(stdscr, tasks: List[Task], selected_idx: int, is_active: bool,
                    start_y: int, max_y: int, width: int, projects: List[Project],
                    selected_project_idx: int):
    """Draw the tasks pane (bottom half)"""
    # Title
    title = "TASKS" if is_active else "Tasks"
    title_attr = curses.color_pair(COLOR_HEADER) | curses.A_BOLD
    if is_active:
        title_attr |= curses.A_REVERSE

    # Show project name
    project_name = ""
    if projects and selected_project_idx < len(projects):
        project_name = f" - {projects[selected_project_idx].short_name[:40]}"

    try:
        stdscr.addstr(start_y, 2, f" {title} ", title_attr)
        stdscr.addstr(start_y, 2 + len(title) + 2,
                     f"  ({len(tasks)} total){project_name}",
                     curses.color_pair(COLOR_HEADER))
    except curses.error:
        pass

    # Header row
    header_y = start_y + 2
    header = f"{'Status':<6} {'Task':<80}"
    try:
        stdscr.addstr(header_y, 2, header, curses.color_pair(COLOR_HEADER) | curses.A_BOLD)
        stdscr.addstr(header_y + 1, 2, "─" * (width - 4))
    except curses.error:
        pass

    # Tasks list
    list_start_y = header_y + 2
    visible_height = max_y - list_start_y - 3  # Leave room for footer

    if not tasks:
        try:
            stdscr.addstr(list_start_y, 2, "No tasks found in tasks.md",
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
        y = list_start_y + i

        if y >= max_y - 3:
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

        # Format row
        status_display = task.status_display
        task_text = task.text[:75]

        row = f"{status_display:<6} {task_text}"

        attr = curses.color_pair(color)
        if is_selected and is_active:
            attr |= curses.A_REVERSE

        try:
            stdscr.addstr(y, 2, row[:width - 4], attr)
        except curses.error:
            pass


def draw_footer(stdscr, height: int, width: int, active_pane: str):
    """Draw footer with keybindings"""
    footer_y = height - 1

    if active_pane == "projects":
        footer = "[↑↓] Navigate  [Tab] Tasks  [s] Sort  [i] Imports  [r] Refresh  [q] Quit"
    else:
        footer = "[↑↓] Navigate  [Tab] Projects  [Space] Toggle  [i] Imports  [q] Quit"

    try:
        stdscr.addstr(footer_y, 2, footer, curses.color_pair(COLOR_HEADER))
    except curses.error:
        pass
