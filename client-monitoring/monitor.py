#!/usr/bin/env python3
"""
Microsoft Teams & Outlook Monitor
Automated browser-based monitoring without backend API access
"""

import json
import asyncio
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
import argparse
import sys

# Configuration
CONFIG_FILE = Path(__file__).parent / "config.json"
STATE_FILE = Path(__file__).parent / "state.json"
DATA_DIR = Path(__file__).parent / "data"
SESSION_DIR = Path(__file__).parent / ".session"


class MonitorConfig:
    """Load and manage configuration"""

    def __init__(self):
        self.config = self._load_config()

    def _load_config(self):
        """Load configuration from file"""
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        else:
            # Create default config
            default_config = {
                "check_interval_seconds": 180,  # 3 minutes
                "monitor_outlook": True,
                "monitor_teams": True,
                "teams_channels": [],  # Empty means monitor all accessible
                "outlook_folders": ["Inbox"],
                "max_messages_per_check": 50,
                "headless": True,
                "save_screenshots": False
            }
            CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(CONFIG_FILE, 'w') as f:
                json.dump(default_config, f, indent=2)
            print(f"✓ Created default config at {CONFIG_FILE}")
            return default_config

    def get(self, key, default=None):
        return self.config.get(key, default)


class StateManager:
    """Track which messages have been processed"""

    def __init__(self):
        self.state = self._load_state()

    def _load_state(self):
        """Load state from file"""
        if STATE_FILE.exists():
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        return {
            "last_check": None,
            "processed_teams_messages": [],
            "processed_outlook_emails": [],
            "session_authenticated": False
        }

    def save(self):
        """Save state to file"""
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(STATE_FILE, 'w') as f:
            json.dump(self.state, f, indent=2)

    def is_processed(self, message_type, message_id):
        """Check if a message has been processed"""
        key = f"processed_{message_type}_messages"
        return message_id in self.state.get(key, [])

    def mark_processed(self, message_type, message_id):
        """Mark a message as processed"""
        key = f"processed_{message_type}_messages"
        if key not in self.state:
            self.state[key] = []

        if message_id not in self.state[key]:
            self.state[key].append(message_id)

            # Keep only last 1000 IDs to prevent unbounded growth
            if len(self.state[key]) > 1000:
                self.state[key] = self.state[key][-1000:]

    def update_last_check(self):
        """Update the last check timestamp"""
        self.state["last_check"] = datetime.utcnow().isoformat()


