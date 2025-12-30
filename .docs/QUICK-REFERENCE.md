# Quick Reference Card

One-page reference for the most common commands and conventions.

---

## Essential Commands

### Project Management

```bash
# Create new project
/new-project category=work container=client-projects name=project-name

# Check project status
/status                    # All projects
/status category=work      # Work projects only

# Update project metadata
cd ~/projects/category/container/project-name
/update-project status=completed
/update-project priority=high
/update-project due=2025-03-31

# Rename project
cd ~/projects/category/container/old-name
/rename-project new-name='new-name'
```

### HubSpot Integration

```bash
# Sync with HubSpot
cd ~/projects/work/client-projects/project-name
/hubspot-sync company='Company Name'

# Preview changes (dry run)
/hubspot-sync company='Company Name' --dry-run

# Partial syncs
/hubspot-sync company='Company Name' --contacts-only
/hubspot-sync company='Company Name' --notes-only
/hubspot-sync company='Company Name' --from=2025-11-01 --to=2025-12-31
```

### Session Management

```bash
# Save current session
/save-session-state

# Restore previous session
/restore-session-state
# or simply say: "restore my session"
```

---

## File Locations

```
~/projects/                         # All projects
~/projects/personal/                # Personal projects
~/projects/development/             # Development projects
~/projects/family/                  # Family projects
~/projects/work/                    # Work projects

~/projects/.docs/                   # Complete documentation
~/projects/.templates/              # Project templates

~/.claude/skills/                   # All skills
~/.claude/logs/                     # Skill execution logs
~/.claude/backups/                  # Skill backups
~/.claude/session-state/            # Session snapshots
```

---

## Project Structure

```
project-name/
├── PROJECT.md          # Main project file (YAML + markdown)
├── tasks.md           # Task tracking
├── timeline.md        # Milestones and phases
├── ENTITIES.md        # People and organizations (optional)
├── docs/              # Additional documentation
├── assets/            # Files, images, attachments
│   └── hubspot-files/ # Downloaded from HubSpot
├── notes/             # General notes
└── meeting-notes/     # Meeting documentation (work projects)
```

---

## Key YAML Fields

```yaml
---
# Identity
title: "Human Readable Title"
category: "personal|development|family|work"
container: "subfolder-name"
status: "active|on-hold|completed|archived"
priority: "high|medium|low"

# Dates (ISO 8601: YYYY-MM-DD)
created: 2025-01-15
due: 2025-03-31       # or null
completed: null        # filled when done
last_updated: 2025-01-20

# Categorization
tags: [tag1, tag2]

# People
owner: "Your Name"
collaborators: []
stakeholders: []

# Metrics
progress_percent: 25   # 0-100
estimated_hours: 40
actual_hours: 15
tasks_total: 12
tasks_completed: 3

# Flags
blocked: false
needs_review: false

# HubSpot (auto-added by sync)
hubspot_company_id: "123456789"
hubspot_deal_id: "987654321"
hubspot_last_sync: "2025-01-20"
---
```

---

## Naming Conventions

### Directories & Files

```
✅ GOOD:
- project-name            (lowercase-with-hyphens)
- api-documentation.md    (lowercase-with-hyphens.md)
- 2025-01-15-meeting.md   (dates: YYYY-MM-DD-description.md)

❌ BAD:
- Project Name            (spaces, capitals)
- API_Documentation.md    (underscores, capitals)
- 01-15-2025-meeting.md   (wrong date format)
```

### Status Values

```yaml
status: "active"       # Currently working on
status: "on-hold"      # Paused, will resume
status: "completed"    # Successfully finished
status: "archived"     # No longer relevant
```

### Priority Values

```yaml
priority: "high"       # Urgent, time-sensitive
priority: "medium"     # Important, flexible timeline
priority: "low"        # Nice-to-have, low urgency
```

---

## Task Status Symbols

```
[ ]  - Not started
[→]  - In progress
[✓]  - Completed
[!]  - Blocked
[~]  - On hold
[×]  - Cancelled
```

---

## Common Git Commands

```bash
# Check status
cd ~/projects
git status

# Add all changes
git add -A

# Commit with message
git commit -m "Descriptive message here"

# Push to remote
git push

# View recent commits
git log --oneline -5

# Restore file from Git
git checkout FILE
```

---

## Weekly Checklist

```
Monday Morning or Friday Afternoon (15-30 minutes):

□ Run /status to see all active projects
□ For each active project:
  □ Update tasks.md (mark completed, add new)
  □ Update PROJECT.md (progress_percent, last_updated, actual_hours)
  □ Check timeline.md (milestones on track?)
  □ Document any blockers
□ Update category READMEs
□ Commit changes to Git
□ Plan next week's priorities
□ /save-session-state
```

---

## Monthly Checklist

