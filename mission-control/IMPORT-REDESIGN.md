# Import Workflow Redesign

**Date**: 2026-01-09
**Status**: Planning
**Priority**: High

---

## Current Problems

### 1. **Too Much Friction**
The current workflow has two manual gates:
```
Drop file → Watch Imports auto-processes → Press [i] → Review each file → Approve/Reject → Content applied
```

**Issues**:
- User must remember to press `[i]` to review
- Each file requires manual approval
- Creates backlog of pending analyses
- Interrupts workflow to review content

### 2. **Confusing State Management**
Files exist in three states:
- Unprocessed (in `import/`)
- Staged for review (in `.mission-control/staging/`)
- Applied (archived to `.import-archive/`)

**Users don't understand**:
- Why files aren't automatically applied
- What "staged for review" means
- How to check if import worked

### 3. **No Post-Import Correction**
Once content is added:
- Can't move tasks between projects
- Can't reassign incorrectly routed content
- Must manually edit files to fix AI mistakes

---

## New Paradigm: Trust First, Fix Later

### Core Philosophy
**"AI makes decisions automatically, users fix mistakes after the fact"**

Like email spam filters:
- Most emails correctly sorted automatically
- You can move incorrectly filtered emails
- System learns from corrections (future enhancement)

---

## Proposed New Workflow

### 1. **Fully Automatic Import** (No Review Gate)

```
Drop file → Watch Imports detects → AI analyzes & routes → Content applied immediately → Notification shown
```

**Benefits**:
- Zero friction - just drop and forget
- No manual review step
- No pending queue to manage
- Instant feedback on what happened

**Notification Example**:
```
✓ Imported meeting-notes.txt
  → Added 3 tasks to quatrro-transcendant-brands
  → Added 1 decision to quatrro-transcendant-brands
  [u] Undo   [v] View changes
```

### 2. **Undo/Rollback for Mistakes**

Add `[u]` key in dashboard:
```
Recent Imports:
- 2 min ago: meeting-notes.txt → quatrro-transcendant-brands [u] Undo
- 5 min ago: screenshot.png → quattro-poke-house [u] Undo
```

**How it works**:
- Keep rollback data for last 10 imports
- Pressing `[u]` removes added tasks/decisions/updates
- Restores original file to import directory
- User can re-import to different project

### 3. **Task Management Features**

Add `[m]` key to move/reassign tasks:
```
Press [m] on a task:
┌─────────────────────────────────────┐
│  Move Task To...                    │
│  ─────────────────────────────────  │
│  [1] quatrro-transcendant-brands    │
│  [2] quattro-poke-house             │
│  [3] quatrro-the-one-group          │
│  [4] (Create new project)           │
│  [ESC] Cancel                       │
└─────────────────────────────────────┘
```

**Also supports**:
- Bulk move: Select multiple tasks, press `[m]`
- Quick reassign between related projects
- Copy task to multiple projects

### 4. **Create Project Modal**

Add `[n]` key for new project:
```
Press [n] anywhere in dashboard:
┌─────────────────────────────────────┐
│  Create New Project                 │
│  ─────────────────────────────────  │
│  Title: [________________]          │
│  Category: [Work ▼]                 │
│  Container: [client-projects ▼]     │
│  Priority: [High ▼]                 │
│  Owner: [Jason Pace]                │
│                                     │
│  [Create]  [Cancel]                 │
└─────────────────────────────────────┘
```

**Auto-scaffolds**:
- PROJECT.md with YAML frontmatter
- tasks.md, timeline.md
- meeting-notes/ folder (if work project)
- Immediately available in dashboard

---

## Implementation Plan

### Phase 1: Remove Review Gate (Quick Win)

**Changes needed**:
1. **Disable staging system** - Apply imports immediately
2. **Remove `[i]` review workflow** - Delete review_view.py
3. **Keep import tracking** - Store what was imported and where
4. **Add notification** - Show brief success message after import

**Files to modify**:
- `src/import_processor.py` - Remove staging, apply directly
- `src/main.py` - Remove `[i]` key handler and review modal
- `src/content_router.py` - Apply changes immediately

**Estimated effort**: 2-3 hours

### Phase 2: Undo/Rollback System

**New functionality**:
1. **Import history tracking** - Store last 10 imports with rollback data
2. **Undo command** - `[u]` key shows recent imports
3. **Rollback logic** - Remove added content, restore file

