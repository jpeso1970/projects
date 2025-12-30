# Common Workflows Guide

Step-by-step workflows for common project management tasks.

---

## Table of Contents

1. [Starting a New Client Project](#workflow-1-starting-a-new-client-project)
2. [Weekly Project Review](#workflow-2-weekly-project-review)
3. [Completing and Archiving a Project](#workflow-3-completing-and-archiving-a-project)
4. [Renaming a Project](#workflow-4-renaming-a-project)
5. [Re-syncing HubSpot Data](#workflow-5-re-syncing-hubspot-data)
6. [Session Management](#workflow-6-session-management)
7. [Monthly Status Report](#workflow-7-monthly-status-report)
8. [Handling Project Blockers](#workflow-8-handling-project-blockers)

---

## Workflow 1: Starting a New Client Project

**Goal**: Set up a complete client project with HubSpot integration

**Prerequisites**:
- HubSpot API key configured
- Client company exists in HubSpot
- Know the project category and container

### Steps

#### 1. Create the Project Structure

```bash
# Navigate to projects directory
cd ~/projects

# Create project using skill
/new-project
```

**Skill will prompt for:**
- Category: `work`
- Container: `client-projects`
- Project name: `acme-website-redesign`
- Title: `Acme Corporation Website Redesign`
- Priority: `high`
- Due date: `2025-03-31`
- Tags: `client`, `website`, `design`
- Description: Brief project purpose

**Result**: Complete project structure created at:
```
~/projects/work/client-projects/acme-website-redesign/
```

#### 2. Navigate to Project

```bash
cd ~/projects/work/client-projects/acme-website-redesign
```

#### 3. Sync HubSpot Data

```bash
/hubspot-sync company='Acme Corporation'
```

**Skill will:**
- Search for company in HubSpot
- Prompt to select correct company if multiple matches
- Fetch company details, deals, contacts
- Prompt to select primary deal if multiple deals
- Update PROJECT.md with client info
- Populate ENTITIES.md with contacts
- Import recent meeting notes
- Download attachments

**Review synced data:**
```bash
cat PROJECT.md       # Check client info section
cat ENTITIES.md      # Verify contacts
ls meeting-notes/    # Check imported meetings
ls assets/hubspot-files/  # Check downloaded files
```

#### 4. Customize Project Details

Edit PROJECT.md to add project-specific information:

```bash
# Use your preferred editor
vim PROJECT.md
# or
code PROJECT.md
```

**Add:**
- Specific project goals and success criteria
- Scope (what's in/out)
- Timeline phases
- Known constraints
- Identified risks

#### 5. Set Up Initial Tasks

Edit tasks.md:

```bash
vim tasks.md
```

**Add initial tasks:**
```markdown
### High Priority
- [ ] Schedule project kickoff meeting
  - Due: Within 1 week
  - Assignee: You

- [ ] Gather detailed requirements
  - Due: 2025-02-15
  - Assignee: You

- [ ] Create project timeline
  - Due: 2025-02-20
  - Assignee: You
```

#### 6. Define Timeline

Edit timeline.md with realistic phases and milestones:

```bash
vim timeline.md
```

#### 7. Commit to Git

```bash
# Navigate to projects root
cd ~/projects

# Check git status
git status

# Add new project
git add work/client-projects/acme-website-redesign

# Commit with descriptive message
git commit -m "$(cat <<'EOF'
Add Acme Corporation website redesign project

- Created project structure with /new-project skill
- Synced HubSpot data (Company ID: 123456789, Deal: $125K)
- Added 5 key stakeholders to ENTITIES.md
- Imported 3 recent meeting notes
- Set up initial task list and timeline
- Priority: HIGH, Due: 2025-03-31

🤖 Generated with Claude Code

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"

# Push if using remote repository
git push
```

#### 8. Schedule Kickoff Meeting

- Send calendar invite to stakeholders
- Prepare agenda
- Share PROJECT.md overview

#### 9. Save Session State

```bash
/save-session-state
```

### Checklist

- [ ] Project created with /new-project
- [ ] Navigated to project directory
- [ ] HubSpot data synced
- [ ] PROJECT.md customized with goals and scope
- [ ] Initial tasks added to tasks.md
- [ ] Timeline defined in timeline.md
- [ ] Changes committed to Git
- [ ] Kickoff meeting scheduled
- [ ] Session state saved

### Expected Time

**Total**: 30-45 minutes

---

## Workflow 2: Weekly Project Review

**Goal**: Review all active projects and update status

**Frequency**: Every Monday morning or Friday afternoon

**Prerequisites**:
- Active projects exist
- Have 15-30 minutes available

### Steps

#### 1. Generate Status Report

```bash
cd ~/projects

# Get overall status
/status

# Or filter by category
/status category=work
```

**Review output for:**
- Overdue projects
- Stale projects (not updated in > 7 days)
- Blocked projects
- Projects nearing deadlines

#### 2. Review Each Active Project

For each project in the status report:

```bash
cd ~/projects/work/client-projects/project-name
```

##### Update tasks.md

```bash
vim tasks.md
```

**Actions:**
- Mark completed tasks with `[✓]`
- Update in-progress tasks with `[→]`
- Add any new tasks discovered
- Flag blocked tasks with `[!]`
- Update task notes

##### Update PROJECT.md

```bash
vim PROJECT.md
```

**Update:**
```yaml
last_updated: 2025-01-27  # Today's date
progress_percent: 35       # Revised estimate
actual_hours: 25           # Time spent this week
```

**Update markdown sections:**
```markdown
### Recent Updates
- 2025-01-27: Completed design mockups, started development

### Next Steps
1. Implement homepage layout
2. Schedule design review meeting
3. Prepare demo for client
```

##### Check Timeline

```bash
vim timeline.md
```

**Review:**
- Are milestones on track?
- Do any phases need adjustment?
- Update phase progress percentages
- Mark completed milestones

##### Identify Blockers

If blocked:

```yaml
blocked: true
needs_review: true
```

**Document blocker in:**
- tasks.md (blocked tasks section)
- PROJECT.md (constraints or risks)
- Create action item to resolve

#### 3. Update Category README

```bash
cd ~/projects/work

vim README.md
```

**Update:**
- Move completed projects to completed section
- Update project descriptions if scope changed
- Adjust priorities if needed

#### 4. Commit Changes

```bash
cd ~/projects

git add -A

git commit -m "$(cat <<'EOF'
Weekly project review - Week of 2025-01-27

Updated status across all active work projects:
- Project A: 35% complete, on track
- Project B: Blocked waiting on client approval
- Project C: 60% complete, ahead of schedule

🤖 Generated with Claude Code

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

#### 5. Plan Next Week

Based on review:
- Prioritize tasks for upcoming week
- Schedule any needed meetings
- Allocate time for blocked projects when unblocked
- Communicate updates to stakeholders

#### 6. Save Session

```bash
/save-session-state
```

### Checklist

- [ ] Generated status report
- [ ] Reviewed all active projects
- [ ] Updated tasks.md for each project
- [ ] Updated PROJECT.md status and progress
- [ ] Checked timelines for accuracy
- [ ] Identified and documented blockers
- [ ] Updated category READMEs
- [ ] Committed changes to Git
- [ ] Planned next week's priorities
- [ ] Saved session state

### Expected Time

**Total**: 15-30 minutes (depending on number of active projects)

---

## Workflow 3: Completing and Archiving a Project

**Goal**: Properly close out and archive a completed project

**Prerequisites**:
- Project is actually complete
- All deliverables shipped
- Retrospective can be conducted

### Steps

#### 1. Final Task Review

```bash
cd ~/projects/work/client-projects/completed-project

vim tasks.md
```

**Ensure:**
- All tasks marked complete `[✓]`
- No outstanding action items
- All blockers resolved or cancelled

#### 2. Update PROJECT.md

```bash
vim PROJECT.md
```

**Update YAML frontmatter:**
```yaml
status: "completed"
priority: "medium"  # Lower priority since done
completed: 2025-01-31
last_updated: 2025-01-31
progress_percent: 100
tasks_completed: 15  # Should equal tasks_total
```

**Fill in Retrospective Section:**
```markdown
## Retrospective

### What Went Well
- Design process was smooth and efficient
- Client communication was excellent
- Delivered 2 weeks early
- No major blockers encountered

### What Could Be Improved
- Initial estimation was off by 20%
- Should have involved backend team earlier
- More frequent testing would have caught bugs sooner

### Lessons Learned
- Always include buffer time for client feedback
- Weekly check-ins prevent scope creep
- Early technical validation saves time later
- Document decisions immediately, not later

### Key Metrics
- **Estimated Time**: 40 hours
- **Actual Time**: 35 hours
- **Budget**: $125,000
- **Client Satisfaction**: 9/10
- **Quality Score**: 8/10
```

#### 3. Final Timeline Update

```bash
vim timeline.md
```

**Mark all milestones complete:**
```markdown
| Project Complete | 2025-01-31 | 2025-01-31 | ✓ Complete | Delivered ahead of schedule |
```

#### 4. Clean Up Files

```bash
# Remove temporary files
rm -f *.tmp
rm -f ~*

# Organize assets
cd assets
# Move final deliverables to clear location
mkdir -p final-deliverables
mv important-file.pdf final-deliverables/

# Return to project root
cd ..
```

#### 5. Export Final Report (Optional)

Create a summary document:

```bash
vim docs/project-completion-report.md
```

**Include:**
- Project overview
- Final outcomes
- Key deliverables
- Metrics and statistics
- Client feedback
- Lessons learned

#### 6. Update Category README

```bash
cd ~/projects/work

vim README.md
```

**Move project from Active to Completed:**

```markdown
## Completed Projects

- [completed-project](./client-projects/completed-project/) - Website redesign for Acme Corp ✓ Completed 2025-01-31 (Budget: $125K)
```

#### 7. Commit Final Changes

```bash
cd ~/projects

git add -A

git commit -m "$(cat <<'EOF'
Mark Acme website project as completed

Project successfully delivered on 2025-01-31, ahead of schedule.

Outcomes:
- Delivered full website redesign
- Client satisfaction: 9/10
- Completed in 35 hours (vs 40 estimated)
- All success criteria met

Lessons learned documented in retrospective section.

🤖 Generated with Claude Code

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

#### 8. Archive Project (Optional)

If you want to move to archive folder:

```bash
cd ~/projects/work/client-projects

# Create _archived folder if doesn't exist
mkdir -p _archived

# Move project
mv completed-project _archived/

# Or use Git to track the move
git mv completed-project _archived/completed-project
git commit -m "Archive completed Acme project"
```

**Note**: Only archive if `auto_archive_on_complete: true` in PROJECT.md

#### 9. Celebrate! 🎉

- Acknowledge the completion
- Share success with team
- Update portfolio if relevant
- Request testimonial from client (if applicable)

### Checklist

- [ ] All tasks marked complete
- [ ] PROJECT.md status set to "completed"
- [ ] Completion date set
- [ ] Retrospective filled out
- [ ] Timeline finalized
- [ ] Files cleaned up
- [ ] Final report created (optional)
- [ ] Category README updated
- [ ] Changes committed to Git
- [ ] Project archived (if desired)
- [ ] Success celebrated

### Expected Time

**Total**: 30-60 minutes

---

## Workflow 4: Renaming a Project

**Goal**: Rename a project and propagate changes everywhere

**Prerequisites**:
- rename-project skill installed
- Project exists and is not currently in use by other processes
- Have a clear reason for renaming (typo, scope change, naming convention)

### Steps

#### 1. Navigate to Project

```bash
cd ~/projects/work/client-projects/old-project-name
```

#### 2. Review Current Name

Check where the old name appears:

```bash
# Check PROJECT.md
grep -n "old-project-name" PROJECT.md

# Check tasks.md
grep -n "Old Project Name" tasks.md

# Check timeline.md
grep -n "Old Project Name" timeline.md
```

#### 3. Run Rename Skill

```bash
/rename-project new-name='new-project-name'
```

**Skill will:**
1. Initialize logging (creates `~/.claude/logs/rename-project/TIMESTAMP-old-name-rename.log`)
2. Create full backup (to `~/.claude/backups/rename-project/TIMESTAMP-old-name-backup/`)
3. Document current state
4. Confirm all changes with you
5. Perform rename operations:
   - Rename directory
   - Update PROJECT.md title (YAML and heading)
   - Update tasks.md heading
   - Update timeline.md heading
   - Update ENTITIES.md heading (if exists)
   - Update category README references
   - Update related_projects in other projects
6. Verify all changes
7. Create summary report

#### 4. Review Changes

```bash
# Check new directory
ls -la ~/projects/work/client-projects/new-project-name

# Verify PROJECT.md
cat PROJECT.md | grep "title:"
cat PROJECT.md | grep "^# "

# Verify tasks.md
head -1 tasks.md

# Verify timeline.md
head -1 timeline.md
```

#### 5. Test Project Files

```bash
# Read PROJECT.md fully
cat PROJECT.md

# Check for any lingering old names
cd ~/projects/work/client-projects/new-project-name
grep -r "old-project-name" .
```

#### 6. Review Log

```bash
# Check the rename log
cat ~/.claude/logs/rename-project/TIMESTAMP-old-project-name-rename.log
```

**Look for:**
- All SUCCESS messages
- No ERROR messages
- Complete list of changes

#### 7. Commit Changes

```bash
cd ~/projects

git add -A

git commit -m "$(cat <<'EOF'
Rename project: old-project-name → new-project-name

Reason: [Explain why you renamed]

Changes made by /rename-project skill:
- Renamed project directory
- Updated PROJECT.md title (YAML + heading)
- Updated tasks.md heading
- Updated timeline.md heading
- Updated ENTITIES.md heading
- Updated work/README.md references
- Verified no broken references

Backup created at: ~/.claude/backups/rename-project/TIMESTAMP-old-project-name-backup/
Log available at: ~/.claude/logs/rename-project/TIMESTAMP-old-project-name-rename.log

🤖 Generated with Claude Code

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

#### 8. Update External References (Manual)

If project is referenced externally:
- Update links in documentation
- Notify team members of new name
- Update any external tracking systems
- Update bookmarks/shortcuts

### Rollback (If Needed)

If something went wrong:

```bash
# Read the backup info
cat ~/.claude/backups/rename-project/TIMESTAMP-old-name-backup/BACKUP_INFO.json

# Follow rollback instructions in rename-project skill
# Or manually restore from backup
cd ~/projects/work/client-projects
rm -rf new-project-name  # Remove failed rename
cp -R ~/.claude/backups/rename-project/TIMESTAMP-old-name-backup/old-project-name .
```

### Checklist

- [ ] Navigated to project directory
- [ ] Reviewed current name usage
- [ ] Ran /rename-project skill
- [ ] Reviewed all changes made
- [ ] Verified PROJECT.md, tasks.md, timeline.md
- [ ] Searched for lingering old names
- [ ] Reviewed rename log
- [ ] Committed changes to Git
- [ ] Updated external references (if any)
- [ ] Notified team members (if applicable)

### Expected Time

**Total**: 10-20 minutes (automated by skill)

---

## Workflow 5: Re-syncing HubSpot Data

**Goal**: Update project with latest data from HubSpot

**When to Use**:
- Monthly data refresh
- After significant HubSpot updates
- New contacts added to company
- New meetings logged in HubSpot

### Steps

#### 1. Navigate to Project

```bash
cd ~/projects/work/client-projects/client-project
```

#### 2. Backup Current Data (Optional)

```bash
# Create manual backup if concerned about overwrites
cp PROJECT.md PROJECT.md.backup
cp ENTITIES.md ENTITIES.md.backup
```

#### 3. Review Current Sync Date

```bash
# Check last sync date
grep "hubspot_last_sync" PROJECT.md
```

#### 4. Run HubSpot Sync

**Full sync:**
```bash
/hubspot-sync company='Company Name'
```

**Or use dry-run to preview:**
```bash
/hubspot-sync company='Company Name' --dry-run
```

**Or partial sync:**
```bash
# Just contacts
/hubspot-sync company='Company Name' --contacts-only

# Just recent meetings
/hubspot-sync company='Company Name' --notes-only --from=2025-01-01
```

#### 5. Review Changes

**Check PROJECT.md:**
```bash
vim PROJECT.md
```

Look for:
- Updated `hubspot_last_sync` date
- New or updated deal information
- Any changes to company details

**Check ENTITIES.md:**
```bash
vim ENTITIES.md
```

Look for:
- New contacts added
- Updated contact information
- New HubSpot links

**Check meeting-notes/:**
```bash
ls -lt meeting-notes/
```

Look for:
- Newly imported meeting notes
- Check dates and topics

**Check assets/hubspot-files/:**
```bash
ls -lR assets/hubspot-files/
```

Look for:
- New downloaded attachments

#### 6. Merge Manual Changes

If you had manually added information:

```bash
# Compare with backup
diff PROJECT.md.backup PROJECT.md
diff ENTITIES.md.backup ENTITIES.md
```

**Manually merge** any custom information that wasn't preserved.

#### 7. Review and Enhance Synced Data

**Add context to contacts:**
```bash
vim ENTITIES.md
```

Add notes like:
```markdown
- **John Smith** - CEO
  - Email: john.smith@acme.com
  - HubSpot: [View Contact](...)
  - Source: HubSpot (synced 2025-01-31)
  - Notes: Prefers morning meetings, decision maker for budget, timezone: PST
```

**Review meeting notes:**
```bash
cd meeting-notes
ls -lt

# Read recent imports
cat 2025-01-25-status-meeting.md
```

Add any missing context or action items.

#### 8. Update PROJECT.md

```bash
vim PROJECT.md
```

Update if needed:
```yaml
last_updated: 2025-01-31
```

#### 9. Commit Changes

```bash
cd ~/projects

git add -A

git commit -m "$(cat <<'EOF'
Re-sync HubSpot data for Acme Corporation project

Updated project with latest HubSpot data:
- Refreshed company details
- Added 2 new contacts
- Imported 3 new meeting notes from January
- Downloaded 5 new attachments

Last sync: 2025-01-31

🤖 Generated with Claude Code

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

#### 10. Clean Up Backups

```bash
# Remove backup files if satisfied
rm PROJECT.md.backup ENTITIES.md.backup
```

### Checklist

- [ ] Navigated to project
- [ ] Created backup (optional)
- [ ] Checked last sync date
- [ ] Ran HubSpot sync (full or partial)
- [ ] Reviewed PROJECT.md changes
- [ ] Reviewed ENTITIES.md changes
- [ ] Reviewed new meeting notes
- [ ] Reviewed new attachments
- [ ] Merged manual changes if needed
- [ ] Enhanced synced data with context
- [ ] Updated last_updated date
- [ ] Committed changes to Git
- [ ] Cleaned up backup files

### Expected Time

**Total**: 15-30 minutes (depending on amount of new data)

---

## Workflow 6: Session Management

**Goal**: Save and restore work sessions for continuity

### Saving a Session

**When to Use:**
- End of work day
- Before closing Claude Code
- After significant work completed
- Before trying experimental changes

#### Steps

```bash
# Navigate to current working directory
cd ~/projects/work/client-projects/current-project

# Save session state
/save-session-state
```

**Skill will:**
- Capture metadata (session ID, timestamp, working directory)
- Summarize conversation (topic, key points, decisions)
- Save active todos with context
- Capture environment variables
- Note recent actions
- Save to `~/.claude/session-state/SESSION-ID-snapshot.json`
- Create symlink to `current-session.json`

**Review saved state:**
```bash
cat ~/.claude/session-state/current-session.json | head -50
```

### Restoring a Session

**When to Use:**
- Starting new Claude Code session
- Continuing work after a break
- Returning to project after working on something else

#### Steps

```bash
# Launch Claude Code
claude

# Restore last session
/restore-session-state
```

**Or explicitly restore:**
```bash
restore my session
```

**Skill will:**
- Load most recent snapshot
- Display session summary
- Show key points and decisions
- Restore todo list
- Show next steps
- Suggest what to do next

**Review restored context:**
- Read the summary carefully
- Check todo list
- Review next steps
- Continue with suggested action

### Best Practices

**Save sessions:**
- At end of each work session
- After completing major tasks
- Before experimenting with changes
- When switching between projects

**Restore sessions:**
- At start of each work session
- When resuming after interruption
- If you forget where you left off

### Checklist

**Saving:**
- [ ] In appropriate working directory
- [ ] Ran /save-session-state
- [ ] Reviewed saved state
- [ ] Session ID noted (if needed)

**Restoring:**
- [ ] Ran /restore-session-state
- [ ] Reviewed session summary
- [ ] Checked todo list
- [ ] Understood next steps
- [ ] Continued work

### Expected Time

**Saving**: 1-2 minutes
**Restoring**: 2-3 minutes

---

## Workflow 7: Monthly Status Report

**Goal**: Generate comprehensive report of all projects

**Frequency**: Last day of each month or first day of new month

### Steps

#### 1. Generate Status Report

```bash
cd ~/projects

# Overall status
/status

# Category-specific
/status category=work
/status category=personal
/status category=development
```

#### 2. Analyze Active Projects

For each active project:

**Check health indicators:**
- Last updated date (< 7 days = healthy)
- Progress vs time elapsed
- Blocked status
- Overdue status

**Categorize:**
- ✅ On track
- ⚠️ At risk
- 🚫 Blocked
- ⏰ Overdue

#### 3. Create Monthly Report

```bash
cd ~/projects

# Create reports directory if needed
mkdir -p reports/monthly

# Create report
vim reports/monthly/2025-01-report.md
```

**Report structure:**
```markdown
# Monthly Project Report - January 2025

**Report Date**: 2025-01-31
**Reporting Period**: 2025-01-01 to 2025-01-31

---

## Executive Summary

- **Total Active Projects**: 12
- **Projects Completed This Month**: 3
- **Projects Started This Month**: 2
- **Average Progress**: 45%
- **On Track Projects**: 8
- **At Risk Projects**: 3
- **Blocked Projects**: 1

---

## Projects by Category

### Work Projects (5 active)

**On Track:**
1. **Acme Website Redesign** (65% complete)
   - Status: Active, on schedule
   - Next milestone: Design review (Feb 5)

2. **Client B Mobile App** (40% complete)
   - Status: Active, progressing well
   - Next milestone: Beta release (Feb 15)

**At Risk:**
3. **Client C Integration** (20% complete)
   - Status: Behind schedule, need more resources
   - Blocker: Waiting on API documentation
   - Action: Escalate to client by Feb 2

**Blocked:**
4. **Partner Program** (0% complete)
   - Status: On hold
   - Blocker: Waiting on signed agreement
   - Action: Follow up with legal team

### Personal Projects (4 active)

...

### Development Projects (3 active)

...

---

## Completed This Month

1. **Project A** - Completed 2025-01-15
   - Delivered on time and under budget
   - Client satisfaction: 9/10

2. **Project B** - Completed 2025-01-22
   - Finished 1 week early
   - All success criteria met

3. **Project C** - Completed 2025-01-29
   - On schedule completion
   - Positive retrospective

---

## Started This Month

1. **New Project X** - Started 2025-01-10
   - HubSpot sync completed
   - Kickoff meeting held
   - Currently 15% complete

2. **New Project Y** - Started 2025-01-25
   - Initial planning phase
   - Requirements gathering in progress

---

## Key Metrics

| Metric | Value | Change vs Last Month |
|--------|-------|---------------------|
| Active Projects | 12 | +1 |
| Completion Rate | 3 projects | +1 |
| Average Progress | 45% | +10% |
| On Track % | 67% | -5% |
| Total Estimated Value | $500K | +$125K |

---

## Risks & Issues

### High Priority
1. **Client C Integration behind schedule**
   - Impact: May miss client deadline
   - Mitigation: Assign additional resources, daily standups

### Medium Priority
2. **Resource constraints on 3 projects**
   - Impact: Slower progress than planned
   - Mitigation: Prioritize high-value projects, defer low priority

---

## Action Items for Next Month

- [ ] Complete design review for Acme Website
- [ ] Resolve API documentation blocker for Client C
- [ ] Follow up on partner agreement
- [ ] Start 2 new client projects
- [ ] Archive 3 completed projects
- [ ] Conduct retrospectives for completed projects

---

## Lessons Learned

1. Early identification of blockers saves time
2. Weekly check-ins prevent projects from going stale
3. HubSpot integration speeds up client project setup
4. Buffer time in estimates is essential

---

**Report Generated**: 2025-01-31
**Next Report Due**: 2025-02-28
```

#### 4. Review with Stakeholders (Optional)

If relevant:
- Share report with team
- Discuss at risk projects
- Align on priorities for next month

#### 5. Commit Report

```bash
cd ~/projects

git add reports/monthly/2025-01-report.md

git commit -m "Add January 2025 monthly project report"
```

### Checklist

- [ ] Generated status reports
- [ ] Analyzed active projects
- [ ] Created monthly report document
- [ ] Categorized projects by health
- [ ] Listed completed projects
- [ ] Identified risks and issues
- [ ] Created action items for next month
- [ ] Documented lessons learned
- [ ] Reviewed with stakeholders (if applicable)
- [ ] Committed report to Git

### Expected Time

**Total**: 45-60 minutes

---

## Workflow 8: Handling Project Blockers

**Goal**: Document, track, and resolve project blockers

**When to Use:**
- Project cannot proceed without external input
- Waiting on decisions or approvals
- Dependencies not yet available
- Resource constraints

### Steps

#### 1. Identify and Document Blocker

```bash
cd ~/projects/work/client-projects/blocked-project

vim PROJECT.md
```

**Update YAML:**
```yaml
blocked: true
needs_review: true
last_updated: 2025-01-31
```

**Document in constraints section:**
```markdown
### Constraints

**Current Blockers**:
- **Blocker**: Waiting on API documentation from client
  - **Impact**: Cannot proceed with backend integration
  - **Owner**: Jane Doe (Client CTO)
  - **Due**: 2025-02-05
  - **Escalation**: If not received by Feb 5, escalate to John Smith (CEO)
```

#### 2. Update tasks.md

```bash
vim tasks.md
```

**Flag blocked tasks:**
```markdown
## Blocked Tasks

### Implement API Integration
- **Status**: Blocked
- **Blocked by**: Missing API documentation from client
- **Resolution needed**: Client to provide complete API docs
- **Owner**: Jane Doe (Client)
- **Follow-up date**: 2025-02-05
- **Escalation plan**: Contact John Smith if not resolved
```

#### 3. Create Action Item

Add to tasks.md:
```markdown
### High Priority
- [→] Follow up on API documentation
  - Due: 2025-02-03 (2 days before deadline)
  - Assignee: You
  - Action: Email Jane Doe, CC John Smith
  - Notes: Polite reminder, emphasize impact on timeline
```

#### 4. Document in Meeting Notes

If discussed in meeting:

```bash
vim meeting-notes/2025-01-31-status-sync.md
```

Add:
```markdown
## Blockers Discussed

### API Documentation Blocker
- **Issue**: Still waiting on complete API documentation
- **Impact**: Backend integration cannot start, 2 weeks behind
- **Commitment**: Jane committed to delivery by Feb 5
- **Follow-up**: Jason to check in Feb 3, escalate to John if needed
```

#### 5. Set Reminder

Add to your calendar or task manager:
- Feb 3: Check in with Jane about API docs
- Feb 5: If not received, escalate to John

#### 6. Update Status Report

When running `/status`, the blocked flag will highlight this project.

#### 7. Communicate with Stakeholders

**Internal team:**
- Notify team of blocker
- Adjust other project priorities if needed
- Reallocate resources temporarily

**Client/external:**
- Send polite follow-up email
- Reiterate impact and urgency
- Offer to help resolve blocker
- Set clear deadline for response

**Example email:**
```
Subject: Follow-up: API Documentation for Integration

Hi Jane,

I wanted to follow up on the API documentation we discussed in our last meeting. We're eager to move forward with the backend integration, but we need the complete documentation to proceed.

Without the API docs, we're currently blocked on:
- Backend integration (2 weeks of work)
- Testing and QA (1 week)
- Final deployment preparation

Could you provide the documentation by February 5th? If there are any issues or delays, please let me know so we can adjust our timeline accordingly.

Happy to jump on a quick call if that would help clarify anything.

Thanks,
Jason
```

#### 8. When Blocker is Resolved

```bash
cd ~/projects/work/client-projects/previously-blocked-project

vim PROJECT.md
```

**Update YAML:**
```yaml
blocked: false
needs_review: false
last_updated: 2025-02-06
```

**Update constraints:**
```markdown
### Constraints

**Resolved Blockers**:
- ~~Waiting on API documentation~~ ✓ Received 2025-02-06
```

**Update tasks.md:**
```markdown
- [✓] Follow up on API documentation - Completed 2025-02-06
  - Outcome: Received complete API docs, can proceed with integration

## Active Tasks

### High Priority
- [→] Implement API integration
  - Was blocked, now in progress
  - Due: 2025-02-20
```

**Commit changes:**
```bash
cd ~/projects

git add -A

git commit -m "Resolve API documentation blocker - integration can proceed"
```

### Checklist

**When Blocked:**
- [ ] Set blocked flag in PROJECT.md
- [ ] Document blocker with full context
- [ ] Flag blocked tasks in tasks.md
- [ ] Create follow-up action items
- [ ] Set reminders for follow-up
- [ ] Communicate with stakeholders
- [ ] Commit changes to Git

**When Unblocked:**
- [ ] Clear blocked flag
- [ ] Document resolution
- [ ] Update tasks to active
- [ ] Resume work
- [ ] Commit changes

### Expected Time

**Documentation**: 10-15 minutes
**Follow-up**: 5-10 minutes per check-in
**Resolution**: 5 minutes to update

---

## Additional Workflows

See also:
- [HubSpot Integration Setup](../integrations/hubspot-setup-guide.md)
- [Skills Reference Guide](../skills/README.md)
- [File Structure Reference](../file-structures/project-files-reference.md)

---

**Last Updated**: 2025-12-29
**Documentation Version**: 1.0.0
