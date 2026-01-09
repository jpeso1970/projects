"""
AI-powered content analyzer for meeting notes, transcripts, and emails.

Dissects unstructured content into structured project updates:
- Tasks to add to tasks.md
- Decisions/anecdotes for PROJECT.md
- Project narrative updates
"""
import os
import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime

try:
    from .file_reader import read_file_content
except ImportError:
    from file_reader import read_file_content


@dataclass
class ExtractedTask:
    """A task extracted from content"""
    text: str
    project: str
    priority: str  # high, medium, low
    assignee: Optional[str] = None  # Who owns this task
    due_date: Optional[str] = None
    context: str = ""  # Where this came from


@dataclass
class ExtractedDecision:
    """A decision or anecdote extracted from content"""
    text: str
    project: str
    date: str
    importance: str  # critical, important, notable
    context: str = ""


@dataclass
class ExtractedUpdate:
    """A narrative update for a project"""
    project: str
    summary: str
    details: str
    sentiment: str  # positive, neutral, negative, mixed


@dataclass
class ContentAnalysis:
    """Complete analysis of imported content"""
    tasks: List[ExtractedTask]
    decisions: List[ExtractedDecision]
    updates: List[ExtractedUpdate]
    unmatched_content: List[str]  # Content with no clear project home
    project_mentions: Dict[str, int]  # project_name -> mention_count


