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
| ~~`i`~~ | ~~Review imports~~ | **REMOVED** - no longer needed |

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

---

## Files to Delete

- `src/staging.py` - No longer needed
- `src/views/review_view.py` - No longer needed
- `.mission-control/staging/` - No longer needed

---

## Next Steps

1. **Get user approval** on this redesign approach
2. **Implement Phase 1** (remove review gate) - Quick win
3. **Test automatic imports** with real files
4. **Implement Phase 2** (undo) - Safety net
5. **Iterate based on usage**

---

**This is a significant UX improvement that reduces friction and builds trust in the AI routing system.**
