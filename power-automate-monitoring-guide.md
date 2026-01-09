# Power Automate Monitoring Guide
## Monitoring Outlook & Teams Without Backend API Access

**Last Updated:** 2025-12-30
**Purpose:** Monitor Outlook inbox and Teams activity (chat messages & channel posts) for client work

---

## Overview

This guide shows you how to use Microsoft Power Automate to monitor your Outlook and Teams accounts using your own user credentials (no backend API access or admin permissions required).

**What you'll build:**
1. Flow to capture Outlook emails → save to OneDrive
2. Flow to capture Teams channel posts → save to OneDrive
3. Flow to capture Teams chat messages → save to OneDrive
4. Local sync setup to get data on your filesystem

---

## Prerequisites

✅ Microsoft 365 Business/Enterprise account
✅ OneDrive access (included with M365)
✅ OneDrive Desktop app installed (for local sync)
✅ Access to Power Automate (https://make.powerautomate.com)

---

## Part 1: Setup OneDrive Storage Structure

Before creating flows, set up the destination folders:

### Step 1.1: Create Folder Structure

1. Open OneDrive (web or desktop)
2. Create a new folder: `Client-Monitoring`
3. Inside `Client-Monitoring`, create three subfolders:
   - `outlook-emails`
   - `teams-channels`
   - `teams-chats`

### Step 1.2: Create Initial Data Files

In each subfolder, create an initial JSON file:

**outlook-emails/emails.json:**
		

**teams-channels/messages.json:**
```json
{
  "messages": []
}
```

**teams-chats/chats.json:**
```json
{
  "chats": []
}
```

---

## Part 2: Create Outlook Monitoring Flow

### Step 2.1: Access Power Automate

1. Go to https://make.powerautomate.com
2. Sign in with your M365 credentials
3. Click **"+ Create"** in the left sidebar
4. Select **"Automated cloud flow"**

### Step 2.2: Configure Trigger

1. **Name your flow:** "Monitor Outlook Inbox"
2. **Search for trigger:** "When a new email arrives"
3. **Select:** "When a new email arrives (V3)" (Office 365 Outlook)
4. Click **"Create"**

### Step 2.3: Configure Trigger Settings

In the trigger configuration:
- **Folder:** Inbox (or specify a subfolder)
- **Include Attachments:** No (unless you need them)
- **Importance:** All
- **Only with Attachments:** No
- **Advanced options:**
  - To: (leave blank to monitor all)
  - From: (leave blank to monitor all)
  - Subject Filter: (optional - add keywords if needed)

### Step 2.4: Add Data Composition Step

1. Click **"+ New step"**
2. Search for **"Compose"** (Data Operation)
3. Select **"Compose"**
4. In the **Inputs** field, click to open dynamic content
5. Create a JSON object with the email data:

```json
{
  "id": @{triggerOutputs()?['body/id']},
  "timestamp": @{utcNow()},
  "received": @{triggerOutputs()?['body/receivedDateTime']},
  "from": @{triggerOutputs()?['body/from/emailAddress/address']},
  "from_name": @{triggerOutputs()?['body/from/emailAddress/name']},
  "to": @{triggerOutputs()?['body/toRecipients']},
  "subject": @{triggerOutputs()?['body/subject']},
  "body_preview": @{triggerOutputs()?['body/bodyPreview']},
  "importance": @{triggerOutputs()?['body/importance']},
  "has_attachments": @{triggerOutputs()?['body/hasAttachments']},
  "conversation_id": @{triggerOutputs()?['body/conversationId']}
}
```

**Note:** You'll need to replace the `@{...}` sections with dynamic content by clicking on the fields from the "When a new email arrives" trigger.

### Step 2.5: Append to OneDrive File

1. Click **"+ New step"**
2. Search for **"Append to array variable"**
3. But wait - Power Automate doesn't have a direct "append to JSON file" action
4. Instead, we'll use a different approach:

**Alternative Approach - Append to CSV:**

1. Click **"+ New step"**
2. Search for **"Create CSV table"** (Data Operation)
3. Input: Select **Outputs** from the Compose step
4. Click **"+ New step"**
5. Search for **"Append to a file"** (OneDrive for Business)
6. Configure:
   - **File:** Navigate to `Client-Monitoring/outlook-emails/emails.csv`
   - **Data:** Select **Output** from "Create CSV table"

**OR - Store Each Email as Separate JSON File:**

1. Click **"+ New step"**
2. Search for **"Create file"** (OneDrive for Business)
3. Configure:
   - **Folder Path:** `/Client-Monitoring/outlook-emails`
   - **File Name:** `email_@{triggerOutputs()?['body/id']}.json`
   - **File Content:** Select **Outputs** from the Compose step

### Step 2.6: Save and Test

1. Click **"Save"** in the top right
2. Click **"Test"** → **"Manually"**
3. Send yourself a test email
4. Verify the flow runs successfully
5. Check OneDrive for the captured data

---

## Part 3: Create Teams Channel Monitoring Flow

### Step 3.1: Create New Flow

1. In Power Automate, click **"+ Create"** → **"Automated cloud flow"**
2. **Name:** "Monitor Teams Channels"
3. **Search for trigger:** "When a new channel message is added"
4. **Select:** "When a new channel message is added" (Microsoft Teams)
5. Click **"Create"**

### Step 3.2: Configure Trigger

In the trigger:
- **Team:** Select the specific team, or use "All Teams" if available
- **Channel:** Select specific channel, or leave blank for all channels

**Important:** You may need to create separate flows for each team/channel you want to monitor if your organization restricts the trigger.

### Step 3.3: Add Data Composition

1. Click **"+ New step"**
2. Search for **"Compose"**
3. Build the message object:

```json
{
  "message_id": @{triggerOutputs()?['body/messageId']},
  "timestamp": @{utcNow()},
  "created": @{triggerOutputs()?['body/createdDateTime']},
  "team_name": @{triggerOutputs()?['body/teamDisplayName']},
  "channel_name": @{triggerOutputs()?['body/channelName']},
  "from": @{triggerOutputs()?['body/from/user/displayName']},
  "from_email": @{triggerOutputs()?['body/from/user/userIdentityType']},
  "message": @{triggerOutputs()?['body/body/content']},
  "subject": @{triggerOutputs()?['body/subject']}
}
```

### Step 3.4: Save to OneDrive

Similar to Outlook flow, choose one:

**Option A - Separate JSON files:**
- Action: **"Create file"** (OneDrive for Business)
- Folder: `/Client-Monitoring/teams-channels`
- File Name: `msg_@{triggerOutputs()?['body/messageId']}.json`
- Content: Outputs from Compose

**Option B - Append to CSV:**
- Convert to CSV table
- Append to `teams-channels/messages.csv`

### Step 3.5: Save and Test

1. Save the flow
2. Test by posting a message in the monitored channel
3. Verify the file appears in OneDrive

---

## Part 4: Create Teams Chat Monitoring Flow

### Step 4.1: Create New Flow

1. Click **"+ Create"** → **"Automated cloud flow"**
2. **Name:** "Monitor Teams Chats"
3. **Search for trigger:** "When a new chat message is received"
4. **Select:** "When a chat message is received in Teams" (Microsoft Teams)

**⚠️ Important Limitation:** This trigger might not be available in all Microsoft 365 tenants due to organizational policies. If you don't see it, see the "Limitations & Workarounds" section.

### Step 4.2: Configure Similar to Channel Flow

Follow the same pattern as the channel monitoring flow:
1. Compose the message data
2. Save to OneDrive (`/Client-Monitoring/teams-chats/`)
3. Test the flow

---

## Part 5: Local Sync Setup

### Step 5.1: Configure OneDrive Desktop Sync

1. **Install OneDrive** (if not already installed)
   - Windows: Comes pre-installed
   - Mac: Download from Microsoft

2. **Sign in to OneDrive Desktop App**
   - Click the OneDrive icon in system tray
   - Sign in with your M365 credentials

3. **Configure Sync Settings**
   - Open OneDrive settings
   - Go to "Account" tab
   - Click "Choose folders"
   - Ensure "Client-Monitoring" folder is selected
   - Click OK

4. **Locate Synced Files**
   - Windows: `C:\Users\YourName\OneDrive - CompanyName\Client-Monitoring`
   - Mac: `/Users/YourName/OneDrive - CompanyName/Client-Monitoring`

### Step 5.2: Verify Sync

1. Check that the folder exists locally
2. Trigger one of your flows (send an email, post a Teams message)
3. Verify the file appears locally within 1-2 minutes

---

## Part 6: Reading the Data Programmatically

Once synced locally, you can process the files with any language. Here's a Python example:

```python
import json
import os
from pathlib import Path
from datetime import datetime

# Path to synced OneDrive folder
MONITORING_PATH = Path.home() / "OneDrive - CompanyName" / "Client-Monitoring"

def read_outlook_emails():
    """Read all captured emails"""
    emails_dir = MONITORING_PATH / "outlook-emails"
    emails = []

    for file in emails_dir.glob("email_*.json"):
        with open(file, 'r') as f:
            emails.append(json.load(f))

    return sorted(emails, key=lambda x: x['timestamp'], reverse=True)

def read_teams_messages():
    """Read all Teams channel messages"""
    messages_dir = MONITORING_PATH / "teams-channels"
    messages = []

    for file in messages_dir.glob("msg_*.json"):
        with open(file, 'r') as f:
            messages.append(json.load(f))

    return sorted(messages, key=lambda x: x['timestamp'], reverse=True)

def get_new_items_since(directory, since_timestamp):
    """Get only new items since a specific timestamp"""
    new_items = []

    for file in directory.glob("*.json"):
        with open(file, 'r') as f:
            data = json.load(f)
            item_time = datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00'))

            if item_time > since_timestamp:
                new_items.append(data)

    return new_items

# Example usage
if __name__ == "__main__":
    emails = read_outlook_emails()
    print(f"Total emails captured: {len(emails)}")

    if emails:
        latest = emails[0]
        print(f"\nLatest email:")
        print(f"  From: {latest['from_name']} <{latest['from']}>")
        print(f"  Subject: {latest['subject']}")
        print(f"  Received: {latest['received']}")
```

---

## Part 7: Flow Management & Monitoring

### Monitor Flow Health

1. Go to https://make.powerautomate.com
2. Click **"My flows"** in left sidebar
3. View run history for each flow:
   - Green checkmark = successful run
   - Red X = failed run
   - Click on any run to see details

### Handle Flow Failures

Common failure reasons:
- **Permission issues:** Re-authenticate the connection
- **File not found:** Ensure OneDrive folders exist
- **Throttling:** Microsoft limits flow runs (see below)

### Flow Run Frequency

Power Automate triggers check for new items at these intervals:
- **Free license:** Every 15 minutes
- **Premium license:** Every 1-3 minutes
- **Instant triggers:** Near real-time (30 seconds - 2 minutes)

Your flows will run automatically whenever a new email/message arrives (subject to these intervals).

---

## Limitations & Workarounds

### Limitation 1: Chat Message Trigger Not Available

**Problem:** "When a chat message is received" trigger may be disabled by IT.

**Workaround:**
- Use Microsoft Teams Power Apps integration
- Create a custom app with a button to manually log chats
- Or use the browser automation fallback (Playwright)

### Limitation 2: Teams Trigger Only Works for Specific Teams

**Problem:** Can't monitor "all teams" at once.

**Workaround:**
- Create multiple flows, one per team
- Use flow templates to speed up duplication

### Limitation 3: Message Content Truncation

**Problem:** Long messages might be truncated in trigger output.

**Workaround:**
- Add a "Get message details" action after the trigger
- Use the full message from the detailed output

### Limitation 4: No Historical Data

**Problem:** Flows only capture new items after they're enabled.

**Workaround:**
- For Outlook: Export existing emails first using Outlook's export feature
- For Teams: No easy workaround for historical messages

### Limitation 5: OneDrive Storage Limits

**Problem:** Free tier has limited storage (usually 1TB with business account).

**Workaround:**
- Periodically archive and delete old monitoring files
- Or use a cleanup flow to delete files older than X days

---

## Troubleshooting

### Issue: Flow doesn't trigger

**Check:**
1. Is the flow turned "On"? (toggle in My Flows)
2. Are the connections authenticated? (click "..." on flow → "Edit" → check connection status)
3. Are you testing with the right account? (some triggers only work for your own activity)
4. Check the flow's run history for errors

### Issue: Files not appearing in OneDrive

**Check:**
1. Go to OneDrive web interface and verify files are there
2. Check OneDrive Desktop sync status (icon in system tray)
3. Try manually triggering sync: Right-click OneDrive icon → "Settings" → "Account" → "Choose folders" → OK

### Issue: Duplicate messages being captured

**Problem:** Sometimes triggers fire multiple times for the same item.

**Fix:**
Add a condition to check if the file already exists:
1. After trigger, add "Get file metadata" action
2. Use the message ID in the file path
3. Add a condition: "If file exists, terminate flow"
4. Otherwise, proceed with creating the file

### Issue: Permission errors

**Fix:**
1. Go to "My flows"
2. Click "..." on the failing flow
3. Select "Edit"
4. Click on any action showing a warning
5. Re-authorize the connection
6. Save the flow

---

## Next Steps

### Basic Setup Complete ✅

You now have:
- ✅ Outlook emails being captured to OneDrive
- ✅ Teams channel messages being captured
- ✅ (Optional) Teams chats being captured
- ✅ Local sync to your filesystem
- ✅ Data accessible for programmatic processing

### Advanced Enhancements

**1. Add Filtering**
- Modify triggers to only capture specific senders/keywords
- Add conditions to filter out system messages

**2. Add Notifications**
- Add an action to send email/SMS when high-priority items arrive
- Use the "Send me an email notification" action

**3. Data Processing**
- Create a scheduled flow to process/summarize the data daily
- Use Power Automate Desktop to process the local files

**4. Backup Strategy**
- Create a flow to periodically copy monitoring data to SharePoint or another backup location
- Set up archival for old data

**5. Dashboard**
- Use Power BI to create visualizations of your monitoring data
- Connect Power BI directly to the OneDrive files

---

## Security & Privacy Considerations

⚠️ **Important:**
- These flows run with your user credentials
- All data is stored in your OneDrive (subject to your org's policies)
- Be mindful of capturing sensitive client information
- Consider encryption for sensitive data
- Follow your organization's data handling policies
- Regularly review and delete old monitoring data

---

## Alternative: Browser Automation Fallback

If Power Automate doesn't work due to organizational restrictions, you can fall back to the Playwright browser automation approach. Let me know if you need that solution instead.

---

## Support Resources

- **Power Automate Documentation:** https://learn.microsoft.com/en-us/power-automate/
- **Teams Connector Reference:** https://learn.microsoft.com/en-us/connectors/teams/
- **Outlook Connector Reference:** https://learn.microsoft.com/en-us/connectors/office365/

---

**Questions or issues?** Test each flow individually and check the run history for detailed error messages.
