# Project Management System - Complete Documentation

Comprehensive documentation for the Claude Code-powered project management system.

**Version**: 1.0.0
**Last Updated**: 2025-12-29
**Maintained By**: Jason Pace

---

## Quick Start

**New to the system?** Start here:
1. Read the [Main README](../README.md) for system overview
2. Review [File Structure Reference](./file-structures/project-files-reference.md) to understand file formats
3. Try [Workflow: Starting a New Project](./workflows/common-workflows.md#workflow-1-starting-a-new-client-project)

**For client projects:** Follow the [HubSpot Integration Setup Guide](./integrations/hubspot-setup-guide.md)

---

## Documentation Structure

### 📚 Core Documentation

#### [Main README](../README.md)
System overview, philosophy, quick start guide, and general best practices.

**Contents:**
- System philosophy and benefits
- Directory structure (personal, development, family, work)
- Quick start for manual and automated project creation
- Category explanations
- Basic automation overview
- File and naming conventions
- Agent-optimized metadata explanation

**When to read:** First time using the system, onboarding new users

---

### 🛠 Skills Documentation

#### [Skills Overview](./skills/README.md)
Complete reference for all Claude Code skills.

**Available Skills:**
- `/new-project` - Create projects with templates
- `/hubspot-sync` - Sync with HubSpot CRM
- `/rename-project` - Rename and propagate changes
- `/update-project` - Update project metadata
- `/status` - Generate status reports
- `/save-session-state` - Save work session
- `/restore-session-state` - Restore work session

**When to read:** Learning to use skills, troubleshooting skill issues

#### Individual Skill Guides

**Coming soon:**
- `skills/new-project.md` - Detailed new-project skill guide
- `skills/hubspot-sync.md` - Detailed HubSpot sync guide
- `skills/rename-project.md` - Detailed rename skill guide
- `skills/update-project.md` - Detailed update skill guide
- `skills/status.md` - Detailed status skill guide
- `skills/session-management.md` - Session state management guide

---

### 🔗 Integration Guides

#### [HubSpot Integration Setup](./integrations/hubspot-setup-guide.md)
Complete guide for setting up and using HubSpot CRM integration.

**Contents:**
- Prerequisites and requirements
- API key generation and configuration
- Environment variable setup
- Usage examples and options
- Data mapping (company, deal, contact, meeting → PROJECT.md, ENTITIES.md)
- Troubleshooting common issues
- Security best practices
- Integration workflows

**When to read:**
- Before starting first client project
- Setting up HubSpot integration
- Troubleshooting sync issues
- Understanding data mapping

#### Future Integrations

**Planned integrations:**
- GitHub/GitLab (automatic repository linking)
- Jira/Asana (task sync)
- Google Calendar (meeting sync)
- Notion (documentation export)

---

### 📁 File Structure Documentation

#### [Project Files Reference](./file-structures/project-files-reference.md)
Complete reference for all file formats, YAML frontmatter, and conventions.

**Contents:**
- **PROJECT.md**: All YAML frontmatter fields explained
- **tasks.md**: Task tracking format and conventions
- **timeline.md**: Timeline, phases, and milestones structure
- **ENTITIES.md**: People and organizations tracking
- **Meeting Notes**: Meeting note file format
- **File Naming Conventions**: Standards for files and directories
- **Directory Structure**: Complete project layout
- **Template Usage**: How templates work
- **Version Control**: Git best practices
- **Maintenance**: File maintenance schedules

**When to read:**
- Creating or customizing PROJECT.md files
- Understanding YAML frontmatter fields
- Looking up file format conventions
- Setting up version control

---

### 🔄 Workflow Guides

#### [Common Workflows](./workflows/common-workflows.md)
Step-by-step guides for common project management tasks.

**Workflows Included:**

1. **Starting a New Client Project** (30-45 min)
   - Create project structure
   - Sync HubSpot data
   - Customize project details
   - Set up tasks and timeline
   - Commit to Git

2. **Weekly Project Review** (15-30 min)
   - Generate status report
   - Update all active projects
   - Review timelines
   - Identify blockers
   - Plan next week

3. **Completing and Archiving a Project** (30-60 min)
   - Final task review
   - Fill retrospective
   - Clean up files
   - Update category README
   - Archive project

4. **Renaming a Project** (10-20 min)
   - Use rename-project skill
   - Verify all changes
   - Commit to Git
   - Update external references

5. **Re-syncing HubSpot Data** (15-30 min)
   - Run HubSpot sync
   - Review changes
   - Merge manual changes
   - Commit updates

6. **Session Management** (1-3 min)
   - Save session state
   - Restore session state
   - Best practices

7. **Monthly Status Report** (45-60 min)
   - Generate comprehensive report
   - Analyze project health
   - Create action items
   - Document lessons learned

8. **Handling Project Blockers** (10-15 min)
   - Document blocker
   - Create follow-up actions
   - Communicate with stakeholders
   - Track resolution

**When to read:**
- Before starting a new workflow
- When you need step-by-step guidance
- Learning best practices
- Troubleshooting workflow issues

---

### 📖 Examples & Templates

#### Coming Soon

**Example Projects:**
- `examples/personal-project-example/` - Sample personal project
- `examples/client-project-example/` - Sample work project with HubSpot sync
- `examples/development-project-example/` - Sample development project

**Templates:**
- Located in `~/projects/.templates/`
- PROJECT.md template
- tasks.md template
- timeline.md template
- meeting-notes template

---

## Navigation by Use Case

### I want to...

#### Create a new project
→ Read [Workflow: Starting a New Client Project](./workflows/common-workflows.md#workflow-1-starting-a-new-client-project)
→ Reference [Skills: new-project](./skills/README.md#new-project)

#### Integrate with HubSpot
→ Follow [HubSpot Integration Setup Guide](./integrations/hubspot-setup-guide.md)
→ Reference [Skills: hubspot-sync](./skills/README.md#hubspot-sync)

#### Understand PROJECT.md fields
→ Read [Project Files Reference: PROJECT.md](./file-structures/project-files-reference.md#projectmd)

#### Review my projects weekly
→ Follow [Workflow: Weekly Project Review](./workflows/common-workflows.md#workflow-2-weekly-project-review)

#### Rename a project
→ Follow [Workflow: Renaming a Project](./workflows/common-workflows.md#workflow-4-renaming-a-project)
→ Reference [Skills: rename-project](./skills/README.md#rename-project)

#### Complete and archive a project
→ Follow [Workflow: Completing and Archiving](./workflows/common-workflows.md#workflow-3-completing-and-archiving-a-project)

#### Handle a blocked project
→ Follow [Workflow: Handling Project Blockers](./workflows/common-workflows.md#workflow-8-handling-project-blockers)

#### Save my work session
→ Reference [Skills: save-session-state](./skills/README.md#save-session-state)
→ Follow [Workflow: Session Management](./workflows/common-workflows.md#workflow-6-session-management)

#### Generate a status report
→ Reference [Skills: status](./skills/README.md#status)
→ Follow [Workflow: Monthly Status Report](./workflows/common-workflows.md#workflow-7-monthly-status-report)

#### Troubleshoot HubSpot sync
→ Read [HubSpot Troubleshooting](./integrations/hubspot-setup-guide.md#troubleshooting)

#### Understand file naming conventions
→ Read [File Naming Conventions](./file-structures/project-files-reference.md#file-naming-conventions)

---

## Navigation by Role

### Project Manager
**Priority reading:**
1. [Main README](../README.md) - System overview
2. [Workflow: Starting Projects](./workflows/common-workflows.md#workflow-1-starting-a-new-client-project)
3. [Workflow: Weekly Reviews](./workflows/common-workflows.md#workflow-2-weekly-project-review)
4. [Workflow: Monthly Reports](./workflows/common-workflows.md#workflow-7-monthly-status-report)
5. [Skills Overview](./skills/README.md)

### Developer
**Priority reading:**
1. [File Structure Reference](./file-structures/project-files-reference.md)
2. [Main README: Development Projects](../README.md#development-projects)
3. [Workflow: Session Management](./workflows/common-workflows.md#workflow-6-session-management)
4. Version control best practices in [File Structure Reference](./file-structures/project-files-reference.md#version-control)

### Client Services / Sales
**Priority reading:**
1. [HubSpot Integration Setup](./integrations/hubspot-setup-guide.md)
2. [Workflow: Starting Client Projects](./workflows/common-workflows.md#workflow-1-starting-a-new-client-project)
3. [Workflow: Re-syncing HubSpot](./workflows/common-workflows.md#workflow-5-re-syncing-hubspot-data)
4. [Skills: hubspot-sync](./skills/README.md#hubspot-sync)

### System Administrator
**Priority reading:**
1. All documentation (comprehensive understanding)
2. [HubSpot Integration: Security](./integrations/hubspot-setup-guide.md#security-best-practices)
3. [File Structure: Version Control](./file-structures/project-files-reference.md#version-control)
4. [Skills Overview](./skills/README.md) - Understanding all automation

---

## Frequently Asked Questions

### Getting Started

**Q: Where do I start?**
A: Read the [Main README](../README.md), then try creating a simple project manually before using skills.

**Q: Do I need to use all the skills?**
A: No! Start with `/new-project` and add other skills as you need them.

**Q: What's the learning curve?**
A: 30 minutes to understand basics, 2-3 hours to become proficient, 1-2 weeks to master workflows.

### Project Management

**Q: How many projects should I have active?**
A: Depends on capacity. Generally 3-7 active projects per person is manageable.

**Q: How often should I update projects?**
A: Minimum weekly. Daily for high-priority projects.

**Q: Should I archive completed projects?**
A: Yes, if `auto_archive_on_complete: true`. Keeps active directories clean.

### HubSpot Integration

**Q: Is HubSpot integration required?**
A: No, only for client projects where you want CRM data synced.

**Q: Will syncing overwrite my manual changes?**
A: No, it adds HubSpot data alongside existing content.

**Q: How often should I sync?**
A: Initially at project creation, then monthly or after significant HubSpot updates.

### File Structure

**Q: Can I customize the templates?**
A: Yes! Templates in `~/projects/.templates/` are starting points.

**Q: Do I need all the template files?**
A: No, use what makes sense. Small projects might only need PROJECT.md and tasks.md.

**Q: Can I add custom YAML fields?**
A: Yes! Add any fields relevant to your projects.

### Version Control

**Q: Should I commit everything to Git?**
A: Commit PROJECT.md, tasks.md, timeline.md, ENTITIES.md, docs, and notes. Be cautious with large files and sensitive data.

**Q: How often should I commit?**
A: After significant changes, weekly reviews, and project milestones.

### Skills & Automation

**Q: What if a skill fails?**
A: Check logs in `~/.claude/logs/skill-name/`. Some skills have rollback features.

**Q: Can I create custom skills?**
A: Yes! Create in `~/.claude/skills/custom-skill-name/SKILL.md`.

**Q: Do skills require internet?**
A: HubSpot sync requires internet. Other skills work offline.

---

## Troubleshooting

### Common Issues

#### "Skill not found"
→ Check `~/.claude/skills/skill-name/` exists and contains `SKILL.md`

#### "HubSpot API error"
→ See [HubSpot Troubleshooting](./integrations/hubspot-setup-guide.md#troubleshooting)

#### "Git repository not found"
→ Run `git init` in `~/projects/` directory

#### "Permission denied"
→ Check file permissions: `chmod +x script.sh`

#### "Project files corrupted"
→ Restore from Git: `git checkout FILE` or from backup

### Getting Help

**Resources:**
- Check relevant documentation sections above
- Review workflow guides for step-by-step help
- Search documentation: `grep -r "search term" ~/projects/.docs/`
- Check logs: `~/.claude/logs/`
- Review backups: `~/.claude/backups/`

**Support Channels:**
- Internal team documentation
- Claude Code community
- GitHub issues (if public repository)

---

## Contributing to Documentation

### Updating Documentation

When you discover improvements:
1. Edit the relevant `.docs/` file
2. Update "Last Updated" date
3. Increment version if major changes
4. Commit with clear message

### Documentation Standards

- Use clear, concise language
- Include examples
- Provide step-by-step instructions
- Add "When to read" sections
- Cross-reference related docs
- Keep table of contents updated

### Adding New Documentation

Create new files in appropriate subdirectory:
- `skills/` - Skill-specific guides
- `integrations/` - Integration guides
- `file-structures/` - File format references
- `workflows/` - Step-by-step workflows
- `examples/` - Example projects

Then update this INDEX.md to include the new documentation.

---

## Documentation Roadmap

### Completed ✅
- Main README with system overview
- Skills overview document
- HubSpot integration comprehensive guide
- Project files reference (all formats)
- Common workflows (8 workflows)
- Documentation index (this file)

### In Progress 🚧
- Individual skill detailed guides
- Example projects
- Video tutorials

### Planned 📋
- Advanced workflows guide
- Integration guides (GitHub, Jira, etc.)
- Agent development guide
- Custom skill creation tutorial
- Best practices for teams
- Migration guide (from other systems)
- Keyboard shortcuts and CLI tips

---

## Version History

### Version 1.0.0 (2025-12-29)
**Initial comprehensive documentation release**

**Completed:**
- Main README enhanced
- Skills overview created
- HubSpot integration guide (complete)
- Project files reference (complete)
- Common workflows guide (8 workflows)
- Documentation index (this file)

**Total Documentation**: ~25,000 words across 6 major documents

**Files Created:**
- `.docs/INDEX.md` (this file)
- `.docs/skills/README.md`
- `.docs/integrations/hubspot-setup-guide.md`
- `.docs/file-structures/project-files-reference.md`
- `.docs/workflows/common-workflows.md`

---

## Quick Reference Card

### Essential Commands

```bash
# Create new project
/new-project category=work container=client-projects name=project-name

# Sync HubSpot
/hubspot-sync company='Company Name'

# Rename project
/rename-project new-name='new-name'

# Check status
/status

# Update project
/update-project status=completed

# Save/restore session
/save-session-state
/restore-session-state
```

### Key File Locations

```
~/projects/                          # All projects
~/projects/.docs/                    # This documentation
~/projects/.templates/               # Project templates
~/.claude/skills/                    # Skills
~/.claude/logs/                      # Skill logs
~/.claude/backups/                   # Skill backups
~/.claude/session-state/             # Session snapshots
```

### Important YAML Fields

```yaml
status: "active|on-hold|completed|archived"
priority: "high|medium|low"
blocked: true|false
needs_review: true|false
progress_percent: 0-100
hubspot_company_id: "123456789"
```

### File Naming

```
Projects: lowercase-with-hyphens
Files: lowercase-with-hyphens.md
Dates: YYYY-MM-DD-description.md
```

---

## Appendix

### Glossary

**Agent** - Autonomous Claude helper that performs tasks proactively
**Skill** - User-invoked command (like `/new-project`)
**Container** - Subdirectory within category (like `client-projects`)
**YAML Frontmatter** - Structured metadata at top of PROJECT.md
**HubSpot Sync** - Integration that pulls CRM data into projects
**Session State** - Saved work context for continuity
**Blocker** - Issue preventing project progress
**Retrospective** - Post-completion review and lessons learned

### File Extensions

- `.md` - Markdown files (documentation)
- `.json` - JSON files (session snapshots, backup info)
- `.log` - Log files (skill execution logs)
- `.yaml` or `.yml` - YAML files (configuration)

### Date Formats

- **ISO 8601**: `YYYY-MM-DD` (use in YAML and filenames)
- **Display**: "January 15, 2025" (use in markdown for readability)
- **Timestamps**: `YYYY-MM-DD HH:MM:SS` (use in logs)

---

**Documentation Maintained By**: Jason Pace
**Last Updated**: 2025-12-29
**Version**: 1.0.0
**License**: Internal Use

---

**Need help?** Start with the [Quick Start](#quick-start) section or navigate using the [Navigation by Use Case](#navigation-by-use-case) guide.

For comprehensive skill documentation, see [Skills Overview](./skills/README.md).
For HubSpot integration, see [HubSpot Integration Setup Guide](./integrations/hubspot-setup-guide.md).
For step-by-step workflows, see [Common Workflows](./workflows/common-workflows.md).
