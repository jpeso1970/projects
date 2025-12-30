# Project Management System

Welcome to your centralized project management system! This directory organizes all personal, development, family, and work projects in one structured location with powerful Claude AI automation.

---

## System Overview

### Philosophy
This system is designed to:
- **Centralize** all project information in one place
- **Standardize** project documentation for consistency
- **Simplify** tracking across multiple life domains
- **Automate** repetitive tasks with Claude agents and skills
- **Enable** easy status checks and reviews

### Structure
```
projects/
├── personal/     → Personal goals, health, finance, home
├── development/  → Software projects, learning, tools
├── family/       → Family events, coordination, shared projects
├── work/         → Client projects, internal work, strategic initiatives
├── .templates/   → Reusable project templates
└── .agents/      → Autonomous Claude agents for automation
```

---

## Quick Start

### Creating a New Project (Automated)

**Using the `/new-project` skill** (recommended):
```
/new-project category=personal container=health name=weight-loss-2025
```

The skill will:
- Prompt for project metadata
- Create all folders and files automatically
- Initialize templates with your data
- Update category README

### Creating a New Project (Manual)

1. **Choose the category**: personal, development, family, or work
2. **Navigate to or create a container** (e.g., personal/health/)
3. **Create project folder**: `mkdir project-name`
4. **Copy templates**:
   ```bash
   cd ~/projects/personal/health
   mkdir -p weight-loss-2025/{docs,assets,notes}
   cp ../.templates/PROJECT.md weight-loss-2025/
   cp ../.templates/tasks.md weight-loss-2025/
   cp ../.templates/timeline.md weight-loss-2025/
   ```
5. **Customize PROJECT.md** with your project details
6. **Start tracking tasks** in tasks.md

---

## Categories Explained

### Personal Projects (`/personal`)
**Purpose**: Self-improvement, personal goals, hobbies

**Common Containers**:
- `health/` - Fitness, wellness, medical
- `finance/` - Budgeting, investing, financial planning
- `home/` - Home improvement, organization
- `learning/` - Courses, skills, education
- `hobbies/` - Creative projects, hobbies

**Characteristics**:
- Simpler structure
- Goal-oriented
- Personal accountability focus
- Optional: progress journaling

---

### Development Projects (`/development`)
**Purpose**: Software development, technical learning, tools

**Common Containers**:
- `mobile-apps/` - iOS, Android projects
- `web-projects/` - Websites, web applications
- `tools/` - CLI tools, automation scripts
- `learning/` - Tech courses, tutorials
- `open-source/` - Contributions, own projects

**Characteristics**:
- Technical documentation focus
- Architecture diagrams
- Code quality tracking
- Repository integration
- Technical decision logs

---

### Family Projects (`/family`)
**Purpose**: Family coordination, events, shared goals

**Common Containers**:
- `events/` - Vacations, parties, gatherings
- `home/` - Family home projects
- `activities/` - Regular family activities
- `planning/` - Long-term family planning

**Characteristics**:
- Shared responsibilities
- Multiple people coordination
- Communication plans
- Budget sharing
- Emphasis on fun/enjoyment

---

### Work Projects (`/work`)
**Purpose**: Professional projects, client work, business

**Common Containers**:
- `client-projects/` - Client deliverables
- `internal/` - Internal company projects
- `strategic/` - Planning, strategy work
- `proposals/` - Business proposals

**Characteristics**:
- Meeting notes (critical!)
- Stakeholder tracking
- Budget management
- Deliverables tracking
- Professional documentation
- Client communication logs

---

## Automation with Claude AI

### Skills (User-Invoked Commands)

#### `/new-project` - Create New Project
Scaffolds a complete project with all templates and folders.
```
/new-project category=work container=client-projects name=abc-website
```

#### `/status` - Generate Status Report
Quick overview of all active projects or by category.
```
/status
/status category=work
```

#### `/update-project` - Update Project Metadata
Quick update of project metadata without manual file editing.
```
/update-project status=completed
/update-project priority=high
```

