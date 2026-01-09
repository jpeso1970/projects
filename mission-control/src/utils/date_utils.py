"""
Date utility functions for Mission Control.
"""
from datetime import date, datetime
from typing import Optional


def parse_date(date_str: Optional[str]) -> Optional[date]:
    """
    Parse a date string in ISO 8601 format (YYYY-MM-DD) to a date object.

    Args:
        date_str: String in format YYYY-MM-DD, or None/null

    Returns:
        date object, or None if parsing fails or input is None/null
    """
    if not date_str or date_str == "null" or date_str == "None":
        return None

    try:
        # Handle YYYY-MM-DD format
        return datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
    except (ValueError, AttributeError):
        return None


def format_date(d: Optional[date]) -> str:
    """
    Format a date object for display.

    Args:
        d: date object or None

    Returns:
        Formatted string like "Jan 15" or "--" if None
    """
    if d is None:
        return "--"

    return d.strftime("%b %d")


def format_date_full(d: Optional[date]) -> str:
    """
    Format a date object for full display with year.

    Args:
        d: date object or None

    Returns:
        Formatted string like "2026-01-15" or "--" if None
    """
    if d is None:
        return "--"

    return d.strftime("%Y-%m-%d")


def format_relative_date(d: Optional[date]) -> str:
    """
    Format a date relative to today.

    Args:
        d: date object or None

    Returns:
        Formatted string like "3d" (3 days ago), "today", "1d" (1 day from now), or "--" if None
    """
    if d is None:
        return "--"

    today = date.today()
    delta = (d - today).days

    if delta == 0:
        return "today"
    elif delta == 1:
        return "tmrw"
    elif delta == -1:
        return "yest"
    elif delta > 0:
        return f"{delta}d"
    else:
        return f"{abs(delta)}d ago"


def format_days_ago(d: date) -> str:
    """
    Format how many days ago a date was.

    Args:
        d: date object

    Returns:
        Formatted string like "3d" (3 days ago), "today", etc.
    """
    delta = (date.today() - d).days

    if delta == 0:
        return "today"
    elif delta == 1:
        return "yest"
    else:
        return f"{delta}d"
