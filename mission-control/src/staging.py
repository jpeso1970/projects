"""
Staging system for AI-analyzed content.

Stores analyses before applying to project files.
"""
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from dataclasses import asdict

try:
    from .content_analyzer import ContentAnalysis
except ImportError:
    from content_analyzer import ContentAnalysis


class StagingManager:
    """
    Manages staged AI analyses waiting for review.
    """

    def __init__(self, staging_dir: Path):
        """
        Initialize staging manager.

        Args:
            staging_dir: Directory to store staged analyses
        """
        self.staging_dir = staging_dir
        self.staging_dir.mkdir(parents=True, exist_ok=True)

    def stage_analysis(self, filename: str, analysis: ContentAnalysis) -> Path:
        """
        Stage an AI analysis for review.

        Args:
            filename: Original filename that was analyzed
            analysis: ContentAnalysis object

        Returns:
            Path to staged analysis file
        """
        # Create staging filename
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        safe_filename = filename.replace('/', '-').replace('\\', '-')
        staging_filename = f"{timestamp}-{safe_filename}.json"
        staging_path = self.staging_dir / staging_filename

        # Convert analysis to JSON-serializable dict
        data = {
            "original_file": filename,
            "analyzed_at": datetime.now().isoformat(),
            "analysis": {
                "tasks": [asdict(t) for t in analysis.tasks],
                "decisions": [asdict(d) for d in analysis.decisions],
                "updates": [asdict(u) for u in analysis.updates],
                "unmatched_content": analysis.unmatched_content,
                "project_mentions": analysis.project_mentions
            },
            "status": "pending",  # pending, approved, rejected
            "approved_items": {
                "tasks": [],  # Indices of approved tasks
                "decisions": [],  # Indices of approved decisions
                "updates": []  # Indices of approved updates
            }
        }

        # Save to JSON
        staging_path.write_text(json.dumps(data, indent=2))

        return staging_path

    def get_pending_analyses(self) -> List[Dict]:
        """
        Get all pending analyses waiting for review.

        Returns:
            List of analysis metadata dicts
        """
        pending = []

        for staging_file in self.staging_dir.glob("*.json"):
            try:
                data = json.loads(staging_file.read_text())
                if data.get("status") == "pending":
                    # Add metadata
                    data["staging_file"] = str(staging_file)
                    data["staging_filename"] = staging_file.name
                    pending.append(data)
            except Exception as e:
                print(f"Error loading {staging_file}: {e}")

        # Sort by timestamp (newest first)
        pending.sort(key=lambda x: x.get("analyzed_at", ""), reverse=True)

        return pending

    def load_analysis(self, staging_file: Path) -> Dict:
        """
        Load a staged analysis.

        Args:
            staging_file: Path to staged analysis JSON

        Returns:
            Analysis data dict
        """
        return json.loads(staging_file.read_text())

    def mark_approved(self, staging_file: Path, approved_items: Dict[str, List[int]]):
        """
        Mark specific items as approved for a staged analysis.

        Args:
            staging_file: Path to staged analysis
            approved_items: Dict with keys 'tasks', 'decisions', 'updates'
                          and values as lists of indices to approve
        """
        data = json.loads(staging_file.read_text())
        data["approved_items"] = approved_items
        data["status"] = "approved"
        data["reviewed_at"] = datetime.now().isoformat()
        staging_file.write_text(json.dumps(data, indent=2))

    def mark_rejected(self, staging_file: Path):
        """
        Mark a staged analysis as rejected.

        Args:
            staging_file: Path to staged analysis
        """
        data = json.loads(staging_file.read_text())
        data["status"] = "rejected"
        data["reviewed_at"] = datetime.now().isoformat()
        staging_file.write_text(json.dumps(data, indent=2))

    def get_approved_items(self, staging_file: Path) -> Dict:
        """
        Get approved items from a staged analysis.

        Args:
            staging_file: Path to staged analysis

        Returns:
            Dict containing approved tasks, decisions, and updates
        """
        data = json.loads(staging_file.read_text())

        if data.get("status") != "approved":
            return {"tasks": [], "decisions": [], "updates": []}

        approved_indices = data.get("approved_items", {})
        analysis = data.get("analysis", {})

        # Extract approved items by index
        result = {
            "tasks": [analysis["tasks"][i] for i in approved_indices.get("tasks", [])
                     if i < len(analysis.get("tasks", []))],
            "decisions": [analysis["decisions"][i] for i in approved_indices.get("decisions", [])
                         if i < len(analysis.get("decisions", []))],
            "updates": [analysis["updates"][i] for i in approved_indices.get("updates", [])
                       if i < len(analysis.get("updates", []))]
        }

        return result

    def archive_processed(self, staging_file: Path):
        """
        Archive a processed staging file.

        Args:
            staging_file: Path to staging file to archive
        """
        archive_dir = self.staging_dir / "archive"
        archive_dir.mkdir(exist_ok=True)

        # Move to archive
        archive_path = archive_dir / staging_file.name
        staging_file.rename(archive_path)

    def get_summary(self) -> Dict:
        """
        Get summary of staging area.

        Returns:
            Dict with counts of pending, approved, rejected
        """
        pending = 0
        approved = 0
        rejected = 0

        for staging_file in self.staging_dir.glob("*.json"):
            try:
                data = json.loads(staging_file.read_text())
                status = data.get("status", "pending")
                if status == "pending":
                    pending += 1
                elif status == "approved":
                    approved += 1
                elif status == "rejected":
                    rejected += 1
            except Exception:
                pass

        return {
            "pending": pending,
            "approved": approved,
            "rejected": rejected
        }