#### `/archive-project` - Archive Completed Project
Moves completed projects to _archived/ folder.
```
cd ~/projects/personal/health/old-project
/archive-project
```

### Agents (Autonomous Helpers)

#### weekly-review Agent
Conducts automated weekly project review. Identifies stale projects, overdue milestones, and generates action items.
```
"Help me review my active projects"
```

#### file-importer Agent
Imports and analyzes files into appropriate projects.
```
"I have 5 screenshots from my meeting, import them to the abc-website project"
```

#### asset-organizer Agent
Organizes project assets by type and date.
```
"Organize the assets folder in my vacation-planning project"
```

#### status-reporter Agent
Generates comprehensive status reports with metrics and visualizations.
```
"Generate a detailed status report for all my work projects"
```

---

## File Conventions

### Naming Standards

**Projects**: `lowercase-with-hyphens`
- Good: `weight-loss-2025`, `client-abc-website`
- Avoid: `Weight Loss 2025`, `Client ABC Website`

**Containers**: `lowercase-simple`
- Good: `health`, `client-projects`
- Avoid: `Health Projects`, `client_projects`

**Documents**: `lowercase-with-hyphens.md`
- Good: `meeting-notes.md`, `api-documentation.md`
- Avoid: `Meeting Notes.md`, `API_Documentation.md`

**Dates in filenames**: `YYYY-MM-DD-description.md`
- Good: `2025-01-15-kickoff-meeting.md`
- Avoid: `01-15-2025-kickoff.md`, `kickoff-meeting-jan-15.md`

---

## Metadata Standards

### Project Status Values
- **active**: Currently being worked on
- **on-hold**: Temporarily paused but will resume
- **completed**: Finished and successful
- **archived**: No longer relevant or abandoned

### Priority Levels
- **high**: Urgent, important, time-sensitive
- **medium**: Important but flexible timeline
- **low**: Nice-to-have, low urgency

### Tags
Use consistent tags across projects for easy filtering:
- `#urgent`, `#waiting`, `#blocked`
- `#quick-win`, `#long-term`
- `#learning`, `#production`
- `#review-needed`, `#approved`

---

## Project Structure

Each project follows this pattern:
```
category/container/project-name/
├── PROJECT.md          # Main project file (YAML frontmatter + markdown)
├── tasks.md           # Task tracking
├── timeline.md        # Milestones and phases
├── docs/              # Documentation folder
├── assets/            # Images, files, attachments
├── notes/             # General notes
└── meeting-notes/     # (Work projects only) Meeting documentation
```

---

## Maintenance & Reviews

### Daily Workflow
- Update tasks in tasks.md as you complete them
- Add notes to notes/ folder
- Import files with file-importer agent

### Weekly Review (15 minutes)
For each active project:
1. Run `/status` to see all active projects
2. Use weekly-review agent for analysis
3. Update task status in `tasks.md`
4. Update "Current Status" in `PROJECT.md`
5. Check timeline milestones in `timeline.md`
6. Identify blockers and next steps

### Monthly Review (30 minutes)
1. Generate comprehensive report with status-reporter agent
2. Review all active projects
3. Update project metadata (status, priority)
4. Archive completed projects with `/archive-project`
5. Clean up old notes and files
6. Adjust timelines as needed

### Quarterly Review (1 hour)
1. Evaluate which projects to continue/stop
2. Review completed projects for lessons learned
3. Plan new projects for next quarter
4. Update category README files

---

## Best Practices

### Starting a Project
1. **Define success** before starting (in PROJECT.md)
2. **Break down into phases** (in timeline.md)
3. **List all tasks** even if rough (in tasks.md)
4. **Set realistic deadlines** with buffer time
5. **Identify dependencies** and risks early
6. **Use `/new-project` skill** for consistency

### During a Project
1. **Update weekly** minimum (tasks and status)
2. **Track changes** to timeline/scope
3. **Document decisions** (especially for work/dev)
4. **Celebrate milestones** (mark in timeline.md)
5. **Communicate** with stakeholders/family
6. **Use agents** for file organization and imports