class TeamsMonitor:
    """Monitor Microsoft Teams for new messages"""

    def __init__(self, page, config, state):
        self.page = page
        self.config = config
        self.state = state
        self.base_url = "https://teams.microsoft.com"

    async def navigate(self):
        """Navigate to Teams"""
        print("📱 Navigating to Teams...")
        # Use 'load' instead of 'networkidle' since Teams has continuous background activity
        await self.page.goto(self.base_url, wait_until="load", timeout=60000)
        await asyncio.sleep(8)  # Let Teams fully load and render

    async def check_authentication(self):
        """Check if already authenticated"""
        try:
            print(f"  → Waiting for Teams to load (URL: {self.page.url})")

            # Try multiple selectors
            selectors_to_try = [
                'tree',  # Chat tree
                '[role="main"]',  # Main content
                'button[aria-label*="Chat"]',  # Chat button
                '[class*="app-bar"]',  # App bar
            ]

            for selector in selectors_to_try:
                try:
                    await self.page.wait_for_selector(selector, timeout=10000)
                    print(f"  ✓ Found element: {selector}")
                    return True
                except PlaywrightTimeout:
                    continue

            print("  ⚠ Could not find Teams elements - trying anyway")
            return True  # Don't fail, just proceed

        except Exception as e:
            print(f"  ⚠ Error checking Teams: {e}")
            return True  # Don't fail, just proceed

    async def get_recent_messages(self):
        """Extract recent messages from Teams"""
        messages = []

        try:
            print("  → Checking Teams chat list...")

            # Wait longer for Teams to fully render
            await asyncio.sleep(8)

            # Try multiple selectors to find the chat list
            chat_list_found = False
            selectors_to_try = [
                ('tree', 'Chat tree'),
                ('[role="tree"]', 'Tree role'),
                ('[role="navigation"]', 'Navigation'),
                ('[aria-label*="Chat"]', 'Chat aria-label'),
                ('[aria-label*="chat"]', 'Chat aria-label lowercase'),
                ('[data-tid*="chat"]', 'Chat data-tid'),
                ('ul[role="list"]', 'List role'),
                ('[class*="chat-list"]', 'Chat list class'),
                ('[class*="rail"]', 'Rail class'),
            ]

            print("  → Trying to find chat list with multiple selectors...")
            for selector, name in selectors_to_try:
                try:
                    element = await self.page.wait_for_selector(selector, timeout=5000)
                    if element:
                        print(f"  ✓ Found chat list using: {name} ({selector})")
                        chat_list_found = True
                        break
                except PlaywrightTimeout:
                    continue

            if not chat_list_found:
                print("  ⚠ Could not find chat list with any selector - trying to proceed anyway")

            # Try multiple approaches to find chat items
            await asyncio.sleep(2)

            # Try to find unread chats or any chats
            chat_items = []
            chat_selectors = [
                ('treeitem:has-text("Unread")', 'Unread tree items'),
                ('[role="treeitem"]', 'Any tree items'),
                ('li[role="treeitem"]', 'List tree items'),
                ('[aria-label*="unread"]', 'Unread aria-label'),
                ('li[role="option"]', 'List options'),
                ('[role="listitem"]', 'List items'),
            ]

            for selector, name in chat_selectors:
                try:
                    elements = await self.page.query_selector_all(selector)
                    if elements and len(elements) > 0:
                        chat_items = elements
                        print(f"  ✓ Found {len(chat_items)} chat items using: {name}")
                        break
                except Exception:
                    continue

            if not chat_items:
                print("  ⚠ No chat items found with any selector")
                return messages

            # Try to click on the first chat item to open it
            try:
                await chat_items[0].click()
                await asyncio.sleep(3)  # Let messages load
                print("  ✓ Clicked on first chat item")

                # Try multiple approaches to find message groups
                message_groups = []
                message_selectors = [
                    ('group:has(heading[level="4"])', 'Group with heading'),
                    ('[role="group"]', 'Role group'),
                    ('[class*="message"]', 'Message class'),
                    ('div[data-tid*="message"]', 'Message data-tid'),
                ]

                for selector, name in message_selectors:
                    try:
                        elements = await self.page.query_selector_all(selector)
                        if elements and len(elements) > 0:
                            message_groups = elements
                            print(f"  ✓ Found {len(message_groups)} message groups using: {name}")
                            break
                    except Exception:
                        continue

                if message_groups:
                    for group in message_groups[:self.config.get('max_messages_per_check', 20)]:
                        try:
                            message_data = await self._extract_message_from_group(group)
                            if message_data and not self.state.is_processed('teams', message_data['id']):
                                messages.append(message_data)
                        except Exception as e:
                            print(f"    ⚠ Error extracting message: {e}")
                            continue

            except Exception as e:
                print(f"  ⚠ Error opening chat: {e}")

            print(f"  → Extracted {len(messages)} new messages")

        except Exception as e:
            print(f"  ✗ Error getting Teams messages: {e}")

        return messages

    async def _extract_message_from_group(self, group):
        """Extract message data from a message group"""
        try:
            # Get all text content from the group
            full_text = await group.text_content()
            if not full_text or not full_text.strip():
                return None

            # Try multiple approaches to find sender
            sender = "Unknown"
            sender_selectors = [
                '[data-tid="message-author"]',
                '[class*="author"]',
                '[class*="sender"]',
                'h3',
                'h4',
                '[role="heading"]',
            ]

            for selector in sender_selectors:
                try:
                    sender_elem = await group.query_selector(selector)
                    if sender_elem:
                        sender_text = await sender_elem.text_content()
                        if sender_text and sender_text.strip():
                            sender = sender_text.strip()
                            break
                except Exception:
                    continue

            # Try to find timestamp
            timestamp = "Unknown"
            time_selectors = [
                'time',
                '[data-tid*="time"]',
                '[class*="time"]',
                '[class*="timestamp"]',
            ]

            for selector in time_selectors:
                try:
                    time_elem = await group.query_selector(selector)
                    if time_elem:
                        time_text = await time_elem.text_content()
                        if time_text and time_text.strip():
                            timestamp = time_text.strip()
                            break
                except Exception:
                    continue

            # Try to find message content
            message_content = ""
            content_selectors = [
                '[data-tid="message-body"]',
                '[class*="message-body"]',
                '[class*="message-content"]',
                'p',
                'div[class*="content"]',
            ]

            for selector in content_selectors:
                try:
                    content_elems = await group.query_selector_all(selector)
                    if content_elems:
                        for elem in content_elems:
                            text = await elem.text_content()
                            if text and text.strip():
                                message_content += text.strip() + " "
                        if message_content.strip():
                            break
                except Exception:
                    continue

            # If we couldn't find specific content, use all text
            if not message_content.strip():
                message_content = full_text.strip()

            # Generate ID based on content and timestamp
            message_id = f"teams_{abs(hash(message_content[:100] + timestamp))}_{int(datetime.utcnow().timestamp())}"

            message_data = {
                "id": message_id,
                "sender": sender,
                "content": message_content.strip()[:500],  # Limit content length
                "timestamp": timestamp,
                "source": "teams",
                "captured_at": datetime.utcnow().isoformat()
            }

            print(f"    ✓ Extracted: {sender[:30]}... - {message_content[:50]}...")
            return message_data

        except Exception as e:
            print(f"    ⚠ Error extracting message from group: {e}")
            return None