```
Last Day of Month (45-60 minutes):

□ Run /status for all categories
□ Create monthly report in reports/monthly/YYYY-MM-report.md
□ Analyze project health (on track, at risk, blocked)
□ Archive completed projects
□ Update project priorities
□ Review and adjust timelines
□ Document lessons learned
□ Commit changes to Git
```

---

## HubSpot Quick Reference

### Prerequisites

```bash
# Set API key (one time)
echo 'export HUBSPOT_API_KEY="pat-na1-YOUR-KEY"' >> ~/.zshrc
source ~/.zshrc

# Verify
echo $HUBSPOT_API_KEY
```

### Data Flow

```
HubSpot Company → PROJECT.md (Client Information section)
HubSpot Deal → PROJECT.md (Deal Information section)
HubSpot Contacts → ENTITIES.md (People section)
HubSpot Meetings → meeting-notes/YYYY-MM-DD-title.md
HubSpot Files → assets/hubspot-files/
```

### Common Issues

```
401 Unauthorized → Check API key
403 Forbidden → Check API key scopes
404 Not Found → Company doesn't exist or no access
429 Rate Limit → Wait 10 seconds, retry
Company not found → Try shorter search or domain search
```

---

## Emergency Commands

### Rollback Failed Rename

```bash
# Check backup location
cat ~/.claude/backups/rename-project/*/BACKUP_INFO.json

# Restore from backup
cd ~/projects/category/container
rm -rf failed-new-name
cp -R ~/.claude/backups/rename-project/TIMESTAMP-old-name-backup/old-name .
```

### Fix Corrupted PROJECT.md

```bash
# Restore from Git
cd ~/projects/category/container/project-name
git checkout PROJECT.md

# Or restore from backup if available
cp PROJECT.md.backup PROJECT.md
```

### Check Skill Logs

```bash
# View recent logs
ls -lt ~/.claude/logs/skill-name/

# Read specific log
cat ~/.claude/logs/skill-name/TIMESTAMP-log.log

# Search logs
grep "ERROR" ~/.claude/logs/skill-name/*.log
```

---

## Keyboard Shortcuts (Terminal)

```
Ctrl+A     - Go to beginning of line
Ctrl+E     - Go to end of line
Ctrl+U     - Delete from cursor to beginning
Ctrl+K     - Delete from cursor to end
Ctrl+R     - Search command history
Ctrl+L     - Clear screen (or type 'clear')

↑ / ↓      - Navigate command history
Tab        - Auto-complete file/directory names
```

---

## Common File Paths

```bash
# Navigate to projects
cd ~/projects

# Navigate to work projects
cd ~/projects/work/client-projects

# Navigate to documentation
cd ~/projects/.docs

# Navigate to skills
cd ~/.claude/skills

# View logs
cd ~/.claude/logs

# View session state
cd ~/.claude/session-state
```

---

## Useful Shell Aliases (Optional)

Add to `~/.zshrc` or `~/.bashrc`:

```bash
# Quick navigation
alias p='cd ~/projects'
alias pw='cd ~/projects/work/client-projects'
alias pd='cd ~/projects/development'
alias pp='cd ~/projects/personal'
alias pf='cd ~/projects/family'

# Quick commands
alias pstatus='/status'
alias psave='/save-session-state'
alias prestore='/restore-session-state'

# Git shortcuts
alias gs='git status'
alias ga='git add -A'
alias gc='git commit -m'
alias gp='git push'
alias gl='git log --oneline -10'
```

Then reload: `source ~/.zshrc`

---

## Documentation Quick Access

```
Complete Index:     ~/projects/.docs/INDEX.md
Skills Guide:       ~/projects/.docs/skills/README.md
HubSpot Guide:      ~/projects/.docs/integrations/hubspot-setup-guide.md
File Reference:     ~/projects/.docs/file-structures/project-files-reference.md
Workflows:          ~/projects/.docs/workflows/common-workflows.md
```

**Or read online:**
```bash
cat ~/projects/.docs/INDEX.md
```

---

## Support

**Documentation**: `~/projects/.docs/INDEX.md`
**Main README**: `~/projects/README.md`
**Search docs**: `grep -r "search term" ~/projects/.docs/`
**Check logs**: `ls -lt ~/.claude/logs/`
**Check backups**: `ls -lt ~/.claude/backups/`

---

## Tips & Tricks

1. **Use tab completion** for file paths
2. **Run /status weekly** to stay on top of projects
3. **Commit to Git frequently** for safety
4. **Use --dry-run** before major changes
5. **Save session state** at end of work
6. **Keep PROJECT.md updated** weekly minimum
7. **Document blockers immediately**
8. **Archive completed projects** to reduce clutter
9. **Sync HubSpot monthly** for fresh data
10. **Review documentation** when learning new features

---

**Print this page and keep it handy!**

**Version**: 1.0.0
**Last Updated**: 2025-12-29
**Full Docs**: `~/projects/.docs/INDEX.md`