**New files**:
- `src/import_history.py` - Track imports and rollback data
- `src/views/import_history_view.py` - Show recent imports

**Estimated effort**: 4-5 hours

### Phase 3: Task Move/Reassign

**New functionality**:
1. **Task selection** - Mark tasks for moving
2. **Project picker** - Choose destination project
3. **Move logic** - Remove from source, add to destination

**New files**:
- `src/task_manager.py` - Move/copy task operations
- `src/views/task_move_view.py` - Project selection modal

**Estimated effort**: 6-8 hours

### Phase 4: Create Project Modal

**New functionality**:
1. **Project creation form** - Inline in dashboard
2. **Template scaffolding** - Auto-create structure
3. **Immediate refresh** - New project appears instantly

**New files**:
- `src/project_creator.py` - Project scaffolding logic
- `src/views/project_create_view.py` - Creation modal

**Estimated effort**: 4-6 hours

---

## Keyboard Shortcuts (New)

| Key | Action | Description |
|-----|--------|-------------|
| `u` | Undo import | View and undo recent imports |
| `m` | Move task | Move selected task to another project |
| `n` | New project | Create new project from dashboard |
| `i` | Inbox | View unmatched items needing routing |
| ~~`i`~~ | ~~Review imports~~ | **REPURPOSED** - now opens inbox instead of staging review |

---

## Phase 5: Scrolling Marquee (Visual Enhancement)

### Bottom Line News Ticker

Add a single-line scrolling marquee at the very bottom showing recent project updates:

```
┌────────────────────────────────────────────────────────────────┐
│ Projects     │ Summary          │ [Keyboard shortcuts]          │
│              │                  │                               │
├──────────────┴──────────────────┴───────────────────────────────┤
│ Tasks                                                            │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│ ← Transcendent: Service credit approved • Poke House: Weekly... │
└──────────────────────────────────────────────────────────────────┘
```

**Features**:
- Scrolls continuously from right to left
- Shows recent updates from all projects
- Format: `[Project]: Update text  •  [Project]: Update text  •  ...`
- Loops seamlessly when reaching the end
- Updates every 30 seconds with fresh project data
- Color-coded: Project names in one color, updates in another

**Implementation**:
- New file: `src/views/marquee.py`
- Collect `recent_updates` from all loaded projects
- Animate scroll position (increment every 100-200ms)
- Use modulo arithmetic to loop text seamlessly
- Render at `height - 1` (bottom line)

**Estimated effort**: 2-3 hours

---

## Data Structures

### Import History Entry
```json
{
  "timestamp": "2026-01-09T15:30:00",
  "source_file": "meeting-notes.txt",
  "imported_to": [
    {
      "project": "quatrro-transcendant-brands",
      "tasks_added": [
        {"line": 15, "text": "Follow up on lease issue"}
      ],
      "decisions_added": [
        {"line": 42, "date": "2026-01-09", "text": "Approved service credit"}
      ],
      "updates_added": [
        {"line": 48, "date": "2026-01-09", "text": "Meeting completed"}
      ]
    }
  ],
  "can_undo": true,
  "original_file_backup": "/path/to/backup"
}
```

### Rollback Process
1. Read rollback data from history
2. For each project affected:
   - Load PROJECT.md, remove added decisions/updates
   - Load tasks.md, remove added tasks (by line number or text match)
   - Save files
3. Restore original file to import directory
4. Mark history entry as undone

---

## Migration Path

### Step 1: Ship Phase 1 Immediately
- Remove friction, make imports automatic
- Users can manually fix mistakes by editing files

### Step 2: Add Undo (Phase 2)
- Safety net for automatic imports
- Reduces fear of AI mistakes

### Step 3: Add Task Management (Phase 3)
- Fixes the "routed to wrong project" problem
- Enables bulk task operations

### Step 4: Add Project Creation (Phase 4)
- Complete the workflow
- No need to leave dashboard

---

## Success Metrics

**Before** (Current):
- Drop file → 3-5 manual steps → content applied
- ~2 minutes per file
- High cognitive load (review each item)

**After** (New):
- Drop file → 0 manual steps → content applied
- ~5 seconds per file
- Low cognitive load (only fix mistakes)

**Quality metric**:
- If AI routing is >90% accurate, automatic import is better UX
- Undo provides safety net for 10% mistakes

