# Sent Message Monitoring Enhancement

## Overview

The monitoring system now checks **both your inbox and sent messages** to help you identify which urgent items you've already replied to versus those that still need action.

## What's New

### 1. Sent Message Capture
- **New folder**: `data/outlook-sent/` stores all captured sent messages
- **Automatic monitoring**: Every monitoring cycle now captures recent sent emails
- **State tracking**: Sent messages are tracked separately to avoid duplicate captures

### 2. Urgent Message Cross-Reference
- **Smart matching**: Compares inbox urgent items against sent messages by subject
- **Reply detection**: Identifies which urgent messages have corresponding replies
- **Clear reporting**: Shows two lists - items needing action vs already handled

## How It Works

### Monitoring Flow
```
./run.sh --once
├─ Checks Inbox (as before)
├─ Checks Teams (as before)
└─ NEW: Checks Sent Items folder
   └─ Captures recent sent emails
   └─ Stores in data/outlook-sent/
```

### Urgent Check Flow
```
python3 check_urgent.py --hours 24
├─ Scans inbox for urgent keywords
├─ Scans sent folder for your replies
├─ Matches subjects between inbox and sent
└─ Reports:
   ├─ ⚠️  NEEDS ACTION (no reply found)
   └─ ✅ ALREADY REPLIED (reply detected)
```

## Usage

### Run Monitoring (captures sent + inbox)
```bash
./run.sh --once
```

### Check Urgent Messages

**Simple matching** (fast, pattern-based):
```bash
python3 check_urgent.py --hours 24
```

**LLM matching** (smart, semantic understanding):
```bash
./check_urgent_llm.sh --hours 24
```

The LLM version uses Claude Haiku to intelligently understand if messages are related, even when:
- Subject lines don't overlap
- You forwarded the request to someone else
- The reply addresses the topic but with different wording

**Setup for LLM matching:**
```bash
export ANTHROPIC_API_KEY='your-api-key-here'
# Or add to ~/.zshrc for permanence
```

### Example Output
```
================================================================================
URGENT MESSAGES REPORT
================================================================================

⚠️  NEEDS ACTION (2 items)
--------------------------------------------------------------------------------

1. FROM: Pinky Dedhia
   SUBJECT: MUC US Cost Budget Discussion
   TIME: 5:39 AM (captured: 2026-01-02 17:05)
   PREVIEW: Hi Jason, Please update on required data of US cost for budget...
   STATUS: ⚠️  NO REPLY FOUND

2. FROM: Sydney Brodeur Clay
   SUBJECT: Reminder to sign document "Quatrro - Starboard - Upsell - 2025"
   TIME: 4:04 PM (captured: 2026-01-02 17:30)
   PREVIEW: CAUTION: [EMAIL FROM EXTERNAL DOMAIN] This email...
   STATUS: ⚠️  NO REPLY FOUND

✅ ALREADY REPLIED (1 item)
--------------------------------------------------------------------------------

1. FROM: Patty Hernandez
   SUBJECT: Adding users to Expandshare
   TIME: 12:21 PM (captured: 2026-01-02 11:17)
   STATUS: ✅ Reply found in sent items

================================================================================
SUMMARY: 2 need action, 1 already handled
================================================================================
```

## Technical Details

### Files Modified
- **monitor.py**:
  - Added `get_sent_emails()` method to `OutlookMonitor` class
  - Updated `_extract_email_from_option()` to accept `folder` parameter
  - Modified `run_monitoring_cycle()` to capture sent messages
  - Updated `_save_items()` to store sent messages separately

### Files Created
- **check_urgent.py**: New script for urgent message analysis with reply detection
- **SENT_MONITORING.md**: This documentation file

### Data Structure

**Inbox email:**
```json
{
  "id": "outlook_inbox_{hash}_{timestamp}",
  "subject": "Email subject",
  "from": "Sender Name",
  "to": "Unknown",
  "preview": "Email preview...",
  "timestamp": "Unknown",
  "source": "outlook",
  "folder": "inbox",
  "captured_at": "2026-01-02T19:17:28.651391"
}
```

**Sent email:**
```json
{
  "id": "outlook_sent_{hash}_{timestamp}",
  "subject": "Email subject",
  "from": "Me",
  "to": "Recipient Name",
  "preview": "Email preview...",
  "timestamp": "Unknown",
  "source": "outlook",
  "folder": "sent",
  "captured_at": "2026-01-02T19:17:28.651391"
}
```

### Subject Matching Logic

The urgent checker normalizes subjects for comparison by:
1. Converting to lowercase
2. Removing common prefixes (RE:, FW:, [Draft], etc.)
3. Extracting core subject text
4. Comparing inbox subjects against sent subjects

This allows it to match:
- "RE: Budget Discussion" (inbox)
- "Budget Discussion" (sent)

As the **same conversation**.

## Urgent Keywords

The system flags messages containing these keywords:
- urgent, asap, immediate, priority, critical
- budget, deadline, action required, approval, sign
- reminder, please, needed, required, request

## Benefits

1. **No False Positives**: Avoid being alerted about items you've already handled
2. **Clear Priorities**: See exactly which urgent items need your attention
3. **Complete Context**: View both incoming requests and your responses
4. **Time Savings**: No manual checking of sent folder to verify replies

## Future Enhancements

Potential improvements:
- Add conversation threading (group related messages)
- Track response time metrics
- Add email body analysis for better matching
- Support for more complex reply patterns (forwarding, multiple recipients)
- Integration with calendar to track follow-up dates

## Troubleshooting

### No sent messages captured
- Ensure monitoring ran successfully (`./run.sh --once`)
- Check `data/outlook-sent/` directory exists and has files
- Verify state file tracks sent messages: `grep outlook-sent state.json`

### Reply not detected
- Subject lines must match after normalization
- Reply must be captured in same time window as inbox check
- Check `check_urgent.py` logs for subject matching details

### Too many false urgent items
- Adjust `URGENT_KEYWORDS` list in `check_urgent.py`
- Increase specificity of keywords (e.g., "budget approval" vs "budget")
- Filter by sender domains (add to script)

## Maintenance

- **State file**: Automatically maintains last 1000 IDs per source
- **Data cleanup**: Consider archiving old JSON files periodically
- **Monitoring frequency**: Adjust `check_interval_seconds` in `config.json`

---

**Last Updated**: 2026-01-02
**Version**: 1.0
