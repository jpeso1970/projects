#!/usr/bin/env python3
"""
Check for urgent messages and cross-reference with sent items
to identify which items need action vs already replied to
"""

import json
import glob
import os
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

DATA_DIR = Path(__file__).parent / "data"

# LLM-based matching flag
USE_LLM_MATCHING = os.environ.get('USE_LLM_MATCHING', 'false').lower() == 'true'

URGENT_KEYWORDS = [
    'urgent', 'asap', 'immediate', 'priority', 'critical',
    'budget', 'deadline', 'action required', 'approval', 'sign',
    'reminder', 'please', 'needed', 'required', 'request'
]


def llm_check_reply_match(inbox_msg, sent_messages):
    """
    Use LLM to intelligently determine if any sent message is a reply to the inbox message.
    Returns True if a reply is found, False otherwise.
    """
    try:
        import anthropic

        client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

        # Prepare context
        inbox_context = f"""
FROM: {inbox_msg.get('from', 'Unknown')}
SUBJECT: {inbox_msg.get('subject', 'No subject')}
PREVIEW: {inbox_msg.get('preview', '')[:300]}
"""

        sent_context = "\n\n".join([
            f"SENT TO: {msg.get('to', 'Unknown')}\nSUBJECT: {msg.get('subject', '')}\nPREVIEW: {msg.get('preview', '')[:200]}"
            for msg in sent_messages  # Check all sent messages in time window
        ])

        prompt = f"""You are analyzing email correspondence to determine if a received message has been replied to.

RECEIVED MESSAGE:
{inbox_context}

RECENT SENT MESSAGES:
{sent_context}

Question: Did the user reply to or acknowledge the received message above? A reply includes:
- Directly responding to the sender
- Forwarding to someone else to handle
- Addressing the topic/request mentioned
- Providing clarification about who should take action
- Delegating the task to someone else
- Any communication with the sender about the same topic/request

Answer with ONLY "YES" if there's a reply/acknowledgment about this message, or "NO" if there's no communication about it."""

        message = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=10,
            temperature=0,
            messages=[{"role": "user", "content": prompt}]
        )

        response = message.content[0].text.strip().upper()
        return response.startswith("YES")

    except Exception as e:
        # Fall back to simple matching if LLM fails
        print(f"  ⚠ LLM matching failed: {e}, using fallback")
        return False


def normalize_subject(subject):
    """Normalize subject for comparison (remove RE:, FW:, etc.)"""
    subject = subject.lower().strip()

    # Remove common metadata prefixes and flags
    metadata_terms = [
        'has attachments', 'flagged', 'replied', 'forwarded', '[draft]',
        'pinned', 'external sender', 'sender', 'external', 'collapsed',
        're:', 'fw:', 'fwd:', 'attachments', 'mentioned'
    ]

    for term in metadata_terms:
        subject = subject.replace(term, ' ')

    # Clean up multiple spaces
    subject = ' '.join(subject.split())

    return subject.strip()


def extract_core_subject(subject):
    """Extract the core subject by removing metadata"""
    # Remove everything before the actual subject in complex subjects
    parts = subject.split('\n')
    if len(parts) > 1:
        # Often the real subject is after markers or in later lines
        for part in parts:
            if len(part) > 10:  # Likely the real subject
                return normalize_subject(part)

    return normalize_subject(subject)