---

## Open Questions

1. **How long to keep import history?**
   - Proposal: 10 most recent imports
   - Store in `.mission-control/import-history.json`

2. **Should undo be permanent or show confirmation?**
   - Proposal: Show confirmation modal with what will be undone

3. **What if user manually edited the imported content?**
   - Proposal: Show warning "Content has changed since import"
   - Allow undo anyway (user can re-import)

4. **Should we keep staging for "low confidence" imports?**
   - Proposal: No, apply everything. Add confidence indicator to notification
   - If confidence <70%, show warning: "⚠️  Low confidence - may need review"

---

## Files to Create

**Phase 1**:
- *(no new files, modify existing)*

**Phase 2**:
- `src/import_history.py` - History tracking and rollback
- `src/views/import_history_view.py` - Show recent imports

**Phase 3**:
- `src/task_manager.py` - Task move/copy operations
- `src/views/task_move_view.py` - Project picker modal

**Phase 4**:
- `src/project_creator.py` - Project scaffolding
- `src/views/project_create_view.py` - Creation form modal

**Phase 5**:
- `src/views/marquee.py` - Scrolling project updates ticker

**Phase 6**:
- `src/usage_tracker.py` - API usage and cost tracking
- `src/views/status_bar.py` - Top status bar renderer

---

## Phase 6: Usage Tracking & Status Bar

### Top Status Bar Display

Add a status bar at the very top showing API usage and costs:

```
┌──────────────────────────────────────────────────────────────────┐
│ Tokens: 1.2M | Today: $2.45 | Week: $15.30 | Month: $47.80      │
├────────────────┬─────────────────────────────────────────────────┤
│ Projects       │ Summary                                          │
│                │                                                  │
```

**Features**:
- Single line at the very top
- Shows aggregated token usage across all API calls
- Cost tracking: daily, weekly (week-to-date), monthly (month-to-date)
- Updates in real-time as API calls are made
- Persisted to disk for cross-session tracking
- Color-coded: Green when under budget, yellow approaching limits, red if exceeded

### Implementation Strategy

**Usage Tracking Data Structure:**

```json
{
  "daily": {
    "2026-01-09": {
      "tokens_used": 125000,
      "cost_usd": 2.45,
      "api_calls": 15,
      "calls": [
        {
          "timestamp": "2026-01-09T10:23:45",
          "operation": "import_analysis",
          "model": "claude-sonnet-4-5",
          "input_tokens": 5000,
          "output_tokens": 3000,
          "cost_usd": 0.16
        }
      ]
    }
  },
  "weekly": {
    "2026-W02": {
      "tokens_used": 1200000,
      "cost_usd": 15.30,
      "api_calls": 87
    }
  },
  "monthly": {
    "2026-01": {
      "tokens_used": 3800000,
      "cost_usd": 47.80,
      "api_calls": 312
    }
  }
}
```

**Storage**: `.mission-control/usage-tracking.json`

**Cost Calculation**:
- Based on Anthropic pricing for Claude models
- Input tokens: $3 per million tokens
- Output tokens: $15 per million tokens
- Configurable in `config.json` for different models

**Tracking Points**:
1. **Import analysis** - When AI analyzes dropped files
2. **Content routing** - When AI decides which project(s) to route to
3. **Task extraction** - When AI extracts tasks/decisions/updates
4. **Project matching** - When AI matches content to projects

**Integration**:
- Wrap all Anthropic API calls in `usage_tracker.track_call()`
- Decorator pattern: `@track_usage` on functions making API calls
- Automatic calculation of costs based on token counts
- Automatic rollup to daily/weekly/monthly aggregates

**New Files**:
- `src/usage_tracker.py` - Core tracking logic:
  - `track_call(operation, model, input_tokens, output_tokens)` - Record API call
  - `get_daily_total()`, `get_weekly_total()`, `get_monthly_total()` - Aggregates
  - `load_usage_data()`, `save_usage_data()` - Persistence
  - `calculate_cost(model, input_tokens, output_tokens)` - Cost calculation

- `src/views/status_bar.py` - Rendering:
  - `render_status_bar(stdscr, y_offset)` - Draw status line
  - `format_tokens(count)` - Format as "1.2M", "450K", etc.
  - `format_cost(amount)` - Format as "$2.45", "$15.30", etc.
  - `get_cost_color(amount, budget)` - Color coding based on budget