class OutlookMonitor:
    """Monitor Outlook for new emails"""

    def __init__(self, page, config, state):
        self.page = page
        self.config = config
        self.state = state
        self.base_url = "https://outlook.office.com/mail"

    async def navigate(self):
        """Navigate to Outlook"""
        print("📧 Navigating to Outlook...")
        # Use 'load' instead of 'networkidle' since Outlook has continuous background activity
        await self.page.goto(self.base_url, wait_until="load", timeout=60000)
        await asyncio.sleep(8)  # Let Outlook fully load and render

    async def check_authentication(self):
        """Check if already authenticated"""
        try:
            # Wait longer and check for multiple possible indicators
            # Outlook can take a while to fully render
            print(f"  → Waiting for Outlook to load (URL: {self.page.url})")

            # Try multiple selectors with retries
            selectors_to_try = [
                'listbox',  # Main message list
                '[role="main"]',  # Main content area
                '[aria-label*="Message list"]',  # Message list by aria-label
                'div[class*="message"]',  # Any message-related divs
            ]

            for selector in selectors_to_try:
                try:
                    await self.page.wait_for_selector(selector, timeout=10000)
                    print(f"  ✓ Found element: {selector}")
                    return True
                except PlaywrightTimeout:
                    continue

            print("  ⚠ Could not find Outlook elements - trying anyway")
            return True  # Don't fail, just proceed

        except Exception as e:
            print(f"  ⚠ Error checking Outlook: {e}")
            return True  # Don't fail, just proceed

    async def get_recent_emails(self):
        """Extract recent emails from Outlook inbox"""
        emails = []

        try:
            print("  → Checking Outlook inbox...")
            print(f"  → Current URL: {self.page.url}")

            # Wait longer for the page to fully render
            await asyncio.sleep(8)

            # Try to find email list with multiple selectors
            email_options = []

            # Try different selectors to find emails
            selectors = [
                'option[role="option"]',  # Standard option elements
                '[role="listitem"]',  # List items
                '[data-convid]',  # Emails with conversation IDs
            ]

            for selector in selectors:
                try:
                    elements = await self.page.query_selector_all(selector)
                    if elements and len(elements) > 0:
                        email_options = elements
                        print(f"  ✓ Found {len(elements)} items using selector: {selector}")
                        break
                except Exception as e:
                    continue

            if not email_options:
                print("  ⚠ No email elements found with any selector")
                return emails

            # Process the first few emails
            for option in email_options[:self.config.get('max_messages_per_check', 10)]:
                try:
                    email_data = await self._extract_email_from_option(option, folder="inbox")

                    if email_data and not self.state.is_processed('outlook', email_data['id']):
                        emails.append(email_data)
                        print(f"  ✓ Captured: {email_data['subject'][:50]}...")

                except Exception as e:
                    print(f"    ⚠ Error extracting email: {e}")
                    continue

            print(f"  → Extracted {len(emails)} new inbox emails")

        except Exception as e:
            print(f"  ✗ Error getting Outlook emails: {e}")

        return emails

    async def get_sent_emails(self):
        """Extract recent sent emails from Outlook"""
        sent_emails = []

        try:
            print("  → Navigating to Sent Items...")

            # Navigate to sent items folder
            sent_url = "https://outlook.office.com/mail/sentitems"
            await self.page.goto(sent_url, wait_until="load", timeout=60000)
            await asyncio.sleep(8)  # Let folder load

            print(f"  → Current URL: {self.page.url}")

            # Try to find email list with multiple selectors (same as inbox)
            email_options = []

            selectors = [
                'option[role="option"]',
                '[role="listitem"]',
                '[data-convid]',
            ]

            for selector in selectors:
                try:
                    elements = await self.page.query_selector_all(selector)
                    if elements and len(elements) > 0:
                        email_options = elements
                        print(f"  ✓ Found {len(elements)} sent items using selector: {selector}")
                        break
                except Exception as e:
                    continue

            if not email_options:
                print("  ⚠ No sent email elements found")
                return sent_emails

            # Process the first few sent emails
            for option in email_options[:self.config.get('max_messages_per_check', 10)]:
                try:
                    email_data = await self._extract_email_from_option(option, folder="sent")

                    if email_data and not self.state.is_processed('outlook-sent', email_data['id']):
                        sent_emails.append(email_data)
                        print(f"  ✓ Captured sent: {email_data['subject'][:50]}...")

                except Exception as e:
                    print(f"    ⚠ Error extracting sent email: {e}")
                    continue

            print(f"  → Extracted {len(sent_emails)} new sent emails")

        except Exception as e:
            print(f"  ✗ Error getting sent emails: {e}")

        return sent_emails

    async def _extract_email_from_option(self, option, folder="inbox"):
        """Extract email data from an email option element"""
        try:
            # Get the full text content first
            full_text = await option.inner_text()

            # Look for generic elements that contain the structured data
            generics = await option.query_selector_all('generic')

            sender = "Unknown"
            subject = "No subject"
            preview = ""
            timestamp = "Unknown"

            # Try to extract sender and subject from the structure
            # The structure is: option > group > generic (layers)
            # Sender and subject are in specific generic elements
            for i, gen in enumerate(generics):
                text = await gen.inner_text()
                text = text.strip()

                # Skip empty or very short texts
                if len(text) < 2:
                    continue

                # First meaningful text is usually sender/recipient
                if sender == "Unknown" and text and not text.startswith("Unread") and not text.startswith("External"):
                    sender = text
                # Next meaningful longer text is usually subject
                elif subject == "No subject" and len(text) > len(sender):
                    subject = text
                # Even longer text might be preview
                elif len(text) > len(subject) and len(text) > 20:
                    preview = text
                    break

            # Try to get timestamp
            time_elements = await option.query_selector_all('generic')
            for elem in time_elements:
                text = await elem.inner_text()
                # Look for time patterns (AM/PM, dates, etc.)
                if any(x in text for x in ['AM', 'PM', ':', '/']):
                    timestamp = text.strip()
                    break

            # Generate unique ID with microsecond precision to avoid collisions
            import time
            unique_timestamp = f"{int(datetime.utcnow().timestamp())}_{int(time.time() * 1000000) % 1000000}"
            email_id = f"outlook_{folder}_{abs(hash(subject + sender + timestamp))}_{unique_timestamp}"

            # If we couldn't extract proper data, use the aria-label as fallback
            if subject == "No subject" and sender == "Unknown":
                aria_label = await option.get_attribute('aria-label')
                if aria_label:
                    # Parse aria-label which contains all info
                    parts = aria_label.split()
                    if len(parts) > 2:
                        sender = parts[0] if parts[0] not in ["Unread", "Collapsed"] else parts[1]
                        # Subject is usually after sender
                        subject_start = 2 if parts[0] not in ["Unread", "Collapsed"] else 3
                        subject = " ".join(parts[subject_start:min(subject_start + 10, len(parts))])

            return {
                "id": email_id,
                "subject": subject[:200],  # Limit length
                "from": sender if folder == "inbox" else "Me",
                "to": sender if folder == "sent" else "Unknown",
                "preview": preview[:300] if preview else full_text[:300],
                "timestamp": timestamp,
                "source": "outlook",
                "folder": folder,
                "captured_at": datetime.utcnow().isoformat()
            }

        except Exception as e:
            return None