class ContentAnalyzer:
    """
    Analyzes unstructured content using Claude API.

    Extracts structured data: tasks, decisions, updates.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the content analyzer.

        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        """
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError(
                "No API key provided. Set ANTHROPIC_API_KEY environment variable "
                "or pass api_key parameter."
            )

    def analyze_content(self, content: str, known_projects: List[str],
                       filename: str = "") -> ContentAnalysis:
        """
        Analyze content and extract structured information.

        Args:
            content: Raw text content to analyze
            known_projects: List of known project names
            filename: Original filename (provides context)

        Returns:
            ContentAnalysis object with extracted data
        """
        # Build the analysis prompt
        prompt = self._build_analysis_prompt(content, known_projects, filename)

        # Call Claude API
        response = self._call_claude_api(prompt)

        # Parse response into structured data
        analysis = self._parse_analysis_response(response)

        return analysis

    def _build_analysis_prompt(self, content: str, known_projects: List[str],
                               filename: str) -> str:
        """Build the analysis prompt for Claude"""
        projects_list = "\n".join([f"- {p}" for p in known_projects])

        prompt = f"""You are analyzing meeting notes, transcripts, or email content to extract structured information for project management.

KNOWN PROJECTS:
{projects_list}

CONTENT TO ANALYZE:
Filename: {filename}

{content}

---

Please analyze this content and extract:

1. **TASKS**: Action items that need to be done. For each task provide:
   - text: Clear description
   - project: Which project it belongs to (from known projects list, or "HOLDING" if unclear)
   - priority: high, medium, or low
   - assignee: Person responsible (name if mentioned, null otherwise)
   - due_date: YYYY-MM-DD if mentioned, null otherwise
   - context: Brief context of where this came from

2. **DECISIONS**: Important decisions or anecdotes worth documenting. For each provide:
   - text: What was decided or what happened
   - project: Which project this relates to
   - date: Today's date in YYYY-MM-DD format
   - importance: critical, important, or notable
   - context: Brief context

3. **UPDATES**: Narrative updates about project status. For each provide:
   - project: Which project
   - summary: One-line summary
   - details: More detail about the update
   - sentiment: positive, neutral, negative, or mixed

4. **UNMATCHED**: Any content that doesn't clearly relate to known projects

Respond ONLY with valid JSON in this exact format:
{{
  "tasks": [
    {{
      "text": "Complete Q4 financial review",
      "project": "quatrro-transcendant-brands-remediation",
      "priority": "high",
      "due_date": "2026-01-15",
      "context": "Discussed in weekly meeting"
    }}
  ],
  "decisions": [
    {{
      "text": "Agreed to extend contract through Q2 2026",
      "project": "quatrro-the-one-group-remediation",
      "date": "{datetime.now().strftime('%Y-%m-%d')}",
      "importance": "important",
      "context": "Client meeting decision"
    }}
  ],
  "updates": [
    {{
      "project": "quatrro-poke-house-management-reports",
      "summary": "Project ahead of schedule",
      "details": "Completed initial setup phase 2 weeks early. Client very satisfied.",
      "sentiment": "positive"
    }}
  ],
  "unmatched": [
    "General discussion about industry trends..."
  ]
}}

Be thorough but precise. Extract all actionable tasks, important decisions, and status updates. If content doesn't match any known project, mark it as "HOLDING".
"""
        return prompt

    def _call_claude_api(self, prompt: str) -> str:
        """
        Call Claude API to analyze content.

        Args:
            prompt: Analysis prompt

        Returns:
            Claude's response text
        """
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=self.api_key)

            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return message.content[0].text

        except ImportError:
            raise ImportError(
                "anthropic package not installed. "
                "Install with: pip install anthropic"
            )
        except Exception as e:
            raise RuntimeError(f"Error calling Claude API: {e}")

    def _parse_analysis_response(self, response: str) -> ContentAnalysis:
        """
        Parse Claude's JSON response into ContentAnalysis object.

        Args:
            response: JSON response from Claude

        Returns:
            ContentAnalysis object
        """
        try:
            # Extract JSON from response (handles markdown code blocks)
            json_str = response
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()

            data = json.loads(json_str)

            # Parse tasks
            tasks = []
            for task_data in data.get("tasks", []):
                tasks.append(ExtractedTask(**task_data))

            # Parse decisions
            decisions = []
            for decision_data in data.get("decisions", []):
                decisions.append(ExtractedDecision(**decision_data))

            # Parse updates
            updates = []
            for update_data in data.get("updates", []):
                updates.append(ExtractedUpdate(**update_data))

            # Get unmatched content
            unmatched = data.get("unmatched", [])

            # Calculate project mentions
            project_mentions = {}
            for task in tasks:
                project_mentions[task.project] = project_mentions.get(task.project, 0) + 1
            for decision in decisions:
                project_mentions[decision.project] = project_mentions.get(decision.project, 0) + 1
            for update in updates:
                project_mentions[update.project] = project_mentions.get(update.project, 0) + 1

            return ContentAnalysis(
                tasks=tasks,
                decisions=decisions,
                updates=updates,
                unmatched_content=unmatched,
                project_mentions=project_mentions
            )

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response from Claude: {e}\n\nResponse:\n{response}")
        except Exception as e:
            raise RuntimeError(f"Error parsing analysis response: {e}")

    def analyze_file(self, file_path: Path, known_projects: List[str]) -> ContentAnalysis:
        """
        Analyze a file from the import directory.

        Args:
            file_path: Path to file to analyze
            known_projects: List of known project names

        Returns:
            ContentAnalysis object
        """
        try:
            content = read_file_content(file_path)
            if content is None:
                raise ValueError(f"Unable to read file or unsupported format: {file_path.name}")
            return self.analyze_content(content, known_projects, file_path.name)
        except Exception as e:
            raise RuntimeError(f"Error analyzing file {file_path}: {e}")


def save_analysis_to_json(analysis: ContentAnalysis, output_path: Path):
    """
    Save analysis results to JSON file for review.

    Args:
        analysis: ContentAnalysis object
        output_path: Where to save JSON
    """
    data = {
        "tasks": [asdict(t) for t in analysis.tasks],
        "decisions": [asdict(d) for d in analysis.decisions],
        "updates": [asdict(u) for u in analysis.updates],
        "unmatched_content": analysis.unmatched_content,
        "project_mentions": analysis.project_mentions
    }

    output_path.write_text(json.dumps(data, indent=2))
