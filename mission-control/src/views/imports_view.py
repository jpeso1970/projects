"""
Imports view - shows pending files in import directory.
"""
import curses
from typing import List
from pathlib import Path

from ..import_processor import ImportFile, ImportProcessor
from .dashboard import COLOR_HEADER, COLOR_ACTIVE, COLOR_BLOCKED, COLOR_STALE


def render_imports_modal(stdscr, import_dir: Path, projects_dir: Path):
    """
    Render a modal showing pending imports.

    Args:
        stdscr: Curses window object
        import_dir: Path to import directory
        projects_dir: Path to projects directory

    Returns:
        True if user wants to process imports, False to cancel
    """
    height, width = stdscr.getmaxyx()

    # Create processor
    processor = ImportProcessor(import_dir, projects_dir)
    import_files = processor.scan_import_directory()

    # Calculate modal size (80% of screen)
    modal_height = int(height * 0.8)
    modal_width = int(width * 0.8)
    modal_y = (height - modal_height) // 2
    modal_x = (width - modal_width) // 2

    # Create modal window
    modal = curses.newwin(modal_height, modal_width, modal_y, modal_x)
    modal.box()

    while True:
        modal.clear()
        modal.box()

        # Title
        title = " 📥 IMPORT DIRECTORY "
        modal.addstr(0, (modal_width - len(title)) // 2, title,
                    curses.color_pair(COLOR_HEADER) | curses.A_BOLD)

        # Info line
        info = f"Location: {import_dir}"
        try:
            modal.addstr(2, 2, info[:modal_width - 4], curses.color_pair(COLOR_HEADER))
        except curses.error:
            pass

        if not import_files:
            # Empty state
            modal.addstr(4, 2, "No files in import directory", curses.color_pair(COLOR_STALE))
            modal.addstr(6, 2, "Drop meeting summaries, transcripts, or notes here:")
            modal.addstr(7, 4, str(import_dir), curses.color_pair(COLOR_ACTIVE))
            modal.addstr(9, 2, "Press any key to close...")
            modal.refresh()
            modal.getch()
            return False

        # File list
        y = 4
        modal.addstr(y, 2, f"Found {len(import_files)} file(s):",
                    curses.color_pair(COLOR_HEADER) | curses.A_BOLD)
        y += 2

        for i, import_file in enumerate(import_files[:modal_height - 12]):
            if y >= modal_height - 4:
                break

            # Filename
            filename_display = import_file.filename[:modal_width - 6]
            modal.addstr(y, 2, f"📄 {filename_display}")
            y += 1

            # Project mentions
            if import_file.mentions:
                modal.addstr(y, 4, f"{len(import_file.mentions)} project(s) detected:",
                           curses.color_pair(COLOR_ACTIVE))
                y += 1
                for mention in import_file.mentions[:3]:  # Show max 3
                    conf_pct = int(mention.confidence * 100)
                    color = COLOR_ACTIVE if mention.confidence >= 0.9 else COLOR_STALE
                    mention_text = f"  • {mention.project_name} ({conf_pct}%, {mention.source})"
                    try:
                        modal.addstr(y, 4, mention_text[:modal_width - 8],
                                   curses.color_pair(color))
                    except curses.error:
                        pass
                    y += 1
            else:
                modal.addstr(y, 4, "⚠️  No projects detected - needs manual review",
                           curses.color_pair(COLOR_BLOCKED))
                y += 1

            y += 1  # Blank line between files

        # Footer with actions
        footer_y = modal_height - 3
        try:
            modal.addstr(footer_y, 2, "─" * (modal_width - 4))
            modal.addstr(footer_y + 1, 2,
                        "[p] Process with auto-routing  [ESC] Cancel",
                        curses.color_pair(COLOR_HEADER))
        except curses.error:
            pass

        modal.refresh()

        # Get input
        key = modal.getch()

        if key == ord('p') or key == ord('P'):
            # Process imports
            return True
        elif key == 27:  # ESC
            return False
        elif key == ord('q') or key == ord('Q'):
            return False


def process_imports_with_feedback(stdscr, import_dir: Path, projects_dir: Path):
    """
    Process imports and show feedback.

    Args:
        stdscr: Curses window object
        import_dir: Path to import directory
        projects_dir: Path to projects directory
    """
    height, width = stdscr.getmaxyx()

    # Create processor
    processor = ImportProcessor(import_dir, projects_dir)

    # Process
    stdscr.addstr(height // 2, (width - 20) // 2,
                 "Processing imports...",
                 curses.color_pair(COLOR_HEADER) | curses.A_BOLD)
    stdscr.refresh()

    summary = processor.process_all(auto_route=True)

    # Show results
    stdscr.clear()

    y = height // 2 - 5
    x_center = width // 2

    title = "✓ Import Processing Complete"
    stdscr.addstr(y, x_center - len(title) // 2, title,
                 curses.color_pair(COLOR_ACTIVE) | curses.A_BOLD)
    y += 2

    results = [
        f"Total files: {summary['total_files']}",
        f"Auto-routed: {summary['auto_routed']}",
        f"Manual review: {summary['manual_review']}",
        f"No mentions: {summary['no_mentions']}"
    ]

    for result in results:
        stdscr.addstr(y, x_center - len(result) // 2, result)
        y += 1

    y += 2
    prompt = "Press any key to continue..."
    stdscr.addstr(y, x_center - len(prompt) // 2, prompt,
                 curses.color_pair(COLOR_HEADER))

    stdscr.refresh()
    stdscr.getch()