class ClientMonitor:
    """Main monitoring orchestrator"""

    def __init__(self, config, state, headless=True):
        self.config = config
        self.state = state
        self.headless = headless
        self.browser = None
        self.context = None
        self.page = None

    async def initialize(self):
        """Initialize browser and context"""
        print("🚀 Initializing browser...")

        playwright = await async_playwright().start()

        # Launch browser with settings to avoid detection
        self.browser = await playwright.chromium.launch(
            headless=self.headless,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
            ]
        )

        # Create persistent context to save authentication
        SESSION_DIR.mkdir(parents=True, exist_ok=True)

        self.context = await self.browser.new_context(
            storage_state=str(SESSION_DIR / "auth.json") if (SESSION_DIR / "auth.json").exists() else None,
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            locale='en-US',
            timezone_id='America/New_York',
            permissions=['notifications'],
        )

        self.page = await self.context.new_page()
        print("✓ Browser initialized")

    async def authenticate(self):
        """Handle authentication if needed"""
        print("\n🔐 Checking authentication...")

        # Go directly to Outlook with v2 endpoint to bypass landing pages
        # This URL forces the web app and avoids download prompts
        outlook_url = "https://outlook.office365.com/mail/inbox"

        print(f"  → Navigating to {outlook_url}")
        await self.page.goto(outlook_url, wait_until="domcontentloaded", timeout=60000)
        await asyncio.sleep(5)

        # Check current URL
        current_url = self.page.url
        print(f"  → Current URL: {current_url}")

        if "login.microsoftonline.com" in current_url or "login.live.com" in current_url:
            print("\n⚠️  Authentication required!")
            print("=" * 60)
            print("Please complete the full login process:")
            print("  1. Enter your Microsoft 365 username")
            print("  2. Enter your password")
            print("  3. Complete 2FA authentication")
            print("  4. Wait for Outlook to fully load")
            print("")
            print("The script will wait up to 10 minutes for you.")
            print("=" * 60)

            # Wait for successful login (redirected to Outlook)
            try:
                # Use wait_for_url instead of wait_for_function to avoid CSP issues
                await self.page.wait_for_url("**/outlook.office*/mail/**", timeout=600000)  # 10 minutes
                print("\n✓ Authentication successful!")

                # Wait a bit more for Outlook to fully load after redirect
                print("⏳ Waiting for Outlook to fully load...")
                await asyncio.sleep(10)

                # Save authentication state
                await self.context.storage_state(path=str(SESSION_DIR / "auth.json"))
                print("✓ Session saved for future runs")

            except PlaywrightTimeout:
                print("✗ Authentication timed out after 10 minutes")
                return False
        else:
            print("✓ Already authenticated")

        return True

    async def run_monitoring_cycle(self):
        """Run one complete monitoring cycle"""
        print(f"\n{'=' * 60}")
        print(f"🔄 Starting monitoring cycle at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'=' * 60}")

        all_new_items = []

        # Monitor Teams
        if self.config.get('monitor_teams', True):
            teams_monitor = TeamsMonitor(self.page, self.config, self.state)
            await teams_monitor.navigate()

            if await teams_monitor.check_authentication():
                messages = await teams_monitor.get_recent_messages()
                all_new_items.extend(messages)

                for msg in messages:
                    self.state.mark_processed('teams', msg['id'])
            else:
                print("  ⚠ Teams authentication check failed")

        # Monitor Outlook
        if self.config.get('monitor_outlook', True):
            outlook_monitor = OutlookMonitor(self.page, self.config, self.state)
            await outlook_monitor.navigate()

            if await outlook_monitor.check_authentication():
                # Get inbox emails
                emails = await outlook_monitor.get_recent_emails()
                all_new_items.extend(emails)

                for email in emails:
                    self.state.mark_processed('outlook', email['id'])

                # Get sent emails
                sent_emails = await outlook_monitor.get_sent_emails()
                all_new_items.extend(sent_emails)

                for sent_email in sent_emails:
                    self.state.mark_processed('outlook-sent', sent_email['id'])
            else:
                print("  ⚠ Outlook authentication check failed")

        # Save new items
        if all_new_items:
            self._save_items(all_new_items)
            print(f"\n✓ Captured {len(all_new_items)} new items")
        else:
            print("\n  ℹ No new items found")

        # Update state
        self.state.update_last_check()
        self.state.save()

        print(f"{'=' * 60}\n")

    def _save_items(self, items):
        """Save captured items to files"""
        DATA_DIR.mkdir(parents=True, exist_ok=True)

        for item in items:
            source = item.get('source', 'unknown')
            folder = item.get('folder', None)
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            item_id = item['id'].replace('/', '_').replace('\\', '_')

            # Determine directory based on source and folder
            if source == "outlook" and folder == "sent":
                dir_name = "outlook-sent"
            else:
                dir_name = source

            filename = f"{source}_{timestamp}_{item_id}.json"
            filepath = DATA_DIR / dir_name / filename
            filepath.parent.mkdir(parents=True, exist_ok=True)

            with open(filepath, 'w') as f:
                json.dump(item, f, indent=2)

    async def cleanup(self, keep_open=False):
        """Clean up browser resources"""
        if keep_open:
            print("\n" + "=" * 60)
            print("Browser will stay open for 60 seconds for inspection.")
            print("You can see what pages are loaded and what's on them.")
            print("The browser will close automatically after 60 seconds.")
            print("=" * 60)
            await asyncio.sleep(60)  # Keep open for 60 seconds

        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()


