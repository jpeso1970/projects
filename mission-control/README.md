# Mission Control - Project Dashboard

Fast, terminal-based "mission control" dashboard for managing all your projects.

## Features (MVP - Phase 1)

✅ **Visual Project Grid**: See all projects at a glance with color-coded status
✅ **Smart Highlighting**: Blockers, overdue, and stale projects prominently displayed
✅ **Fast Startup**: < 1 second for typical project counts
✅ **Zero Dependencies**: Pure Python stdlib (no PyYAML required!)
✅ **Keyboard Navigation**: Arrow keys, vim-style (j/k), and quick commands

## Installation

The dashboard is already installed at:
```
~/.claude/skills/mission-control/
```

## Usage

Launch Mission Control:
```bash
~/.claude/skills/mission-control/mc
```

Or create a symlink for easier access:
```bash
ln -s ~/.claude/skills/mission-control/mc /usr/local/bin/mc
mc
```

## Keyboard Commands

- **↑/↓** or **k/j**: Navigate project list
- **s**: Cycle sort order (priority → due date → last updated → name → risk)
- **r**: Refresh data from disk
- **Home/End**: Jump to first/last project
- **q**: Quit

## Color Coding

- 🟢 **Green**: Active projects
- 🟡 **Yellow**: On-hold
- 🔴 **Red**: Blocked or overdue
- 🔵 **Blue**: Completed
- ⚪ **Gray**: Stale (7+ days since update)

## Project Display

Each row shows:
- **Emoji indicator**: Status at a glance (🚫 blocked, 📌 high priority, ⏰ overdue)
- **Project name**: Truncated to 30 characters
- **Status**: ACTV, HOLD, BLCK, DONE
- **Priority**: HIGH, MED, LOW
- **Progress bar**: Visual [███░░░] with percentage
- **Due date**: Formatted as "Jan 15" or "--" if none
- **Last updated**: "3d" (3 days ago), "today", "yest"

## Attention Panel

The bottom panel highlights projects needing attention:
- 🚫 **BLOCKED**: Projects with `blocked: true` flag
- ⏰ **OVERDUE**: Past due date and not completed
- 📅 **STALE**: Not updated in 7+ days

## Technical Details

- **Zero dependencies**: Uses pure Python stdlib (no PyYAML)
- **Fast parsing**: Simple regex-based YAML parser for predictable PROJECT.md structure
- **Cached properties**: Risk scores and computed values cached for performance
- **Curses UI**: Terminal-native interface, no browser needed

## Project Discovery

Mission Control automatically discovers all PROJECT.md files under:
```
~/projects/
```

Excluded directories:
- `.templates`
- `_archived`
- `.git`
- `.agents`
- `.docs`

## Coming Soon (Phase 2-5)

🔜 Blocker board view (press 'b')
🔜 Quick update panel (press 'u')
🔜 HubSpot bulk sync (press 'h')
🔜 Filtering by status/category/priority
🔜 Search/fuzzy find
🔜 Help screen (press '?')

## Files

```
~/.claude/skills/mission-control/
├── mc                      # Executable launcher
├── README.md              # This file
├── src/
│   ├── main.py            # Main application entry
│   ├── models.py          # Project dataclass
│   ├── loader.py          # PROJECT.md discovery & parsing
│   ├── views/
│   │   └── dashboard.py   # Main grid view
│   └── utils/
│       └── date_utils.py  # Date formatting helpers
```

## Version

v0.1.0 - MVP Phase 1 Complete

## Support

For issues or feature requests, see your Claude Code session or update the SKILL.md file.
