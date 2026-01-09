# Mission Control - Project Dashboard

A fast, terminal-based dashboard for managing all your projects in the `~/projects` system.

## Features

✅ **Three-Pane Interface**: Projects | Summary | Tasks view
✅ **Scrollable Project History**: View recent decisions and updates with keyboard controls
✅ **Flicker-Free Rendering**: Optimized display updates only when needed
✅ **Color-Coded Status**: Visual indicators for project health
✅ **Task Management**: View, toggle completion, delete, and undo tasks
✅ **Multiple Sort Options**: Priority, category, due date, last updated, name, risk
✅ **Import Processing**: AI-powered file analysis and routing
✅ **Import Review Workflow**: Stage and review AI analyses before applying
✅ **Auto-Import Monitoring**: Continuous watching with periodic checks
✅ **Keyboard Navigation**: Full keyboard control, mouse disabled for reliability

## Quick Start

### 🚀 Double-Click Launch (macOS)

The easiest way to use Mission Control:

1. Open **Finder** and navigate to `~/projects/mission-control/`
2. Double-click one of these launchers:
   - **Mission Control.command** - Main dashboard (includes import processing via `[i]` key)
   - **Watch Imports.command** - Continuous import monitor

Each launcher opens a new Terminal window and runs the application.

### ⌨️ Command Line Launch

```bash
# Main dashboard (includes import processing via [i] key)
~/projects/mission-control/mc

# Watch for imports continuously
~/projects/mission-control/watch-imports
```

## Main Dashboard (mc)

### Interface Layout

```
┌─────────────────────────────┬─────────────────────────────┐
│         PROJECTS            │      PROJECT SUMMARY        │
│  [List of all projects]     │  [Selected project details] │
│  - Status, priority, prog.  │  - Scrollable decisions     │
│                             │  - Scrollable updates       │
│                             │  - Progress, dates          │
├─────────────────────────────┴─────────────────────────────┤
│                         TASKS                             │
│  [Tasks for selected project]                             │
│  - Toggle completion, delete, undo                        │
└───────────────────────────────────────────────────────────┘
```

### Keyboard Commands

#### Navigation
- **↑/↓** or **k/j**: Navigate active pane (projects or tasks)
- **Tab**: Switch between Projects pane and Tasks pane
- **Home/End**: Jump to first/last item in active pane

#### Projects Pane
- **s**: Cycle sort order (priority → category → due date → last updated → name → risk)
- **[** or **PgUp**: Scroll project summary up
- **]** or **PgDn**: Scroll project summary down

#### Tasks Pane
- **Space**: Toggle task completion
- **d**: Delete selected task
- **u**: Undo last deletion

#### General
- **i**: Open import review workflow (if pending analyses exist) or import processor
- **r**: Refresh all project data from disk
- **q**: Quit

### Project Summary Scrolling

The project summary pane (upper-right) displays:
- Project metadata (status, priority, progress, dates)
- **Recent Decisions**: Entries from PROJECT.md Recent Updates without emojis
- **Recent Updates**: Entries from PROJECT.md Recent Updates with emojis (✓, ⚠️, •)

Use **[** and **]** keys to scroll through decisions and updates when there's more content than fits on screen. Scroll indicators (↑↑, ↓↓) appear when content extends beyond visible area.

### Color Coding

- 🟢 **Green**: Active projects, todo tasks
- 🟡 **Yellow**: On-hold projects, in-progress tasks
- 🔴 **Red**: Blocked or overdue projects, urgent tasks
- 🔵 **Blue**: Completed projects and tasks
- ⚪ **Gray**: Stale projects (7+ days since update)

## Import Processing

### Two Ways to Process Imports

**Method 1: Manual Processing via Main Dashboard**
1. Drop files into `~/projects/import/`
2. Launch Mission Control dashboard
3. Press **[i]** key to open import processor
4. Choose processing mode:
   - **AI Analysis**: Uses Claude to analyze content and route to projects
   - **Manual Routing**: Select destination project manually
5. Review and confirm routing
6. Files are analyzed and staged for review
7. Press **[i]** again to review and approve staged analyses

**Method 2: Automatic Continuous Processing**
Launch Watch Imports for hands-free monitoring (see below)

**Supported Files:**
- Images (PNG, JPG, HEIC, etc.)
- PDFs
- Text files (TXT, MD)
- Documents (DOCX)
- Meeting transcripts

