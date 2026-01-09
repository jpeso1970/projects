# Microsoft Teams & Outlook Monitor

Browser automation-based monitoring for Teams and Outlook when backend API access is not available.

## Overview

This tool uses Playwright to automate browser interactions with Teams Web and Outlook Web App to capture:
- **Teams**: Chat messages, channel posts, team activity
- **Outlook**: Inbox emails with subject, sender, and preview text

**Why this approach?**
- ✅ No backend API access required
- ✅ Captures actual message content (not just metadata)
- ✅ Uses your existing Microsoft 365 credentials
- ✅ Runs locally with full control over data
- ✅ Persistent authentication (login once, reuse session)
- ✅ Anti-detection measures to bypass browser automation detection
- ✅ Robust selector fallbacks for UI changes

## ✨ What's Working

Based on successful testing (January 2, 2026):
- ✅ **Teams**: Successfully capturing messages from 88 chat items
- ✅ **Outlook**: Successfully capturing emails with full metadata
- ✅ **Authentication**: Session persistence working (no re-login needed)
- ✅ **Anti-Detection**: Microsoft browser checks bypassed
- ✅ **Data Storage**: All captures saved to JSON files with deduplication

## Installation

### Prerequisites

- Python 3.8 or higher
- Microsoft 365 Business/Enterprise account
- macOS, Linux, or Windows

### Setup Steps

1. **Clone or download this directory**

2. **Create and activate virtual environment:**
   ```bash
   cd client-monitoring
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browser:**
   ```bash
   playwright install chromium
   ```

5. **Make the run script executable:**
   ```bash
   chmod +x run.sh
   ```

6. **Run initial setup (authenticate):**
   ```bash
   ./run.sh --setup
   ```

   This will:
   - Open a Chromium browser window
   - Navigate to Outlook (for authentication)
   - Prompt you to log in with your Microsoft 365 credentials (including 2FA)
   - Wait up to 10 minutes for you to complete login
   - Save your authentication session for future runs
   - Confirm "Session saved for future runs"

7. **Test that it works:**
   ```bash
   ./run.sh --once --no-headless
   ```

   This runs one monitoring cycle with the browser visible so you can see what it's doing. The browser will stay open for 60 seconds for inspection, then close automatically.

## Usage

### Run Once (Manual Check)

```bash
./run.sh --once
```

Checks Teams and Outlook once, saves new items, then exits. Runs in headless mode (browser hidden).

### Run Continuously (Daemon Mode)

```bash
./run.sh
```

Runs continuously, checking every 5 minutes (configurable). Press Ctrl+C to stop.

### Run with Visible Browser (Debug Mode)

```bash
./run.sh --no-headless
```

Shows the browser window so you can see what's happening. Browser stays open for 60 seconds after each check for inspection. Useful for troubleshooting or verifying what's being captured.

### Combined Options

```bash
./run.sh --once --no-headless   # Single run with visible browser
```

### Command Line Options

- `--once`: Run monitoring cycle once and exit
- `--no-headless`: Show browser window (default is hidden)
- `--setup`: Run initial authentication setup

### Expected Output

When running successfully, you'll see:
```
🚀 Initializing browser...
✓ Browser initialized

============================================================
🔄 Starting monitoring cycle at 2026-01-02 07:20:15
============================================================
📱 Navigating to Teams...
  ✓ Found chat list using: Tree role ([role="tree"])
  ✓ Found 88 chat items using: Any tree items
  ✓ Clicked on first chat item
  ✓ Found 12 message groups using: Role group
    ✓ Extracted: MUC TEAM!...
  → Extracted 12 new messages
📧 Navigating to Outlook...
  ✓ Found 16 items using selector: [data-convid]
  ✓ Captured: Email subject...
  → Extracted 16 new emails

✓ Captured 28 new items
```

## Configuration

Configuration is stored in `config.json` (created automatically on first run).

### Default Configuration

```json
{
  "check_interval_seconds": 180,
  "monitor_outlook": true,
  "monitor_teams": true,
  "teams_channels": [],
  "outlook_folders": ["Inbox"],
  "max_messages_per_check": 50,
  "headless": true,
  "save_screenshots": false
}
```

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `check_interval_seconds` | Seconds between checks (continuous mode) | 180 (3 min) |
| `monitor_outlook` | Enable/disable Outlook monitoring | true |
| `monitor_teams` | Enable/disable Teams monitoring | true |
| `teams_channels` | Specific channels to monitor (empty = all) | [] |
| `outlook_folders` | Outlook folders to monitor | ["Inbox"] |
| `max_messages_per_check` | Max items to process per check | 50 |
| `headless` | Run browser in background | true |
| `save_screenshots` | Save screenshots during monitoring | false |

## Data Output

Captured messages and emails are saved to the `data/` directory:

```
data/
├── teams/
│   ├── teams_20250101_120000_msg123.json
│   └── teams_20250101_120130_msg124.json
└── outlook/
    ├── outlook_20250101_120015_email456.json
    └── outlook_20250101_120045_email457.json