async def monitor_once(headless=True):
    """Run monitoring cycle once"""
    config = MonitorConfig()
    state = StateManager()

    monitor = ClientMonitor(config, state, headless=headless)

    try:
        await monitor.initialize()

        # Authenticate if first run
        if not state.state.get('session_authenticated', False):
            if await monitor.authenticate():
                state.state['session_authenticated'] = True
                state.save()
            else:
                print("✗ Authentication failed, exiting")
                return

        # Run monitoring cycle
        await monitor.run_monitoring_cycle()

    finally:
        # Keep browser open when not in headless mode (for debugging)
        await monitor.cleanup(keep_open=not headless)


async def monitor_continuous(headless=True):
    """Run monitoring continuously"""
    config = MonitorConfig()
    interval = config.get('check_interval_seconds', 180)

    print(f"🔄 Starting continuous monitoring (checking every {interval} seconds)")
    print(f"   Press Ctrl+C to stop\n")

    while True:
        try:
            await monitor_once(headless=headless)
            print(f"⏰ Waiting {interval} seconds until next check...")
            await asyncio.sleep(interval)

        except KeyboardInterrupt:
            print("\n\n✓ Monitoring stopped by user")
            break
        except Exception as e:
            print(f"\n✗ Error in monitoring cycle: {e}")
            print(f"   Retrying in {interval} seconds...")
            await asyncio.sleep(interval)


def main():
    parser = argparse.ArgumentParser(description='Monitor Microsoft Teams and Outlook')
    parser.add_argument('--once', action='store_true', help='Run once and exit')
    parser.add_argument('--no-headless', action='store_true', help='Show browser window')
    parser.add_argument('--setup', action='store_true', help='Run initial setup and authentication')

    args = parser.parse_args()
    headless = not args.no_headless

    if args.setup:
        print("🔧 Running initial setup...")
        print("   This will open a browser for you to authenticate.")
        asyncio.run(monitor_once(headless=False))
    elif args.once:
        asyncio.run(monitor_once(headless=headless))
    else:
        asyncio.run(monitor_continuous(headless=headless))


if __name__ == "__main__":
    main()
