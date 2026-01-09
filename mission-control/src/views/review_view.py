"""
Review view - interactive UI for approving staged AI analyses.

Displays pending analyses with checkboxes for selective approval.
"""
import curses
from pathlib import Path
from typing import List, Dict, Set
import json


def render_review_modal(stdscr, staging_manager, y_offset: int = 0):
    """
    Render review modal for pending staged analyses.

    Args:
        stdscr: Curses screen object
        staging_manager: StagingManager instance
        y_offset: Vertical offset for rendering

    Returns:
        Action to take: 'processed' if changes applied, 'quit' to exit
    """
    # Get pending analyses
    pending = staging_manager.get_pending_analyses()

    if not pending:
        # No pending items
        height, width = stdscr.getmaxyx()
        y = height // 2
        x = width // 2 - 20

        stdscr.addstr(y, x, "No pending analyses to review", curses.A_BOLD)
        stdscr.addstr(y + 2, x, "Press any key to continue...")
        stdscr.refresh()
        stdscr.getch()
        return 'quit'

    # Interactive review loop
    current_analysis_idx = 0

    while current_analysis_idx < len(pending):
        analysis = pending[current_analysis_idx]

        # Render the analysis review screen
        action = render_single_analysis_review(
            stdscr, staging_manager, analysis,
            current_analysis_idx + 1, len(pending)
        )

        if action == 'next':
            current_analysis_idx += 1
        elif action == 'prev':
            current_analysis_idx = max(0, current_analysis_idx - 1)
        elif action == 'quit':
            return 'quit'
        elif action == 'processed':
            # Reload pending list after processing
            pending = staging_manager.get_pending_analyses()
            if not pending:
                return 'processed'
            # Stay on same index (or adjust if out of bounds)
            current_analysis_idx = min(current_analysis_idx, len(pending) - 1)

    return 'processed'


def render_single_analysis_review(stdscr, staging_manager, analysis: Dict,
                                   num: int, total: int) -> str:
    """
    Render review screen for a single staged analysis.

    Args:
        stdscr: Curses screen object
        staging_manager: StagingManager instance
        analysis: Analysis data dict
        num: Current analysis number (1-indexed)
        total: Total number of pending analyses

    Returns:
        Action: 'next', 'prev', 'quit', or 'processed'
    """
    height, width = stdscr.getmaxyx()

    # Initialize selection state
    # Track which items are selected (True = approve, False = not selected)
    selected_items = {
        'tasks': set(range(len(analysis['analysis']['tasks']))),  # Default: all selected
        'decisions': set(range(len(analysis['analysis']['decisions']))),
        'updates': set(range(len(analysis['analysis']['updates'])))
    }

    # UI state
    current_section = 'tasks'  # tasks, decisions, updates
    current_item_idx = 0
    scroll_offset = 0

    while True:
        stdscr.clear()

        # Header
        header = f"Review Analysis ({num}/{total}) - {analysis['original_file']}"
        stdscr.addstr(0, 0, header[:width-1], curses.A_BOLD | curses.A_REVERSE)

        analyzed_at = analysis['analyzed_at'][:19].replace('T', ' ')
        stdscr.addstr(1, 0, f"Analyzed: {analyzed_at}")

        # Instructions
        y = 3
        stdscr.addstr(y, 0, "Instructions:", curses.A_BOLD)
        y += 1
        stdscr.addstr(y, 2, "↑/↓: Navigate items  | Space: Toggle selection  | Tab: Switch section")
        y += 1
        stdscr.addstr(y, 2, "[A]pprove Selected   | [R]eject All           | [N]ext / [P]rev      | [Q]uit")
        y += 2

        # Render sections
        y = render_section(stdscr, "Tasks", analysis['analysis']['tasks'],
                          selected_items['tasks'], y, width, height,
                          is_active=(current_section == 'tasks'),
                          current_idx=current_item_idx if current_section == 'tasks' else -1,
                          scroll_offset=scroll_offset if current_section == 'tasks' else 0)

        y += 1
        y = render_section(stdscr, "Decisions", analysis['analysis']['decisions'],
                          selected_items['decisions'], y, width, height,
                          is_active=(current_section == 'decisions'),
                          current_idx=current_item_idx if current_section == 'decisions' else -1,
                          scroll_offset=scroll_offset if current_section == 'decisions' else 0)

        y += 1
        y = render_section(stdscr, "Updates", analysis['analysis']['updates'],
                          selected_items['updates'], y, width, height,
                          is_active=(current_section == 'updates'),
                          current_idx=current_item_idx if current_section == 'updates' else -1,
                          scroll_offset=scroll_offset if current_section == 'updates' else 0)

        # Footer summary
        total_selected = sum(len(s) for s in selected_items.values())
        total_items = (len(analysis['analysis']['tasks']) +
                      len(analysis['analysis']['decisions']) +
                      len(analysis['analysis']['updates']))

        stdscr.addstr(height - 1, 0,
                     f"Selected: {total_selected}/{total_items} items",
                     curses.A_REVERSE)

        stdscr.refresh()

        # Handle input
        key = stdscr.getch()

        # Get current section items
        current_items = analysis['analysis'][current_section]
        max_idx = len(current_items) - 1

        if key == curses.KEY_UP:
            if current_item_idx > 0:
                current_item_idx -= 1
                # Adjust scroll if needed
                if current_item_idx < scroll_offset:
                    scroll_offset = current_item_idx

        elif key == curses.KEY_DOWN:
            if current_item_idx < max_idx:
                current_item_idx += 1
                # Adjust scroll if needed
                visible_lines = height - 15  # Approximate available space
                if current_item_idx >= scroll_offset + visible_lines:
                    scroll_offset = current_item_idx - visible_lines + 1

        elif key == ord(' '):  # Space - toggle selection
            if current_item_idx in selected_items[current_section]:
                selected_items[current_section].remove(current_item_idx)
            else:
                selected_items[current_section].add(current_item_idx)

        elif key == ord('\t'):  # Tab - switch section
            sections = ['tasks', 'decisions', 'updates']
            current_idx = sections.index(current_section)
            current_section = sections[(current_idx + 1) % 3]
            current_item_idx = 0
            scroll_offset = 0

        elif key == ord('a') or key == ord('A'):  # Approve selected
            # Apply selected items
            approved_indices = {
                'tasks': list(selected_items['tasks']),
                'decisions': list(selected_items['decisions']),
                'updates': list(selected_items['updates'])
            }

            # Mark as approved
            staging_file = Path(analysis['staging_file'])
            staging_manager.mark_approved(staging_file, approved_indices)

            # Apply changes (this will be done by import_processor)
            return 'processed'

        elif key == ord('r') or key == ord('R'):  # Reject all
            staging_file = Path(analysis['staging_file'])
            staging_manager.mark_rejected(staging_file)
            return 'processed'

        elif key == ord('n') or key == ord('N'):  # Next
            return 'next'

        elif key == ord('p') or key == ord('P'):  # Previous
            return 'prev'

        elif key == ord('q') or key == ord('Q'):  # Quit
            return 'quit'


