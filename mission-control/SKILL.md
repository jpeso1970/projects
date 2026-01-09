# Mission Control Skill

## Overview

Mission Control is a fast, terminal-based dashboard for managing all your projects. Think `htop` for your project portfolio - instant visual overview, keyboard-driven navigation, and zero configuration.

**When to use**: Launch daily to see project status at a glance, identify blockers, spot stale projects, and understand what needs attention.

## Command

```bash
~/.claude/skills/mission-control/mc
```

Or after symlinking:
```bash
mc
```

## What it does

- **Discovers** all PROJECT.md files under ~/projects/
- **Parses** YAML frontmatter (status, priority, dates, metrics, flags)
- **Displays** color-coded grid with projects, progress, due dates
- **Highlights** blockers, overdue, and stale projects (7+ days)
- **Sorts** by priority, due date, last updated, name, or risk score
- **Refreshes** data on demand with 'r' key

## Features (Phase 1 MVP)

✅ **Visual Project Grid**
- Color-coded status (green=active, yellow=on-hold, red=blocked, blue=completed)
- Progress bars [███░░░] with percentages
- Due dates and last updated timestamps
- Emoji indicators (🚫 blocked, 📌 high priority, ⏰ overdue)

✅ **Attention Panel**
- Prominently shows blocked projects
- Highlights overdue projects (past due date)
- Flags stale projects (not updated in 7+ days)

✅ **Fast Performance**
- Zero external dependencies (pure Python stdlib)
- < 1 second startup for typical project counts
- Efficient caching of computed properties

✅ **Keyboard Navigation**
- Arrow keys or vim-style (j/k) to navigate
- 's' to cycle sort options
- 'r' to refresh data
- 'q' to quit

## Usage Examples

### Daily Status Check
```bash
mc
# Launches dashboard, see all projects at a glance
# Check attention panel for urgent items
# Press 'q' to exit
```

### Review by Priority
```bash
mc
# Press 's' repeatedly to cycle sort options
# Stops at "priority" sort (default)
# High priority projects at top
```

### Find Stale Projects
```bash
mc
# Look for gray-colored projects in grid
# Check attention panel for "STALE" items
# Navigate with arrow keys to review each one
```

## Keyboard Commands

| Key | Action |
|-----|--------|
| **↑/↓** | Navigate project list |
| **k/j** | Vim-style navigation (up/down) |
| **Home** | Jump to first project |
| **End** | Jump to last project |
| **s** | Cycle sort: priority → due date → last updated → name → risk |
| **r** | Refresh data from disk |
| **q** | Quit dashboard |

## Data Source

Mission Control reads from PROJECT.md files located at:
```
~/projects/**/**/PROJECT.md
```

Excluded directories:
- .templates
- _archived
- .git
- .agents
- .docs

## Color Legend

- 🟢 **Green** (active): Project is active and on track
- 🟡 **Yellow** (on-hold): Project temporarily paused
- 🔴 **Red** (blocked/overdue): Needs immediate attention
- 🔵 **Blue** (completed): Successfully finished
- ⚪ **Gray** (stale): Not updated recently (7+ days)

## Display Format

```
┏━━━━━━━━━━━━━━━━━━━━━ Mission Control ━━━━━━━━━━━━━━━━━━━━━┓
┃ Projects (6)              Sort: [Priority] ▾               ┃
┃                                                             ┃
┃ Project                  Status  Pri  Progress  Due  Upd   ┃
┃ ─────────────────────────────────────────────────────────  ┃
┃ 🚫 Quatrro Corcentric    HOLD   MED  [░░░░] 0%  --   5d    ┃
┃ 📌 California Move       ACTV   HIGH [█░░░] 5%  Jun30 3d   ┃
┃    Transcendant Brands   ACTV   HIGH [███░] 35% Feb15 1d   ┃
┃                                                             ┃
┃ ⚠ Attention Needed                                          ┃
┃ 🚫 BLOCKED (1): Quatrro Corcentric AP                      ┃
┃ 📅 STALE (2): The One Group (8d), UNO Restaurants (8d)     ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
 [↑↓] Navigate  [s] Sort  [r] Refresh  [q] Quit
```

## Integration with Other Skills

**Complementary to `/status`**:
- `/status` generates Markdown reports (exportable, scriptable)
- Mission Control provides interactive visual dashboard (daily use)
- Both read same PROJECT.md files, no conflicts

**Data Source**:
- Same YAML frontmatter schema as other skills
- Compatible with `/update-project`, `/new-project`, `/hubspot-sync`
- Changes made by other skills immediately visible on refresh

## Future Phases

**Phase 2** (Attention Features):
- Blocker board view (press 'b')
- Detailed blocker information
- Quick unblock action

**Phase 3** (Quick Updates):
- Update panel (press 'u')
- Edit status, priority, progress, dates
- Direct YAML write-back

**Phase 4** (HubSpot Integration):
- HubSpot sync manager (press 'h')
- Bulk sync multiple projects
- Show last sync dates

**Phase 5** (Polish):
- Filtering by status/category/priority
- Search/fuzzy find by name
- Help screen (press '?')
- Configurable thresholds (stale days, etc.)

## Technical Implementation

**Architecture**:
- Pure Python stdlib (no external dependencies)
- Curses-based TUI (terminal-native)
- Zero-dependency YAML parser (regex-based)
- Cached computed properties for performance

**Files**:
```
~/.claude/skills/mission-control/
├── mc                # Executable launcher
├── SKILL.md         # This file
├── README.md        # User documentation
└── src/
    ├── main.py      # Event loop & controller
    ├── models.py    # Project dataclass with computed properties
    ├── loader.py    # PROJECT.md discovery & parsing
    ├── views/
    │   └── dashboard.py  # Curses UI rendering
    └── utils/
        └── date_utils.py # Date formatting helpers
```

## Requirements

- Python 3.6+
- Terminal with color support
- Minimum terminal size: 80x24

## Installation

Already installed at:
```
~/.claude/skills/mission-control/
```

Optional - create symlink for easy access:
```bash
ln -s ~/.claude/skills/mission-control/mc /usr/local/bin/mc
```

## Version

v0.1.0 - Phase 1 MVP Complete

## Notes

- Terminal size too small? Dashboard will show error
- Malformed PROJECT.md? Skips that project, shows warning
- No projects found? Shows empty state message
- File changes not appearing? Press 'r' to refresh

---

**Mission Control**: Your daily command center for project visibility and action.