def check_urgent_items(hours=24):
    """
    Check for urgent items in the last N hours
    Returns dict of urgent items with reply status
    """
    cutoff = datetime.utcnow() - timedelta(hours=hours)

    urgent_items = []
    sent_messages = []  # Full message data for LLM matching
    sent_subjects = []  # For fallback matching

    # Collect all sent messages
    print(f"📤 Scanning sent messages...")
    sent_dir = DATA_DIR / "outlook-sent"
    if sent_dir.exists():
        for file_path in sorted(sent_dir.glob("*.json"), reverse=True):
            try:
                with open(file_path) as f:
                    data = json.load(f)

                    captured = datetime.fromisoformat(data['captured_at'])
                    if captured > cutoff:
                        sent_messages.append(data)  # Store full message for LLM
                        subject = extract_core_subject(data.get('subject', ''))
                        if subject:
                            sent_subjects.append(subject)
            except Exception as e:
                print(f"  ⚠ Error reading {file_path.name}: {e}")

    print(f"  ✓ Found {len(sent_messages)} sent messages in last {hours} hours")

    # Now scan inbox for urgent items
    print(f"\n📥 Scanning inbox for urgent messages...")
    inbox_dir = DATA_DIR / "outlook"

    if not inbox_dir.exists():
        print("  ⚠ No inbox data found")
        return []

    for file_path in sorted(inbox_dir.glob("*.json"), reverse=True):
        try:
            with open(file_path) as f:
                data = json.load(f)

                captured = datetime.fromisoformat(data['captured_at'])
                if captured > cutoff:
                    subject = data.get('subject', '').lower()
                    preview = data.get('preview', '').lower()
                    sender = data.get('from', 'Unknown')

                    # Check for urgent indicators
                    is_urgent = any(
                        keyword in subject or keyword in preview
                        for keyword in URGENT_KEYWORDS
                    )

                    # Skip if this is a CC (informational only) - check if addressed to someone else
                    is_cced = False
                    preview_lower = preview.lower()
                    # Common patterns indicating message is for someone else
                    cc_patterns = [
                        'hi jeri', 'hello jeri', 'dear jeri',
                        'hi chris', 'hello chris', 'dear chris',
                        'hi team', 'hello team', 'dear team',
                    ]
                    for pattern in cc_patterns:
                        if preview_lower.startswith(pattern) or f'\n{pattern}' in preview_lower:
                            is_cced = True
                            break

                    if is_urgent and not is_cced:
                        # Check if we've replied to this
                        has_reply = False

                        if USE_LLM_MATCHING and sent_messages:
                            # Use LLM for intelligent semantic matching
                            has_reply = llm_check_reply_match(data, sent_messages)
                        else:
                            # Fallback: Simple subject word overlap matching
                            core_subject = extract_core_subject(data.get('subject', ''))
                            if core_subject:
                                inbox_words = set()
                                for word in core_subject.split():
                                    clean_word = ''.join(c for c in word if c.isalnum())
                                    if len(clean_word) >= 3:
                                        inbox_words.add(clean_word)

                                for sent_subj in sent_subjects:
                                    if sent_subj:
                                        sent_words = set()
                                        for word in sent_subj.split():
                                            clean_word = ''.join(c for c in word if c.isalnum())
                                            if len(clean_word) >= 3:
                                                sent_words.add(clean_word)

                                        if inbox_words and sent_words:
                                            overlap = len(inbox_words & sent_words) / len(inbox_words)
                                            if overlap >= 0.5:
                                                has_reply = True
                                                break

                        urgent_items.append({
                            'subject': data.get('subject', 'No subject')[:100],
                            'from': sender,
                            'preview': data.get('preview', '')[:150],
                            'timestamp': data.get('timestamp', 'Unknown'),
                            'captured_at': captured.strftime('%Y-%m-%d %H:%M'),
                            'has_reply': has_reply,
                            'file': file_path.name
                        })

        except Exception as e:
            print(f"  ⚠ Error reading {file_path.name}: {e}")

    print(f"  ✓ Found {len(urgent_items)} urgent messages")

    return urgent_items


def print_report(urgent_items):
    """Print a formatted report of urgent items"""
    if not urgent_items:
        print("\n✅ No urgent messages found!")
        return

    # Separate into replied and needs action
    needs_action = [item for item in urgent_items if not item['has_reply']]
    already_replied = [item for item in urgent_items if item['has_reply']]

    print(f"\n{'=' * 80}")
    print(f"URGENT MESSAGES REPORT")
    print(f"{'=' * 80}")

    if needs_action:
        print(f"\n⚠️  NEEDS ACTION ({len(needs_action)} items)")
        print(f"{'-' * 80}")

        for i, item in enumerate(needs_action, 1):
            print(f"\n{i}. FROM: {item['from']}")
            print(f"   SUBJECT: {item['subject']}")
            print(f"   TIME: {item['timestamp']} (captured: {item['captured_at']})")
            print(f"   PREVIEW: {item['preview']}...")
            print(f"   STATUS: ⚠️  NO REPLY FOUND")

    if already_replied:
        print(f"\n\n✅ ALREADY REPLIED ({len(already_replied)} items)")
        print(f"{'-' * 80}")

        for i, item in enumerate(already_replied, 1):
            print(f"\n{i}. FROM: {item['from']}")
            print(f"   SUBJECT: {item['subject']}")
            print(f"   TIME: {item['timestamp']} (captured: {item['captured_at']})")
            print(f"   STATUS: ✅ Reply found in sent items")

    print(f"\n{'=' * 80}")
    print(f"SUMMARY: {len(needs_action)} need action, {len(already_replied)} already handled")
    print(f"{'=' * 80}\n")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Check for urgent messages')
    parser.add_argument('--hours', type=int, default=24,
                       help='Check messages from last N hours (default: 24)')

    args = parser.parse_args()

    print(f"\n🔍 Checking for urgent messages in last {args.hours} hours...\n")

    urgent_items = check_urgent_items(hours=args.hours)
    print_report(urgent_items)


if __name__ == "__main__":
    main()
