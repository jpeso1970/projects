# Project Files Reference Guide

Complete reference for all file formats, YAML frontmatter fields, and file conventions in the project management system.

---

## Table of Contents

1. [PROJECT.md](#projectmd)
2. [tasks.md](#tasksmd)
3. [timeline.md](#timelinemd)
4. [ENTITIES.md](#entitiesmd)
5. [Meeting Notes](#meeting-notes)
6. [File Naming Conventions](#file-naming-conventions)

---

## PROJECT.md

The main project file with agent-optimized YAML frontmatter and markdown content.

### YAML Frontmatter

#### Required Fields

```yaml
---
# Project Identity
title: "Human-Readable Project Title"
category: "personal|development|family|work"
container: "subfolder-name"
status: "active|on-hold|completed|archived"
priority: "high|medium|low"

# Dates (ISO 8601 format: YYYY-MM-DD)
created: 2025-01-15
due: 2025-03-31           # or null if no deadline
completed: null            # filled when status=completed
last_updated: 2025-01-20

# Categorization
tags:
  - tag1
  - tag2
  - tag3

# People
owner: "Your Name"
collaborators: []          # or null
stakeholders: []           # or null

# Metrics (for agent tracking)
progress_percent: 25       # 0-100
estimated_hours: 40
actual_hours: 15
tasks_total: 12
tasks_completed: 3

# Links
related_projects: []       # or null
external_links: []         # or null
repository: null           # GitHub/GitLab URL or null

# Flags (for agent automation)
needs_review: false
blocked: false
auto_archive_on_complete: true
---
```

#### Field Descriptions

**title** (string, required)
- Human-readable project name
- Used in displays and reports
- Can contain spaces and special characters
- Example: `"Weight Loss Goal - 2025"`

**category** (enum, required)
- One of: `personal`, `development`, `family`, `work`
- Determines directory location
- Affects template customizations
- Cannot be changed without moving files

**container** (string, required)
- Subdirectory within category
- Groups related projects
- Lowercase, simple names
- Examples: `health`, `client-projects`, `mobile-apps`

**status** (enum, required)
- `active` - Currently being worked on
- `on-hold` - Paused but will resume
- `completed` - Successfully finished
- `archived` - No longer relevant
- Agents use this for filtering

**priority** (enum, required)
- `high` - Urgent, time-sensitive
- `medium` - Important, flexible timeline
- `low` - Nice-to-have, low urgency
- Helps agents suggest next actions

**created** (date, required)
- Project creation date
- ISO 8601 format: YYYY-MM-DD
- Automatically set by /new-project skill
- Never changes after creation

**due** (date or null, required)
- Target completion date
- ISO 8601 format: YYYY-MM-DD
- Use `null` if no specific deadline
- Agents use for deadline warnings

**completed** (date or null, required)
- Actual completion date
- Set to `null` until project completes
- Automatically filled when status changes to `completed`
- Used for velocity calculations

**last_updated** (date, required)
- Last modification date
- Should be updated with any significant change
- Used by agents to identify stale projects
- Update manually or via /update-project skill

**tags** (array, required)
- Flexible categorization
- Use for filtering and searching
- Common tags: `urgent`, `waiting`, `blocked`, `quick-win`, `learning`
- Can be empty array: `[]`

**owner** (string, required)
- Primary person responsible
- Usually your name
- For shared projects, use primary owner
- Example: `"Jason Pace"`

**collaborators** (array or null, optional)
- People working on project with you
- Can be empty array or null
- Format: `["Name 1", "Name 2"]`
- For family/team projects

**stakeholders** (array or null, optional)
- People who care about outcomes
- Not necessarily working on it
- Important for work projects
- Format: `["Name 1", "Name 2"]` or null

**progress_percent** (integer, required)
- Completion percentage: 0-100
- Manual estimate or calculated from tasks
- Agents use for progress tracking
- Update weekly

**estimated_hours** (number, required)
- Initial time estimate
- Can be refined as project progresses
- Use 0 if unknown
- Helps with capacity planning

**actual_hours** (number, required)
- Actual time spent
- Track for future estimation accuracy
- Update periodically
- Use 0 if not tracking time

**tasks_total** (integer, required)
- Total number of tasks
- Auto-updated by agents (future)
- Manual update for now
- Sync with tasks.md

**tasks_completed** (integer, required)
- Number of completed tasks
- Used to calculate progress_percent
- Manual update for now
- Keep in sync with tasks.md

**related_projects** (array or null, optional)
- Links to related projects
- Format: relative paths
- Example: `["../other-project", "../../personal/health/related-project"]`
- Or null if none

**external_links** (array or null, optional)
- Links to external resources
- Websites, docs, repositories
- Format: `["https://example.com", "https://docs.example.com"]`
- For HubSpot links, clients, etc.

**repository** (string or null, optional)
- Git repository URL
- Mainly for development projects
- Example: `"https://github.com/user/repo"`
- Use null if not applicable

**needs_review** (boolean, required)
- Flag for agent attention
- Set to true when review needed
- Agents can proactively offer help
- Reset to false after review

**blocked** (boolean, required)
- True if project is blocked
- Waiting on external factors
- Agents will highlight in reports
- Document blocker in project notes

**auto_archive_on_complete** (boolean, required)
- Auto-move to _archived/ when completed
- Usually set to true
- Set to false for reference projects
- Keeps active directories clean

#### Optional Custom Fields

You can add custom fields for specific needs:

```yaml
# Client/Work-specific
hubspot_company_id: "123456789"
hubspot_deal_id: "987654321"
hubspot_last_sync: "2025-01-20"
client_name: "Acme Corporation"
contract_value: 125000

# Development-specific
tech_stack: ["React", "Node.js", "PostgreSQL"]
deployment_url: "https://app.example.com"
api_version: "v2.1"

# Personal-specific
habit_frequency: "daily"
target_metric: "weight"
starting_value: 180
target_value: 165
```

### Markdown Sections

After the YAML frontmatter, PROJECT.md contains markdown sections:

```markdown
---
# YAML frontmatter above
---

# Project Title

## Overview

**Purpose**: Brief statement of why this project exists

**Context**: Background information, how it fits into larger goals

**Success Criteria**: What does "done" look like?
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Current Status

**Status**: Active
**Progress**: 25%
**Last Updated**: 2025-01-20

### Recent Updates
- YYYY-MM-DD: What happened
- YYYY-MM-DD: Another update

### Next Steps
1. First action item
2. Second action item
3. Third action item

## Project Details

### Goals
1. **Primary Goal**: Main objective
2. **Secondary Goal**: Supporting objective
3. **Stretch Goal**: Nice-to-have outcome

### Scope

**In Scope**:
- Item 1
- Item 2
- Item 3

**Out of Scope**:
- Item 1
- Item 2

### Constraints
- **Time**: Deadline or timeframe constraints
- **Budget**: Financial limitations (if applicable)
- **Resources**: Available resources and limitations
- **Dependencies**: What this project depends on

### Risks
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Risk 1 | High/Med/Low | High/Med/Low | How to address |
| Risk 2 | High/Med/Low | High/Med/Low | How to address |

## Resources

### Documentation
- [Tasks](./tasks.md) - Task tracking and todo list
- [Timeline](./timeline.md) - Milestones and phases
- See [docs/](./docs/) folder for additional documentation

### Assets
- See [assets/](./assets/) folder for files, images, etc.

### Notes
- See [notes/](./notes/) folder for general notes and ideas

## Metrics & Tracking

### Key Metrics
- **Metric 1**: Description (Target: X, Current: Y)
- **Metric 2**: Description (Target: X, Current: Y)

### Time Tracking
- **Estimated Time**: 40 hours
- **Actual Time**: 15 hours
- **Time Remaining**: 25 hours

## Retrospective

### What Went Well
- (To be filled on completion)

### What Could Be Improved
- (To be filled on completion)

### Lessons Learned
- (To be filled on completion)

---

**Project Created**: 2025-01-15
**Last Updated**: 2025-01-20
**Project Owner**: Your Name
```

---

## tasks.md

Task tracking file with checkboxes and status indicators.

### Structure

```markdown
# Tasks - Project Name

**Project**: [Link to PROJECT.md](./PROJECT.md)
**Last Updated**: 2025-01-20

## Task Overview

**Total Tasks**: 12
**Completed**: 3
**In Progress**: 2
**Blocked**: 1

**Progress**: 25%

---

## Task Status Legend

- `[ ]` - Not started
- `[→]` - In progress
- `[✓]` - Completed
- `[!]` - Blocked
- `[~]` - On hold
- `[×]` - Cancelled

---

## Active Tasks

### High Priority
- [→] Task 1 - Description of what needs to be done
  - Due: 2025-01-25
  - Assignee: Name
  - Notes: Additional context

- [ ] Task 2 - Another high priority task
  - Due: 2025-01-31
  - Assignee: Name

### Medium Priority
- [ ] Task 3 - Medium priority task
- [ ] Task 4 - Another medium task

### Low Priority
- [ ] Task 5 - Low priority task
- [ ] Task 6 - Nice to have task

---

## Blocked Tasks

### Task Name That's Blocked
- **Blocked by**: What's preventing progress
- **Resolution needed**: What needs to happen to unblock
- **Owner**: Who should resolve the blocker

---

## Backlog

### Future Tasks (Not Yet Scheduled)
- [ ] Backlog item 1
- [ ] Backlog item 2
- [ ] Backlog item 3

---

## Completed Tasks

### Week of 2025-01-15
- [✓] Example completed task - Completed 2025-01-16
- [✓] Another completed task - Completed 2025-01-18

---

## Task Details Template

When you need more detail for a task:

```markdown
### [Task Name]
- **Status**: Not Started / In Progress / Completed / Blocked
- **Priority**: High / Medium / Low
- **Due Date**: YYYY-MM-DD
- **Assignee**: Name
- **Estimated Time**: X hours
- **Actual Time**: X hours
- **Dependencies**: Other tasks this depends on
- **Subtasks**:
  - [ ] Subtask 1
  - [ ] Subtask 2
- **Notes**: Additional context, decisions, or links
- **Completion Notes**: What was done (fill on completion)
```
```

### Best Practices

- Review tasks weekly
- Update progress regularly
- Break large tasks into smaller subtasks
- Archive completed tasks monthly
- Use tags for filtering: #urgent #waiting #research
- Keep task list < 20 active items

---

## timeline.md

Project timeline with phases, milestones, and calendar view.

### Structure

```markdown
# Timeline - Project Name

**Project**: [Link to PROJECT.md](./PROJECT.md)
**Last Updated**: 2025-01-20

## Project Timeline Overview

**Start Date**: 2025-01-15
**Target End Date**: 2025-03-31
**Duration**: 11 weeks
**Current Phase**: Phase 1 - Planning

---

## Phases

### Phase 1: Planning & Setup
**Dates**: 2025-01-15 → 2025-01-31
**Status**: In Progress
**Progress**: 50%

**Objectives**:
- [✓] Define project scope
- [→] Gather requirements
- [ ] Create initial plan
- [ ] Set up project structure

**Deliverables**:
- Project charter
- Requirements document
- Initial timeline

**Notes**:
- Stakeholder meeting scheduled for 2025-01-25

---

### Phase 2: Implementation
**Dates**: 2025-02-01 → 2025-03-15
**Status**: Not Started
**Progress**: 0%

**Objectives**:
- [ ] Objective 1
- [ ] Objective 2
- [ ] Objective 3

**Deliverables**:
- Deliverable 1
- Deliverable 2

---

### Phase 3: Review & Launch
**Dates**: 2025-03-16 → 2025-03-31
**Status**: Not Started
**Progress**: 0%

**Objectives**:
- [ ] Final review
- [ ] Testing
- [ ] Launch preparation
- [ ] Documentation

**Deliverables**:
- Final product/outcome
- Documentation
- Lessons learned

---

## Milestones

| Milestone | Target Date | Actual Date | Status | Notes |
|-----------|-------------|-------------|--------|-------|
| Project Kickoff | 2025-01-15 | 2025-01-15 | ✓ Complete | |
| Planning Complete | 2025-01-31 | - | In Progress | |
| Phase 2 Start | 2025-02-01 | - | Pending | |
| Mid-project Review | 2025-02-28 | - | Pending | |
| Phase 2 Complete | 2025-03-15 | - | Pending | |
| Final Review | 2025-03-25 | - | Pending | |
| Project Complete | 2025-03-31 | - | Pending | |

---

## Calendar View

### January 2025
```
Week 1 (Jan 1-5):   [Setup]
Week 2 (Jan 6-12):  [Planning]
Week 3 (Jan 13-19): [Planning]
Week 4 (Jan 20-26): [Planning]
Week 5 (Jan 27-31): [Phase 1 Complete]
```

### February 2025
```
Week 1 (Feb 1-7):   [Implementation Start]
Week 2 (Feb 8-14):  [Implementation]
Week 3 (Feb 15-21): [Implementation]
Week 4 (Feb 22-28): [Mid-project Review]
```

### March 2025
```
Week 1 (Mar 1-7):   [Implementation]
Week 2 (Mar 8-14):  [Implementation Final Push]
Week 3 (Mar 15-21): [Review & Testing]
Week 4 (Mar 22-31): [Launch Prep & Complete]
```

---

## Dependencies Timeline

```
Task A ──────────┐
                 ├──> Task C ───────┐
Task B ──────────┘                  ├──> Task E
                                    │
Task D ─────────────────────────────┘
```

**Key Dependencies**:
1. Task A & B must complete before Task C
2. Task C & D must complete before Task E

---

## Critical Path

**Critical tasks that affect the end date**:
1. Task 1 (Jan 15-20) - 5 days
2. Task 2 (Jan 21-31) - 10 days
3. Task 3 (Feb 1-28) - 28 days
4. Task 4 (Mar 1-15) - 15 days
5. Task 5 (Mar 16-31) - 15 days

**Total Critical Path Duration**: 73 days

---

## Timeline Changes Log

| Date | Change | Reason | Impact |
|------|--------|--------|--------|
| 2025-01-15 | Initial timeline created | Project start | N/A |
| 2025-01-22 | Phase 1 extended by 3 days | Additional requirements | Slight delay |

---

## Notes

- Update this timeline weekly or when significant changes occur
- Mark milestones as completed when achieved
- Document any timeline changes in the log above
- Use this for project status meetings and reviews
```

---

## ENTITIES.md

Track all people, organizations, and systems mentioned in the project.

### Structure

```markdown
# Entities - Project Name

This file tracks all people, organizations, and systems mentioned in project documentation.

**Last Updated**: 2025-01-20
**HubSpot Sync**: 2025-01-18

---

## People

### Client Team (Acme Corporation)

- **John Smith** - CEO
  - Email: john.smith@acme.com
  - Phone: (555) 123-4567
  - HubSpot: [View Contact](https://app.hubspot.com/contacts/contact/123456)
  - Source: HubSpot (synced 2025-01-18)
  - Notes: Primary decision maker, prefers email communication

- **Jane Doe** - CTO
  - Email: jane.doe@acme.com
  - Phone: (555) 123-4568
  - HubSpot: [View Contact](https://app.hubspot.com/contacts/contact/789012)
  - Source: HubSpot (synced 2025-01-18)
  - Notes: Technical lead, available for weekly syncs

### Our Team

- **Jason Pace** - Project Lead
  - Email: jason@example.com
  - Role: Primary contact, overall project management
  - Availability: Mon-Fri 9am-5pm

- **Sarah Johnson** - Developer
  - Email: sarah@example.com
  - Role: Frontend development
  - Availability: Tue-Sat 10am-6pm

---

## Organizations & Systems

### Acme Corporation
- **Type**: Client Company
- **Industry**: Technology
- **Location**: San Francisco, CA
- **Website**: https://acme.com
- **HubSpot**: [View Company](https://app.hubspot.com/contacts/company/456789)
- **Added**: 2025-01-15
- **Notes**: Fortune 500 company, 500+ employees

### External Services

#### Service Name
- **Type**: SaaS / API / Tool
- **Purpose**: What it's used for
- **URL**: https://service.com
- **Access**: Who has access
- **Notes**: Additional context

---

## Roles & Responsibilities

### Project Roles

| Role | Person | Responsibilities |
|------|--------|-----------------|
| Project Lead | Jason Pace | Overall coordination, client communication |
| Developer | Sarah Johnson | Frontend implementation |
| Reviewer | John Smith (Client) | Approval authority |

---

## Communication Matrix

| Person | Email | Phone | Preferred Method | Response Time |
|--------|-------|-------|-----------------|--------------|
| John Smith | john.smith@acme.com | (555) 123-4567 | Email | < 24 hours |
| Jane Doe | jane.doe@acme.com | (555) 123-4568 | Slack | < 4 hours |

---

## Notes

- Keep this file updated as new people join the project
- Add contact preferences and communication notes
- Link to HubSpot for most current information
- Archive contacts when they leave projects

---

*Last Updated*: 2025-01-20
*HubSpot Sync*: 2025-01-18
```

### Best Practices

- Add all people mentioned in meetings
- Include communication preferences
- Update when people change roles
- Link to HubSpot for client contacts
- Add context notes (timezone, availability, preferences)

---

## Meeting Notes

Individual meeting note files in `meeting-notes/` directory.

### Naming Convention

```
YYYY-MM-DD-meeting-topic.md
```

Examples:
- `2025-01-15-project-kickoff.md`
- `2025-01-22-weekly-sync.md`
- `2025-02-05-requirements-review.md`

### Structure

```markdown
# Meeting Title

**Date**: 2025-01-22
**Time**: 10:00 AM - 11:00 AM PST
**Type**: Weekly Sync / Kickoff / Review / etc.
**Location**: Zoom / Office / Phone
**Source**: Manual / HubSpot

---

## Attendees

**Present**:
- John Smith (Acme Corporation) - CEO
- Jane Doe (Acme Corporation) - CTO
- Jason Pace (Our Team) - Project Lead

**Absent**:
- Sarah Johnson (Our Team) - Developer (conflict)

---

## Agenda

1. Review progress from last week
2. Discuss current blockers
3. Plan next week's priorities
4. Q&A

---

## Discussion Notes

### Topic 1: Progress Review
- Completed items X, Y, Z
- On track for milestone
- Client expressed satisfaction with progress

### Topic 2: Blockers
- **Blocker 1**: Waiting on API documentation
  - **Owner**: Jane Doe
  - **Due**: 2025-01-25

- **Blocker 2**: Design approval needed
  - **Owner**: John Smith
  - **Due**: 2025-01-29

### Topic 3: Next Week's Plan
- Focus on implementation of feature A
- Schedule design review meeting
- Prepare demo for stakeholders

---

## Action Items

- [ ] Jason: Send meeting summary to team (Due: 2025-01-23)
- [ ] Jane: Provide API documentation (Due: 2025-01-25)
- [ ] John: Review and approve designs (Due: 2025-01-29)
- [ ] Sarah: Implement feature A (Due: 2025-01-31)

---

## Decisions Made

1. **Decision**: Use REST API instead of GraphQL
   - **Rationale**: Simpler integration, team more familiar
   - **Impact**: Affects backend architecture

2. **Decision**: Weekly sync meetings every Tuesday 10am PST
   - **Rationale**: Consistent communication
   - **Impact**: Block calendars accordingly

---

## Next Meeting

**Date**: 2025-01-29
**Time**: 10:00 AM PST
**Agenda**: Feature A demo, design review, sprint planning

---

## Attachments

- [Presentation Slides](../assets/2025-01-22-weekly-sync-slides.pdf)
- [Design Mockups](../assets/design-v2.png)

---

**Notes taken by**: Jason Pace
**Distributed to**: All attendees + Sarah Johnson

---

*Meeting imported from HubSpot on 2025-01-22* (if applicable)
*HubSpot Engagement ID: 123456789* (if applicable)
```

### Meeting Notes Best Practices

- Create immediately after meeting while fresh
- Use consistent naming (YYYY-MM-DD-topic.md)
- Distribute to all attendees + those who should know
- Track action items to completion
- Link to related files in assets/
- Archive old meeting notes periodically

---

## File Naming Conventions

### General Rules

1. **Lowercase only**: `project-name` not `Project-Name`
2. **Hyphens for spaces**: `my-project` not `my_project` or `myproject`
3. **No special characters**: Avoid `@#$%^&*()`
4. **Descriptive names**: `api-documentation` not `doc1`
5. **Dates first when relevant**: `2025-01-15-meeting.md`

### Project Directories

```
✅ Good:
- weight-loss-2025
- acme-website-redesign
- mobile-app-development

❌ Bad:
- Weight Loss 2025
- Acme_Website_Redesign
- mobileAppDev
```

### Document Files

```
✅ Good:
- api-documentation.md
- technical-architecture.md
- 2025-01-15-kickoff-meeting.md

❌ Bad:
- API Documentation.md
- technical_architecture.md
- Meeting-01-15-2025.md
```

### Asset Files

```
✅ Good:
- company-logo.png
- 2025-q1-budget.xlsx
- database-schema-v2.pdf

❌ Bad:
- Company Logo.png
- Budget_Q1_2025.xlsx
- db-schema.pdf (version unclear)
```

### Date Formats

**For filenames**: `YYYY-MM-DD`
```
2025-01-15-meeting-notes.md
2025-03-31-project-complete.md
```

**For YAML**: ISO 8601 `YYYY-MM-DD`
```yaml
created: 2025-01-15
due: 2025-03-31
```

**For display**: Natural format
```markdown
**Date**: January 15, 2025
**Last Updated**: 2025-01-20
```

---

## Directory Structure

Standard project layout:

```
project-name/
├── PROJECT.md          # Main project file with YAML
├── tasks.md           # Task tracking
├── timeline.md        # Milestones and phases
├── ENTITIES.md        # People and organizations (optional)
├── docs/              # Additional documentation
│   ├── api-docs.md
│   ├── architecture.md
│   └── technical-specs.md
├── assets/            # Files, images, attachments
│   ├── images/
│   ├── documents/
│   └── hubspot-files/ (if synced with HubSpot)
│       ├── contracts/
│       ├── documents/
│       ├── presentations/
│       └── other/
├── notes/             # General notes and ideas
│   ├── 2025-01-15-initial-ideas.md
│   └── brainstorm.md
└── meeting-notes/     # Meeting documentation (work projects)
    ├── 2025-01-15-kickoff.md
    ├── 2025-01-22-weekly-sync.md
    └── README.md
```

---

## Template Usage

### When Creating Projects Manually

1. Copy templates from `~/projects/.templates/`
2. Customize YAML frontmatter
3. Update project-specific sections
4. Remove unused sections
5. Add category-specific sections as needed

### When Using /new-project Skill

Skill automatically:
- Copies and customizes templates
- Sets current dates
- Fills in YAML metadata
- Creates directory structure
- Updates category README

---

## Version Control

### What to Commit

✅ **Always commit:**
- PROJECT.md
- tasks.md
- timeline.md
- ENTITIES.md
- docs/ content
- notes/ content
- meeting-notes/ content

✅ **Usually commit:**
- Small assets (< 1MB)
- Text-based assets
- Essential documents

### What NOT to Commit

❌ **Never commit:**
- API keys or credentials
- `.env` files
- Personal sensitive data
- Client confidential information
- Very large files (> 10MB)

❌ **Usually don't commit:**
- Temporary notes
- Downloaded HubSpot attachments (can re-sync)
- Large binary files
- Auto-generated reports

### .gitignore Example

```
# Credentials
.env
.env.local
credentials.json

# Large files
assets/hubspot-files/
*.zip
*.tar.gz

# OS files
.DS_Store
Thumbs.db

# Temporary
*.tmp
*.temp
~*
```

---

## Maintenance

### Weekly
- Update tasks.md with progress
- Update last_updated date in PROJECT.md
- Review and triage new files

### Monthly
- Archive completed tasks
- Update progress_percent
- Clean up old notes
- Review timeline accuracy

### Project Completion
- Fill retrospective section
- Update status to "completed"
- Set completed date
- Run `/archive-project` if desired

---

**Last Updated**: 2025-12-29
**Documentation Version**: 1.0.0