def render_section(stdscr, title: str, items: List[Dict], selected: Set[int],
                   y: int, width: int, height: int, is_active: bool = False,
                   current_idx: int = -1, scroll_offset: int = 0) -> int:
    """
    Render a section (tasks, decisions, or updates) with items.

    Returns:
        New y position after rendering
    """
    if y >= height - 2:
        return y

    # Section header
    header_attr = curses.A_BOLD | curses.A_UNDERLINE if is_active else curses.A_BOLD
    stdscr.addstr(y, 0, f"{title} ({len(items)}):", header_attr)
    y += 1

    if not items:
        stdscr.addstr(y, 2, "(none)")
        return y + 1

    # Render items with scrolling
    visible_start = scroll_offset
    visible_end = min(len(items), scroll_offset + (height - y - 3))

    for i in range(visible_start, visible_end):
        if y >= height - 2:
            break

        item = items[i]
        is_selected = i in selected
        is_current = (i == current_idx and is_active)

        # Checkbox
        checkbox = "[✓]" if is_selected else "[ ]"

        # Format item text based on type
        if 'text' in item:  # Task or Decision
            item_text = item['text'][:width-10]
            project = item.get('project', '')
        elif 'summary' in item:  # Update
            item_text = item['summary'][:width-10]
            project = item.get('project', '')
        else:
            item_text = str(item)[:width-10]
            project = ''

        # Build display line
        line = f"  {checkbox} {item_text}"
        if project and project != "HOLDING":
            line += f" [{project}]"

        # Apply styling
        attr = curses.A_NORMAL
        if is_current:
            attr |= curses.A_REVERSE
        if is_selected:
            attr |= curses.A_BOLD

        try:
            stdscr.addstr(y, 0, line[:width-1], attr)
        except curses.error:
            pass

        y += 1

    # Show scroll indicator if needed
    if visible_end < len(items):
        try:
            stdscr.addstr(y, 2, f"... ({len(items) - visible_end} more)")
        except curses.error:
            pass
        y += 1

    return y
