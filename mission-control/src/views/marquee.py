"""
Scrolling marquee view for project updates ticker.
"""
import curses
import time
from typing import List, Tuple
from pathlib import Path

from .dashboard import COLOR_HEADER, COLOR_ACTIVE


class Marquee:
    """
    Manages a scrolling news ticker showing recent project updates.

    Displays updates from all projects in a continuous scrolling format:
    "Project Name: Update text • Project Name: Update text • ..."
    """

    def __init__(self, refresh_interval: int = 30):
        """
        Initialize marquee.

        Args:
            refresh_interval: Seconds between content refreshes (default: 30)
        """
        self.scroll_position = 0
        self.last_refresh = 0
        self.refresh_interval = refresh_interval
        self.content = ""
        self.last_update_time = 0

    def update_content(self, projects: List) -> None:
        """
        Refresh marquee content from project list.

        Args:
            projects: List of Project objects with recent_updates
        """
        updates = []

        for project in projects:
            if hasattr(project, 'recent_updates') and project.recent_updates:
                # Get up to 3 most recent updates per project
                project_updates = project.recent_updates[:3]

                for update in project_updates:
                    # Format: "Project Title: Update text"
                    updates.append(f"{project.title}: {update}")

        if updates:
            # Join with bullet separator
            self.content = "  •  ".join(updates) + "  •  "
        else:
            self.content = "No recent project updates  •  "

        self.last_refresh = time.time()

    def should_refresh(self) -> bool:
        """Check if content should be refreshed"""
        return time.time() - self.last_refresh > self.refresh_interval

    def render(self, stdscr, y: int, width: int, projects: List) -> None:
        """
        Render the scrolling marquee at specified line.

        Args:
            stdscr: Curses window object
            y: Y position (typically height - 1 for bottom line)
            width: Available width
            projects: List of projects (for content refresh)
        """
        # Refresh content if needed
        if self.should_refresh() or not self.content:
            self.update_content(projects)

        # Don't render if no content
        if not self.content:
            return

        # Auto-scroll: increment position every render
        # Speed controlled by main loop refresh rate
        current_time = time.time()
        if current_time - self.last_update_time > 0.1:  # Scroll every 100ms
            self.scroll_position += 1
            self.last_update_time = current_time

        # Loop the content seamlessly
        content_length = len(self.content)
        if content_length == 0:
            return

        # Reset position when we've scrolled past the entire content
        if self.scroll_position >= content_length:
            self.scroll_position = 0

        # Build the visible text
        # We need to show content from scroll_position, and loop back if needed
        visible_text = ""

        # Fill the width with looped content
        chars_needed = width - 2  # Leave space for border
        pos = self.scroll_position

        while len(visible_text) < chars_needed:
            visible_text += self.content[pos % content_length]
            pos += 1

        # Truncate to exact width
        visible_text = visible_text[:chars_needed]

        # Render the line
        try:
            # Draw left border
            stdscr.addstr(y, 0, "│", curses.color_pair(COLOR_HEADER))

            # Draw scrolling content with highlighting
            self._render_colored_text(stdscr, y, 1, visible_text, width - 2)

            # Draw right border
            stdscr.addstr(y, width - 1, "│", curses.color_pair(COLOR_HEADER))

        except curses.error:
            # Ignore rendering errors at screen edges
            pass

    def _render_colored_text(self, stdscr, y: int, x: int, text: str, max_width: int) -> None:
        """
        Render text with color highlighting for project names.

        Project names (before ':') are highlighted, content is normal.
        """
        current_x = x
        i = 0

        while i < len(text) and current_x < x + max_width:
            # Check if we're at a project name (text before ':')
            if ':' in text[i:]:
                colon_pos = text[i:].index(':')

                # Project name - render in active color
                project_name = text[i:i+colon_pos]
                if current_x + len(project_name) <= x + max_width:
                    try:
                        stdscr.addstr(y, current_x, project_name,
                                    curses.color_pair(COLOR_ACTIVE) | curses.A_BOLD)
                        current_x += len(project_name)
                    except curses.error:
                        break
                    i += colon_pos
                else:
                    # Not enough space, render what we can
                    remaining = x + max_width - current_x
                    try:
                        stdscr.addstr(y, current_x, project_name[:remaining],
                                    curses.color_pair(COLOR_ACTIVE) | curses.A_BOLD)
                    except curses.error:
                        pass
                    break

            # Find next project name or bullet
            next_delimiter = float('inf')
            for delimiter in [':', '•']:
                pos = text[i:].find(delimiter)
                if pos != -1 and pos < next_delimiter:
                    next_delimiter = pos

            if next_delimiter == float('inf'):
                # Rest of string - render normally
                remaining_text = text[i:]
                remaining_width = x + max_width - current_x
                try:
                    stdscr.addstr(y, current_x, remaining_text[:remaining_width])
                except curses.error:
                    pass
                break
            else:
                # Render up to next delimiter
                chunk = text[i:i+next_delimiter+1]
                remaining_width = x + max_width - current_x

                if len(chunk) <= remaining_width:
                    try:
                        stdscr.addstr(y, current_x, chunk)
                        current_x += len(chunk)
                    except curses.error:
                        break
                    i += next_delimiter + 1
                else:
                    # Not enough space
                    try:
                        stdscr.addstr(y, current_x, chunk[:remaining_width])
                    except curses.error:
                        pass
                    break


def render_marquee_border_top(stdscr, y: int, width: int) -> None:
    """
    Render the top border of the marquee section.

    Args:
        stdscr: Curses window object
        y: Y position for the border
        width: Screen width
    """
    try:
        # Draw horizontal line with corners
        stdscr.addstr(y, 0, "├" + "─" * (width - 2) + "┤",
                     curses.color_pair(COLOR_HEADER))
    except curses.error:
        pass


def render_marquee_border_bottom(stdscr, y: int, width: int) -> None:
    """
    Render the bottom border of the marquee section.

    Args:
        stdscr: Curses window object
        y: Y position for the border
        width: Screen width
    """
    try:
        # Draw horizontal line with corners
        stdscr.addstr(y, 0, "└" + "─" * (width - 2) + "┘",
                     curses.color_pair(COLOR_HEADER))
    except curses.error:
        pass