**Files to Modify**:
- `src/import_processor.py` - Add `@track_usage` to AI calls
- `src/content_router.py` - Add `@track_usage` to routing logic
- `src/main.py` - Render status bar at top, adjust layout
- `src/views/three_pane_view.py` - Adjust y_offset for status bar

**Estimated effort**: 4-5 hours

---

## Rethinking Unmatched Content

### Current Problem: The "Holding Project" Anti-Pattern

**Current approach (flawed)**:
- Content that AI can't match to a project goes to a "holding project"
- Creates an artificial project that's not really a project
- Confusing: Is it a real project or just a bucket?
- Doesn't fit the mental model

### Proposed Solutions

#### Option A: Inbox Mode (Recommended)

**Concept**: Unmatched content goes to a special "Inbox" view accessible via `[i]` key

```
Press [i] to open Inbox:
┌─────────────────────────────────────────────────────────────────┐
│ Inbox (5 unmatched items)                                       │
├─────────────────────────────────────────────────────────────────┤
│ Tasks:                                                           │
│  [ ] Review quarterly financials                                │
│      Confidence: 45% | Suggested: quatrro-transcendant-brands   │
│      [m] Move to project   [n] Create new project               │
│                                                                  │
│  [ ] Call vendor about invoice                                  │
│      Confidence: 30% | Suggested: (none)                        │
│      [m] Move to project   [n] Create new project               │
│                                                                  │
│ Decisions:                                                       │
│  [ ] Approved budget increase for Q2                            │
│      Confidence: 38% | Suggested: (multiple projects)           │
│      [m] Move to project   [n] Create new project               │
└─────────────────────────────────────────────────────────────────┘
```

**How it works**:
- Unmatched items stored in `.mission-control/inbox/tasks.json`, `decisions.json`, `updates.json`
- Badge on status bar: `Inbox: 5` (red if items present)
- Pressing `[i]` opens inbox view
- Each item shows AI confidence score and suggested project (if any)
- User can:
  - Press `[m]` to move to existing project
  - Press `[n]` to create new project from item
  - Press `[d]` to delete/discard item
- Items automatically removed from inbox when moved
- Inbox persists across sessions

**Benefits**:
- Clear separation: Inbox is NOT a project
- Explicit action required (press `[i]` to review)
- Shows AI confidence/suggestions to guide routing
- Natural workflow: "check inbox, route items, done"

**Data Structure**:
```json
{
  "tasks": [
    {
      "id": "task-20260109-152330-abc123",
      "text": "Review quarterly financials",
      "source_file": "meeting-notes.txt",
      "added_at": "2026-01-09T15:23:30",
      "ai_confidence": 0.45,
      "suggested_project": "quatrro-transcendant-brands",
      "alternate_suggestions": ["quattro-poke-house"],
      "reasoning": "Mentions financials and Q1, common to Transcendant project"
    }
  ],
  "decisions": [],
  "updates": []
}
```

#### Option B: Smart Notification with Quick Route

**Concept**: When import creates unmatched content, show notification with quick routing

```
✓ Imported meeting-notes.txt
  → Added 3 tasks to quatrro-transcendant-brands
  → Added 1 decision to quatrro-transcendant-brands

⚠️  2 items need routing:
  1. Task: "Review quarterly financials" → [Suggested: transcendant-brands]
     Press 1 to accept | Press [m] to choose project | Press [x] to inbox

  2. Task: "Call vendor" → [No suggestion]
     Press [m] to choose project | Press [x] to inbox
```

**How it works**:
- Notification immediately after import
- Shows unmatched items inline
- Quick keys to route instantly (1-9 for suggestions)
- `[m]` opens project picker
- `[x]` sends to inbox for later
- Times out after 10 seconds → items go to inbox automatically

**Benefits**:
- Immediate routing opportunity
- Reduces inbox accumulation
- Fast workflow for obvious matches

#### Option C: Project Suggestion Engine

**Concept**: For low-confidence items, show them IN the suggested project with "?" indicator

```
Quatrro Transcendant Brands

Tasks (5):
✓ Update lease documentation
- Schedule follow-up meeting
? Review quarterly financials  ← Unmatched but suggested here
  [✓] Confirm   [✗] Remove   [m] Move to different project
```

