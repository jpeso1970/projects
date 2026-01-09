# Mission Control Improvement Plan

**Analysis Date:** 2026-01-09
**Analyst:** Claude Code
**Status:** In Progress

---

## Executive Summary

The Mission Control system captures rich project data but displays only a fraction of it. This document outlines concrete improvements organized by effort level and category.

---

## Quick Wins (Low Effort, High Impact)

### Presentation
- [x] **Display owner in project list** - Show project owner between name and status columns
- [x] **Show days_until_due in summary** - Color-coded display with urgency indicators
- [x] **Add needs_review emoji indicator** - Shows 👀 for projects needing review
- [x] **Show risk_score as visual indicator** - Shows 🔴🟠🟡🟢 based on score (0-100)
- [x] **Display description in summary pane** - Shows purpose/context with word wrap

### Functionality
- [x] **Fix duplicate updates issue** - Deduplication added to content routing

---

## Medium Effort Improvements

### Presentation
- [x] **Show task assignees in tasks pane** - Added column for assignee in tasks pane
- [ ] **Display tags as badges** - Show project tags in summary pane
- [ ] **Show external_links in summary** - Display clickable links (HubSpot, repository, etc.)
- [ ] **Display stakeholders for work projects** - Show key contacts in summary
- [ ] **Show estimated vs actual hours** - Display time tracking with utilization %

### Functionality
- [x] **Add filtering capability** - Press `f` to cycle: all/active/blocked/work/personal/development/family/high
- [x] **Implement help screen** - Press `?` to show all keybindings in modal
- [ ] **Auto-calculate progress percent** - Compute from tasks_completed/tasks_total
- [ ] **Bound summary scroll offset** - Prevent scrolling past content
- [ ] **Add project quick-open** - `o` key to open project folder in file manager

---

## Larger Improvements

### Architecture
- [ ] **Replace custom YAML parser** - Use pyyaml instead of fragile regex-based parser
- [ ] **Add configuration file** - Move hardcoded settings (timeouts, intervals) to config
- [ ] **Implement proper logging** - Replace print() statements with logging module
- [ ] **Add unit tests** - At minimum for loader.py, task_parser.py, models.py

### Functionality
- [ ] **Auto-sync task metrics** - Update tasks_total/tasks_completed in YAML on task changes
- [ ] **Parse Next Steps section** - Extract and display next steps from PROJECT.md
- [ ] **Parse client info for work projects** - Load deal amount, contacts into model
- [ ] **Add inline task creation** - `a` key to add task from dashboard
- [ ] **HubSpot sync from dashboard** - Trigger refresh from UI

### Data Quality
- [ ] **Validate status values** - Enforce enum (active, on-hold, blocked, completed)
- [ ] **Validate priority values** - Enforce enum (high, medium, low)
- [ ] **Clean template placeholders** - Remove "Item 1", "Risk 1" from real projects

---

## Data Currently Captured But Not Displayed

| Field | Storage Location | Recommended Display | Status |
|-------|------------------|---------------------|--------|
| `owner` | PROJECT.md YAML | Project list + Summary | ✅ Done |
| `collaborators` | PROJECT.md YAML | Summary pane | Pending |
| `stakeholders` | PROJECT.md YAML | Summary pane | Pending |
| `estimated_hours` | PROJECT.md YAML | Summary with utilization | Pending |
| `actual_hours` | PROJECT.md YAML | Summary with utilization | Pending |
| `tags` | PROJECT.md YAML | Summary as badges | Pending |
| `description` | Extracted from Overview | Summary pane | ✅ Done |
| `related_projects` | PROJECT.md YAML | Summary with navigation | Pending |
| `external_links` | PROJECT.md YAML | Summary (clickable) | Pending |
| `repository` | PROJECT.md YAML | Summary pane | Pending |
| `hubspot_company_id` | PROJECT.md YAML | Summary (HubSpot badge) | Pending |
| `hubspot_deal_id` | PROJECT.md YAML | Summary (HubSpot badge) | Pending |
| `needs_review` | PROJECT.md YAML | Project list emoji | ✅ Done |
| `days_since_update` | Computed property | Project list column | Pending |
| `days_until_due` | Computed property | Summary prominently | ✅ Done |
| `risk_score` | Computed property | Project list + Summary | ✅ Done |
| `task.assignee` | tasks.md | Tasks pane column | ✅ Done |

---

## Code Quality Issues to Address

### Architecture Problems
| Issue | Location | Description |
|-------|----------|-------------|
| Custom YAML parser fragile | `loader.py:165-229` | Regex-based, breaks on complex YAML |
| Import inside function | `main.py:229` | `import re` should be at top |
| Silent exception swallowing | `main.py:110-112` | Auto-import errors caught with bare `pass` |
| Magic numbers | `main.py:66` | Hardcoded 30s, 100ms timeouts |
| Cached properties on mutable data | `models.py:55-114` | Won't update if data changes |

### Code Duplication
| Location | Issue |
|----------|-------|
| `main.py` (5 places) | Same 3-line task reload pattern |
| `three_pane_view.py` + `dashboard.py` | Similar project row rendering |
| `models.py:126-143` | Three similar `*_display` methods |

---

## Priority Order for Implementation

1. **Display days_until_due prominently** - Critical for deadline awareness
2. **Add needs_review indicator** - Already tracked, easy win
3. **Show risk_score visually** - Computed, high value
4. **Add filtering capability** - Essential for 15+ projects
5. **Fix duplicate content issue** - Data quality
6. **Implement help screen** - Usability
7. **Auto-sync task metrics** - Data accuracy
8. **Replace YAML parser** - Reliability

---

## Files to Modify

| Improvement | Primary File(s) |
|-------------|-----------------|
| Display improvements | `views/three_pane_view.py` |
| Filtering | `main.py`, `loader.py` |
| Help screen | `main.py`, new `views/help_view.py` |
| Task sync | `task_parser.py`, `loader.py` |
| YAML parser | `loader.py` |
| Deduplication | `content_router.py` |

---

## Progress Log

| Date | Item | Status |
|------|------|--------|
| 2026-01-09 | Display owner in project list | Completed |
| 2026-01-09 | Show days_until_due in summary (color-coded) | Completed |
| 2026-01-09 | Add needs_review emoji indicator (👀) | Completed |
| 2026-01-09 | Show risk_score visual indicator (🔴🟠🟡🟢) | Completed |
| 2026-01-09 | Display description in summary pane | Completed |
| 2026-01-09 | Fix duplicate updates (deduplication) | Completed |
| 2026-01-09 | Add filtering capability (f key) | Completed |
| 2026-01-09 | Implement help screen (? key) | Completed |
| 2026-01-09 | Show task assignees in tasks pane | Completed |

---

*This document will be updated as improvements are implemented.*