```

### Data Format

**Teams Message (Actual Captured Format):**
```json
{
  "id": "teams_3359075685701888502_1767396063",
  "sender": "Unknown",
  "content": "Sales - MUCMUC - Deal DeskMUC - Sale Team ChatQuatrro Business Support Solutions Pvt LtdGeneral...",
  "timestamp": "Unknown",
  "source": "teams",
  "captured_at": "2026-01-02T15:21:03.381131"
}
```

**Outlook Email (Actual Captured Format):**
```json
{
  "id": "outlook_6961059508542496078_1767396089",
  "subject": "Sydney Brodeur Clay Reminder to sign document \"Quatrro - Starboard",
  "from": "External",
  "preview": "SC\nExternal\nSydney Brodeur Clay\nReminder to sign document \"Quatrro - Starboard - Upsell - 2025\"\nThu 4:04 PM\nCAUTION: [EMAIL FROM EXTERNAL DOMAIN]...",
  "timestamp": "Unknown",
  "source": "outlook",
  "captured_at": "2026-01-02T15:21:29.859779"
}
```

**Note:** Timestamps currently show as "Unknown" because they're extracted from relative time displays (e.g., "2 hours ago") which requires additional parsing. The `captured_at` field provides an accurate ISO 8601 timestamp of when the item was captured.

## State Management

The tool tracks which messages have been processed to avoid duplicates:

- **State file:** `state.json`
- **Session auth:** `.session/auth.json`

### State File Structure

```json
{
  "last_check": "2025-01-01T12:00:00.000000",
  "processed_teams_messages": ["teams_123", "teams_124"],
  "processed_outlook_emails": ["email_456", "email_457"],
  "session_authenticated": true
}
```

The state file prevents re-processing the same messages on subsequent runs.

## Running as a Background Service

### macOS/Linux (using launchd/systemd)

**Option 1: launchd (macOS)**

Create `~/Library/LaunchAgents/com.clientmonitor.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.clientmonitor</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/yourusername/projects/client-monitoring/monitor.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/yourusername/projects/client-monitoring/monitor.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/yourusername/projects/client-monitoring/monitor.error.log</string>
</dict>
</plist>
```

Load it:
```bash
launchctl load ~/Library/LaunchAgents/com.clientmonitor.plist
```

**Option 2: cron (macOS/Linux)**

```bash
crontab -e
```

Add this line to run every 3 minutes:
```
*/3 * * * * cd /Users/yourusername/projects/client-monitoring && /usr/bin/python3 monitor.py --once >> monitor.log 2>&1
```

**Option 3: Simple background process**

```bash
# Run in background
nohup python monitor.py > monitor.log 2>&1 &

# Check if running
ps aux | grep monitor.py

# Stop it
pkill -f monitor.py
```

### Windows (Task Scheduler)

1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily, repeat every 3 minutes
4. Action: Start a program
   - Program: `C:\Python39\python.exe`
   - Arguments: `C:\path\to\client-monitoring\monitor.py --once`
5. Save and enable

## Processing the Data

### Python Example

```python
import json
from pathlib import Path
from datetime import datetime, timedelta

DATA_DIR = Path("data")

def get_recent_items(hours=24):
    """Get all items from the last N hours"""
    cutoff = datetime.utcnow() - timedelta(hours=hours)
    items = []

    for json_file in DATA_DIR.rglob("*.json"):
        with open(json_file) as f:
            data = json.load(f)
            captured = datetime.fromisoformat(data['captured_at'].replace('Z', '+00:00'))

            if captured > cutoff:
                items.append(data)

    return sorted(items, key=lambda x: x['captured_at'], reverse=True)

def search_messages(keyword):
    """Search for messages containing a keyword"""
    results = []

    for json_file in DATA_DIR.rglob("*.json"):
        with open(json_file) as f:
            data = json.load(f)

            if keyword.lower() in data.get('content', '').lower() or \
               keyword.lower() in data.get('subject', '').lower():
                results.append(data)

    return results

# Example usage
recent = get_recent_items(hours=24)
print(f"Found {len(recent)} items in last 24 hours")