**How it works**:
- AI assigns unmatched items to "best guess" project with confidence score
- Items marked with `?` indicator in tasks pane
- User must explicitly confirm or move
- Stays in suggested project until confirmed/moved
- Prevents items from getting lost

**Benefits**:
- Items appear in context where they might belong
- Reduces separate "inbox" concept
- Encourages confirmation workflow

#### Option D: Discard by Default + Search Archive

**Concept**: Don't keep unmatched items at all - archive them with full-text search

```
Unmatched items discarded to archive:
- 2 tasks archived to .mission-control/archive/unmatched-20260109.json

To recover: Press [s] to search archive
```

**How it works**:
- Low-confidence items automatically archived
- Full-text search available via `[s]` key
- User can search and pull items out if needed
- Assumption: If AI can't match with 50%+ confidence, probably not important

**Benefits**:
- Reduces cognitive load
- Inbox doesn't fill up with noise
- Important items can still be recovered

### Recommendation: **Option A (Inbox Mode)**

**Why Option A is best**:
1. **Clear mental model**: Inbox is separate from projects
2. **Explicit workflow**: User knows where unmatched items go
3. **Visible indicator**: Status bar shows inbox count
4. **Preserves context**: Items stored with source file and AI reasoning
5. **Flexible routing**: User can move to project or create new one
6. **Persistent**: Survives across sessions

**Implementation**:
- Store in `.mission-control/inbox/` directory
- Badge on status bar: `Inbox: 5` (only if items present)
- `[i]` key opens inbox view (reuse `i` key since review workflow deleted)
- Integration with Phase 3 (task move) and Phase 4 (project creation)

**New Files**:
- `src/inbox_manager.py` - Add/remove inbox items
- `src/views/inbox_view.py` - Render inbox modal

**Estimated effort**: 3-4 hours

---

## Files to Delete

- `src/staging.py` - No longer needed
- `src/views/review_view.py` - No longer needed
- `.mission-control/staging/` - No longer needed

---

## Implementation Roadmap

### Phase 1: Remove Review Gate (2-3 hours)
**Priority**: Immediate - Removes core friction
- Automatic import application
- Brief success notifications
- No staging system

### Phase 2: Undo/Rollback (4-5 hours)
**Priority**: High - Safety net for automatic imports
- Last 10 imports tracked
- Full rollback capability
- Restore to import directory

### Phase 3: Task Move/Reassign (6-8 hours)
**Priority**: High - Fix routing mistakes
- Move tasks between projects
- Bulk operations
- Copy to multiple projects

### Phase 4: Create Project Modal (4-6 hours)
**Priority**: Medium - Complete workflow
- Inline project creation
- Auto-scaffolding
- Immediate availability

### Phase 5: Scrolling Marquee (2-3 hours)
**Priority**: Low - Visual enhancement
- Bottom line news ticker
- Continuous right-to-left scroll
- Recent project updates

### Phase 6: Usage Tracking & Status Bar (4-5 hours)
**Priority**: Medium - Visibility and cost awareness
- Top status bar with API usage
- Daily/weekly/monthly cost tracking
- Budget alerts

### Inbox System for Unmatched Content (3-4 hours)
**Priority**: High - Completes import workflow
- Replaces holding project concept
- `[i]` key for inbox view
- AI confidence scores and suggestions

---

## Total Estimated Effort

| Phase | Hours | Priority |
|-------|-------|----------|
| Phase 1: Auto-apply imports | 2-3 | Immediate |
| Phase 2: Undo/rollback | 4-5 | High |
| Phase 3: Task management | 6-8 | High |
| Phase 4: Project creation | 4-6 | Medium |
| Phase 5: Scrolling marquee | 2-3 | Low |
| Phase 6: Status bar | 4-5 | Medium |
| Inbox system | 3-4 | High |
| **Total** | **25-34 hours** | |

---

## Next Steps

1. **Get user approval** on this comprehensive redesign
2. **Implement Phase 1** (automatic imports) - Immediate quick win
3. **Test with real files** - Validate AI routing accuracy
4. **Implement Phase 2** (undo) - Add safety net
5. **Implement Inbox system** - Handle unmatched content properly
6. **Implement Phase 3** (task management) - Enable corrections
7. **Implement remaining phases** based on priority and user feedback

---

**This is a comprehensive redesign that transforms Mission Control from a manual review system to an intelligent, trust-first workflow with proper safety nets and correction mechanisms.**