### Completing a Project
1. **Mark all tasks complete** in tasks.md
2. **Update status to "completed"** in PROJECT.md
3. **Fill retrospective section** (lessons learned)
4. **Archive with `/archive-project` skill**
5. **Clean up unnecessary files**

---

## Agent-Optimized Metadata

Projects use YAML frontmatter for agent parsing:

```yaml
---
title: "Project Title"
category: "personal|development|family|work"
status: "active|on-hold|completed|archived"
priority: "high|medium|low"
created: 2025-01-15
due: 2025-03-31
progress_percent: 25
tags: [tag1, tag2]
---
```

This enables:
- Automated status tracking
- Smart project suggestions
- Intelligent file imports
- Comprehensive reporting

---

## FAQ

**Q: Do I need all the template files for every project?**
A: No! Use what makes sense. Small personal projects might only need PROJECT.md and tasks.md.

**Q: Can I customize the templates?**
A: Absolutely! Templates are starting points. Adapt to your needs.

**Q: Should I use `/new-project` or create projects manually?**
A: Use `/new-project` for consistency and speed. Manual works too for simple projects.

**Q: How do I use the agents?**
A: Just ask Claude naturally: "Help me review my projects" or "Import these files to my vacation project"

**Q: What if my project spans multiple categories?**
A: Choose the primary category, then link to related projects in other categories.

**Q: How detailed should my tasks be?**
A: Detailed enough that "future you" understands what needs doing.

---

## System Benefits

### Core Benefits
1. **Centralized**: All projects in one location
2. **Consistent**: Standardized templates
3. **Flexible**: Category-specific customizations
4. **Scalable**: Easy to add new projects
5. **Trackable**: Built-in task and timeline tracking
6. **Reviewable**: Structured format enables reviews
7. **Portable**: Markdown files work everywhere

### Automation Benefits
8. **Rapid Setup**: Create projects in seconds
9. **Intelligent Insights**: Agents analyze project health
10. **Reduced Friction**: Quick updates via skills
11. **Automatic Organization**: File importer keeps things tidy
12. **Proactive Reviews**: Never miss important updates
13. **Data-Driven**: Metrics and visualizations
14. **Context-Aware**: Agents understand relationships

---

## Getting Help

**System created**: 2025-01-15
**Version**: 1.0
**Documentation Version**: 1.0.0

### 📚 Comprehensive Documentation

**Looking for detailed guides?** See [.docs/INDEX.md](./.docs/INDEX.md) for complete documentation:

- **[Skills Reference](./.docs/skills/README.md)** - Complete guide to all skills (/new-project, /hubspot-sync, etc.)
- **[HubSpot Integration](./.docs/integrations/hubspot-setup-guide.md)** - Complete HubSpot setup and usage guide
- **[File Structure Reference](./.docs/file-structures/project-files-reference.md)** - All YAML fields and file formats explained
- **[Common Workflows](./.docs/workflows/common-workflows.md)** - Step-by-step guides for 8 common tasks
- **[Documentation Index](./.docs/INDEX.md)** - Master index with search by use case and role

**Quick Links:**
- [Starting a New Client Project](./.docs/workflows/common-workflows.md#workflow-1-starting-a-new-client-project)
- [Weekly Project Review](./.docs/workflows/common-workflows.md#workflow-2-weekly-project-review)
- [HubSpot Troubleshooting](./.docs/integrations/hubspot-setup-guide.md#troubleshooting)

### File Locations

**Skills Location**: `~/.claude/skills/`
**Agents Location**: `~/projects/.agents/`
**Templates Location**: `~/projects/.templates/`
**Documentation**: `~/projects/.docs/`

For system updates or improvements, update this README and template files as you learn what works best for your workflow.

---

**Remember**: This system serves you. Adapt it as needed. The goal is to help you track and complete projects, not create busywork. Start simple with manual projects, then add automation as you identify needs.

Use `/new-project` to get started!