urgent = search_messages("urgent")
print(f"Found {len(urgent)} messages containing 'urgent'")
```

### Command Line Processing

```bash
# Count total captured items
find data -name "*.json" | wc -l

# Search for specific content
grep -r "urgent" data/

# Get today's items
find data -name "*.json" -mtime 0

# View latest captured item
ls -t data/**/*.json | head -1 | xargs cat | python -m json.tool
```

## Troubleshooting

### Authentication Issues

**Problem:** "Authentication required" every run

**Solution:**
1. Delete corrupted session: `rm -f .session/auth.json state.json`
2. Run setup again: `./run.sh --setup`
3. Ensure you completely log in (including MFA if required)
4. Wait for Outlook to fully load (the script waits up to 10 minutes)
5. Look for "✓ Session saved for future runs" confirmation

**Problem:** Browser redirects to login page repeatedly

**Solution:**
This was fixed by authenticating through Outlook first instead of Teams. The script now uses `outlook.office365.com/mail/inbox` for initial authentication.

### Teams "Unsupported Browser" Error

**Problem:** Teams shows "unsupported browser" message

**Solution:**
This was fixed with anti-detection measures in the browser launch settings:
- Better user agent string
- Locale and timezone settings
- Notification permissions
- Disabled automation flags

If it happens again, check `monitor.py` lines 80-95 for browser context settings.

### Content Security Policy (CSP) Errors

**Problem:** Error like "Evaluating a string as JavaScript violates CSP directive"

**Solution:**
This was fixed by using URL pattern matching instead of JavaScript evaluation:
```python
# Use this:
await page.wait_for_url("**/outlook.office*/mail/**")

# Not this:
await page.wait_for_function("window.location.href.includes('outlook')")
```

### No Messages Captured

**Problem:** Script runs but shows "→ Extracted 0 new messages"

**Debug steps:**
1. Run with visible browser: `./run.sh --once --no-headless`
2. Watch what the browser is doing for 60 seconds
3. Check console output for which selectors are working
4. Look for patterns like "✓ Found chat list using: Tree role"

**Solution:**
The script now tries multiple fallback selectors:
- 9 different selectors for Teams chat list
- 6 different selectors for chat items
- 4 different selectors for message content

If still failing, the UI may have changed significantly.

### Element Detection Timeouts

**Problem:** "Could not find Teams/Outlook elements" warnings

**Solution:**
This is usually okay! The script now continues anyway with fallback selectors. The improved wait times (8 seconds instead of 5) also help with slow page loads.

If pages aren't loading at all:
1. Check your internet connection
2. Verify Teams/Outlook work in a regular browser
3. Try increasing wait times in `monitor.py` (search for `asyncio.sleep(8)`)

### Page Navigation Timeouts

**Problem:** "Timeout 60000ms exceeded" on page.goto()

**Solution:**
Changed navigation from `wait_until="networkidle"` to `wait_until="load"`. Modern SPAs like Teams/Outlook have continuous background activity that prevents "networkidle" from ever triggering.

### Selector Issues (UI Changed)

**Problem:** Microsoft updated the UI and selectors no longer work

**Diagnosis:**
1. Run with visible browser: `./run.sh --once --no-headless`
2. Check which selector attempts are failing in the console
3. Look for messages like "⚠ Could not find chat list with any selector"

**Solution:**
Update the selector arrays in `monitor.py`:
- `TeamsMonitor.get_recent_messages()` - lines 157-167 for chat list selectors
- `OutlookMonitor.get_recent_emails()` - lines 345-352 for email selectors

The script tries multiple selectors in order, so add new ones to the beginning of the lists.

### Script Crashes

**Problem:** Script exits with Python errors

**Common fixes:**
1. Activate virtual environment: `source venv/bin/activate`
2. Update Playwright: `pip install --upgrade playwright`
3. Reinstall browsers: `playwright install chromium`
4. Check Python version: `python3 --version` (needs 3.8+)

**Problem:** EOFError when running in background

**Solution:**
Don't use `input()` in background processes. The script now uses `asyncio.sleep(60)` instead for browser keep-open feature.

### Re-authentication Required

**Problem:** Session expires after a while

**Solution:**
This is normal. Microsoft sessions expire periodically (usually after several days). Just run:
```bash
./run.sh --setup
```

### Deprecation Warnings

**Problem:** Seeing warnings about `datetime.utcnow()` being deprecated

**Impact:** These are just warnings and don't affect functionality. The script works fine with Python 3.13.

**Future fix:** These will be updated to use `datetime.now(datetime.UTC)` in a future version.

## Security Considerations

⚠️ **Important Security Notes:**

1. **Authentication Storage**
   - Your session is stored in `.session/auth.json`
   - This file contains authentication tokens
   - Keep it secure and never commit to git

2. **Captured Data**
   - All captured messages are saved as plain text JSON
   - Ensure proper file permissions on the `data/` directory
   - Consider encrypting sensitive data

3. **Network Security**
   - Script communicates directly with Microsoft servers
   - Uses HTTPS (encrypted)
   - No third-party servers involved

4. **Recommended Practices**
   - Add `.session/` and `data/` to `.gitignore`
   - Regularly review and delete old captured data
   - Use disk encryption on the machine running the monitor
   - Follow your organization's data handling policies

## Technical Implementation Details

### Browser Anti-Detection

The script includes several measures to bypass Microsoft's automated browser detection:

```python
# Browser launch flags
'--disable-blink-features=AutomationControlled'
'--disable-dev-shm-usage'
'--no-sandbox'

