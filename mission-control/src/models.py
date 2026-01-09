"""
Data models for Mission Control dashboard.
"""
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Optional
from functools import cached_property


@dataclass
class Project:
    """Represents a project with all its metadata from PROJECT.md"""

    # Core fields from YAML frontmatter
    title: str
    category: str  # personal, development, family, work
    container: str
    status: str    # active, on-hold, blocked, completed
    priority: str  # high, medium, low

    # Paths
    project_dir: Path
    project_md_path: Path

    # Dates
    created: date
    due: Optional[date]
    completed: Optional[date]
    last_updated: date

    # Metrics
    progress_percent: int
    tasks_total: int
    tasks_completed: int
    estimated_hours: int
    actual_hours: int

    # Flags
    blocked: bool
    needs_review: bool

    # HubSpot integration
    hubspot_company_id: Optional[str]
    hubspot_deal_id: Optional[str]
    hubspot_last_sync: Optional[date]

    # Additional fields
    tags: list[str]
    owner: Optional[str]
    description: Optional[str]  # Brief overview from PROJECT.md
    recent_decisions: list[str]  # Recent project decisions
    recent_updates: list[str]    # Recent project updates

    @cached_property
    def is_overdue(self) -> bool:
        """
        Returns True if project has a due date that has passed
        and the project is not completed.
        """
        if self.due is None or self.status == "completed":
            return False
        return date.today() > self.due

    @cached_property
    def is_stale(self) -> bool:
        """
        Returns True if project hasn't been updated in 7+ days.
        """
        days_since_update = (date.today() - self.last_updated).days
        return days_since_update >= 7

    @cached_property
    def days_until_due(self) -> Optional[int]:
        """
        Returns number of days until due date.
        Negative if overdue, None if no due date.
        """
        if self.due is None:
            return None
        delta = self.due - date.today()
        return delta.days

    @cached_property
    def days_since_update(self) -> int:
        """Returns number of days since last update"""
        return (date.today() - self.last_updated).days

    @cached_property
    def risk_score(self) -> int:
        """
        Calculates a composite risk score (0-100).

        Scoring:
        - Blocked: +50 points
        - Overdue: +30 points
        - Stale (7+ days): +10 points
        - Needs review: +10 points
        """
        score = 0

        if self.blocked:
            score += 50

        if self.is_overdue:
            score += 30

        if self.is_stale:
            score += 10

        if self.needs_review:
            score += 10

        return min(score, 100)  # Cap at 100

    @property
    def short_name(self) -> str:
        """Returns a shortened version of the title for display"""
        if len(self.title) <= 60:
            return self.title
        return self.title[:57] + "..."

    @property
    def status_display(self) -> str:
        """Returns formatted status for display"""
        status_map = {
            "active": "ACTV",
            "on-hold": "HOLD",
            "blocked": "BLCK",
            "completed": "DONE"
        }
        return status_map.get(self.status.lower(), self.status.upper()[:4])

    @property
    def priority_display(self) -> str:
        """Returns formatted priority for display"""
        priority_map = {
            "high": "HIGH",
            "medium": "MED",
            "low": "LOW"
        }
        return priority_map.get(self.priority.lower(), self.priority.upper()[:4])

    @property
    def category_display(self) -> str:
        """Returns formatted category for display"""
        category_map = {
            "work": "WORK",
            "personal": "PERS",
            "development": "DEV",
            "family": "FAM"
        }
        return category_map.get(self.category.lower(), self.category.upper()[:4])

    @property
    def has_hubspot(self) -> bool:
        """Returns True if project has HubSpot integration"""
        return self.hubspot_company_id is not None

    def __str__(self) -> str:
        """String representation for debugging"""
        return f"Project({self.title}, {self.status}, {self.priority})"

    def __repr__(self) -> str:
        return self.__str__()
