# Skills Reference Guide

This directory contains comprehensive documentation for all Claude Code skills used in the project management system.

## Available Skills

### Project Management Skills

1. **[new-project](./new-project.md)** - Create new projects with templates and structure
2. **[update-project](./update-project.md)** - Update project metadata and settings
3. **[rename-project](./rename-project.md)** - Rename projects and propagate changes
4. **[status](./status.md)** - Generate project status reports

### Session Management Skills

5. **[save-session-state](./save-session-state.md)** - Save current session context
6. **[restore-session-state](./restore-session-state.md)** - Restore previous session context

### Integration Skills

7. **[hubspot-sync](./hubspot-sync.md)** - Sync projects with HubSpot CRM data

---

## Quick Reference

### Creating a New Project
```bash
/new-project category=work container=client-projects name=client-abc
```

### Syncing with HubSpot
```bash
/hubspot-sync company='Company Name'
```

### Renaming a Project
```bash
cd ~/projects/work/client-projects/old-name
/rename-project new-name='new-project-name'
```

### Checking Project Status
```bash
/status
/status category=work
```

### Updating Project Metadata
```bash
cd ~/projects/work/client-projects/project-name
/update-project status=completed priority=high
```

### Saving Session State
```bash
/save-session-state
```

### Restoring Session State
```bash
/restore-session-state
```

---

## Skill Installation

Skills are stored in `~/.claude/skills/` and are automatically available in Claude Code.

**User Skills Location**: `~/.claude/skills/`
**Plugin Skills**: Managed by Claude Code plugins

---

## Skill Development

To create a new skill:

1. Create a directory: `~/.claude/skills/skill-name/`
2. Create `SKILL.md` with skill instructions
3. Follow the skill template format
4. Test thoroughly before using in production

---

## Best Practices

### When to Use Skills

- **Use `/new-project`** for all new projects (consistency)
- **Use `/hubspot-sync`** when starting client projects (data accuracy)
- **Use `/rename-project`** for all renames (propagation)
- **Use `/update-project`** for metadata changes (speed)
- **Use `/status`** for weekly reviews (oversight)
- **Use session management** before ending work sessions (continuity)

### When NOT to Use Skills

- Simple file reads (use Read tool directly)
- One-off changes (edit files manually)
- Experimental changes (manual control is better)
- Learning the system (do it manually first)

---

## Troubleshooting

### Skill Not Found
- Check `~/.claude/skills/skill-name/` exists
- Verify `SKILL.md` file is present
- Restart Claude Code if needed

### Permission Errors
- Check file permissions: `chmod +x script.sh`
- Verify directory write permissions
- Check for locked files

### Skill Fails Partway Through
- Check logs in `~/.claude/logs/skill-name/`
- Review backup in `~/.claude/backups/skill-name/`
- Use rollback procedures if available

---

**Last Updated**: 2025-12-29
**Documentation Version**: 1.0.0