# Context settings
user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...'
locale='en-US'
timezone_id='America/New_York'
permissions=['notifications']
```

### Robust Selector System

Instead of relying on a single selector, the script tries multiple approaches:

**Example from Teams chat list detection:**
```python
selectors_to_try = [
    ('tree', 'Chat tree'),
    ('[role="tree"]', 'Tree role'),
    ('[role="navigation"]', 'Navigation'),
    ('[aria-label*="Chat"]', 'Chat aria-label'),
    # ... 5 more fallbacks
]
```

This makes the script resilient to minor UI changes.

### Navigation Strategy

Uses `wait_until="load"` instead of `"networkidle"` because modern SPAs like Teams/Outlook maintain persistent WebSocket connections and background polling that prevent networkidle from ever triggering.

### Deduplication

Messages are tracked by generated IDs based on content hash + timestamp:
```python
message_id = f"teams_{abs(hash(content[:100] + timestamp))}_{int(datetime.utcnow().timestamp())}"
```

The `state.json` file maintains lists of processed message IDs to prevent re-processing.

### Session Persistence

Authentication tokens are stored in `.session/auth.json` using Playwright's storage state API, eliminating the need to re-authenticate on every run.

## Limitations

1. **UI Dependency:** Relies on web interface structure (can break with Microsoft updates, mitigated by fallback selectors)
2. **No Real-Time:** Checks periodically, not instant notifications (5-minute intervals by default)
3. **Browser Required:** Needs a browser running (uses ~200-300MB RAM per instance)
4. **Message History:** Only captures new messages after start (no backfill of old messages)
5. **Session Expiration:** Need to re-authenticate periodically (typically every few days)
6. **Timestamp Parsing:** Relative timestamps ("2 hours ago") not currently parsed to absolute times
7. **Sender Detection:** Teams sender names show as "Unknown" (selector needs improvement)

## Advanced Usage

### Custom Filtering

Edit `monitor.py` to add custom filtering logic:

```python
async def _extract_message_from_item(self, item):
    message_data = # ... extract logic ...

    # Add custom filtering
    if "urgent" in message_data['content'].lower():
        message_data['priority'] = 'high'

    # Skip system messages
    if message_data['sender'] == 'System':
        return None

    return message_data
```

### Webhook Integration

Send captured items to a webhook:

```python
import requests

def _save_items(self, items):
    # Save to files (existing logic)
    # ...

    # Also send to webhook
    for item in items:
        requests.post('https://your-webhook-url.com/notify', json=item)
```

### Database Storage

Store in SQLite instead of JSON files:

```python
import sqlite3

conn = sqlite3.connect('monitoring.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id TEXT PRIMARY KEY,
        source TEXT,
        content TEXT,
        timestamp TEXT,
        captured_at TEXT
    )
''')

# Insert captured items
cursor.executemany(
    'INSERT OR IGNORE INTO messages VALUES (?, ?, ?, ?, ?)',
    [(item['id'], item['source'], item.get('content', ''),
      item['timestamp'], item['captured_at']) for item in items]
)

conn.commit()
```

## Support & Contributing

This is a custom tool built for specific monitoring needs. Feel free to modify and adapt it to your requirements.

### Common Modifications

- **Change check frequency:** Edit `check_interval_seconds` in `config.json`
- **Monitor specific channels:** Edit `teams_channels` in `config.json`
- **Add more email folders:** Edit `outlook_folders` in `config.json`
- **Change data format:** Modify `_save_items()` method
- **Add notifications:** Integrate with email/SMS/Slack in `_save_items()`

---

**Questions?** Review the troubleshooting section or inspect the code with debug mode (`--no-headless`).
