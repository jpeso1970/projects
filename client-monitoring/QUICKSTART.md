# Quick Start Guide

Get up and running in 5 minutes.

## Step 1: Install Dependencies

```bash
cd /Users/jasonpace/projects/client-monitoring

# Install Python package
pip install playwright

# Install browser
playwright install chromium
```

## Step 2: Authenticate

```bash
python monitor.py --setup
```

This opens a browser window. Log in with your Microsoft 365 credentials (including MFA if required). The script will save your session for future runs.

## Step 3: Test It

```bash
python monitor.py --once --no-headless
```

You'll see the browser:
1. Navigate to Teams
2. Check for messages
3. Navigate to Outlook
4. Check for emails
5. Save any new items to `data/`

## Step 4: Run Continuously

```bash
# Run in background, check every 3 minutes
nohup python monitor.py > monitor.log 2>&1 &

# Check the log
tail -f monitor.log

# Stop it later
pkill -f monitor.py
```

## Step 5: View Captured Data

```bash
# See statistics
python read_data.py --stats

# See latest 5 items
python read_data.py --latest 5

# Search for keyword
python read_data.py --search "urgent"

# See items from last 12 hours
python read_data.py --recent 12
```

## Data Location

Your captured messages are saved here:
```
data/
├── teams/
│   └── teams_20250101_120000_msg123.json
└── outlook/
    └── outlook_20250101_120000_email456.json
```

## Configuration

Edit `config.json` to change settings:
- Check interval (default: 180 seconds / 3 minutes)
- Enable/disable Teams or Outlook
- Max messages per check

## Troubleshooting

**Authentication fails?**
- Delete `.session/auth.json`
- Run `python monitor.py --setup` again

**No messages captured?**
- Run with `--no-headless` to see what's happening
- Check if you actually have new messages
- Teams/Outlook UI may have changed (see README.md for selector updates)

**Script crashes?**
- Check Python version: `python --version` (need 3.8+)
- Update Playwright: `pip install --upgrade playwright`
- Check the logs

## What Next?

- **Automate:** Set up cron job or launchd (see README.md)
- **Integrate:** Send data to webhook, database, or Slack
- **Customize:** Edit filters, add notifications, change output format

Read the full README.md for detailed documentation.