### Watch Imports

Continuous monitoring mode that auto-processes files:

**Features:**
- Checks `~/projects/import/` every 10 seconds
- Auto-processes with AI when files detected
- Shows real-time progress and status
- Displays recent import results
- Keyboard controls:
  - **q**: Quit
  - **r**: Force immediate check
  - **c**: Clear results display

## Import Review Workflow

After files are processed (via manual import `[i]` key or Watch Imports), they're staged for review in the main dashboard:

1. Launch main dashboard (`mc`)
2. Press **[i]** to open import review (if analyses are pending)
3. Review each analysis:
   - See extracted content and AI reasoning
   - Choose to **Approve** or **Reject**
4. After reviewing all items, apply approved changes
5. Tasks, decisions, and updates are added to project files
6. Original files are archived to `.import-archive/`

**Note**: If no pending analyses exist, pressing `[i]` opens the import processor instead.

## Technical Details

### Architecture

```
~/projects/
├── mission-control/           # This application
│   ├── mc                     # Main dashboard (includes import via [i] key)
│   ├── process-imports        # Import processor (accessed via mc → [i])
│   ├── watch-imports          # Continuous import watcher
│   ├── Mission Control.command     # Double-click launcher for dashboard
│   ├── Watch Imports.command       # Double-click launcher for watcher
│   └── src/
│       ├── main.py            # Dashboard entry point
│       ├── models.py          # Project dataclass
│       ├── loader.py          # PROJECT.md parser
│       ├── import_processor.py     # Import AI logic
│       ├── content_analyzer.py     # Content extraction
│       ├── content_router.py       # AI routing
│       ├── staging.py         # Review workflow
│       ├── task_parser.py     # Task parsing
│       ├── views/             # UI components
│       │   ├── dashboard.py        # Grid view
│       │   ├── three_pane_view.py  # Main 3-pane layout
│       │   ├── imports_view.py     # Import modal
│       │   └── review_view.py      # Review modal
│       └── utils/
│           └── date_utils.py       # Date helpers
├── import/                    # Drop files here to import
├── .import-archive/           # Processed files moved here
└── .mission-control/          # Application data
    └── staging/               # Pending analyses
```

### Performance Optimizations

- **Render-on-change**: Screen only updates when state changes (eliminates flicker)
- **Mouse events disabled**: Prevents display corruption from scroll events
- **Virtual scrolling**: Only renders visible items in long lists
- **Cached properties**: Risk scores and computed values cached
- **Simple YAML parser**: Regex-based parsing for PROJECT.md (no PyYAML dependency)

### Project Discovery

Automatically discovers all PROJECT.md files under `~/projects/` excluding:
- `.templates`
- `_archived`
- `.git`
- `.agents`
- `.docs`

## Dependencies

- **Python 3.9+**
- **Standard library only** for dashboard (curses, pathlib, re, datetime)
- **Anthropic SDK** for import processing (AI analysis)

## Environment Variables

Set these for import processing functionality:

```bash
# Required for AI-powered import processing
export ANTHROPIC_API_KEY="your-api-key"
```

Add to your shell profile (~/.zshrc or ~/.bashrc):
```bash
echo 'export ANTHROPIC_API_KEY="your-key"' >> ~/.zshrc
source ~/.zshrc
```

## Troubleshooting

### Display Issues
- If display corrupts, quit (q) and restart
- Ensure terminal is at least 80x24 characters
- Disable mouse events in terminal preferences if problems persist

### Import Processing Issues
- Verify ANTHROPIC_API_KEY is set: `echo $ANTHROPIC_API_KEY`
- Check files are in `~/projects/import/`
- Review logs in staging directory: `~/.mission-control/staging/`

### Files Not Appearing
- Run refresh (r) to reload from disk
- Verify PROJECT.md has valid YAML frontmatter
- Check file permissions

## Version History

**v1.0** (January 2026)
- Three-pane interface with scrollable decisions/updates
- Flicker-free rendering with render-on-change pattern
- Enhanced import processing with AI routing
- Review workflow with staging
- Double-click launchers for macOS
- Mouse events disabled for reliability

**v0.1** (Initial Release)
- Basic dashboard with project grid
- Simple keyboard navigation
- Color-coded status

## Support

Part of the `~/projects` system. See the main [projects README](../README.md) for complete documentation.

For issues or feature requests, use Claude Code or modify this file.
