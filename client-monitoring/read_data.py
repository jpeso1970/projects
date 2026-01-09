#!/usr/bin/env python3
"""
Helper script to read and analyze captured monitoring data
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import argparse


DATA_DIR = Path(__file__).parent / "data"


def get_all_items():
    """Get all captured items"""
    items = []

    for json_file in DATA_DIR.rglob("*.json"):
        try:
            with open(json_file) as f:
                data = json.load(f)
                items.append(data)
        except Exception as e:
            print(f"Error reading {json_file}: {e}")

    return sorted(items, key=lambda x: x.get('captured_at', ''), reverse=True)


def get_recent_items(hours=24):
    """Get items from the last N hours"""
    cutoff = datetime.utcnow() - timedelta(hours=hours)
    items = []

    for json_file in DATA_DIR.rglob("*.json"):
        try:
            with open(json_file) as f:
                data = json.load(f)
                captured = datetime.fromisoformat(data['captured_at'].replace('Z', '+00:00'))

                if captured > cutoff:
                    items.append(data)
        except Exception as e:
            continue

    return sorted(items, key=lambda x: x['captured_at'], reverse=True)


def search_content(keyword):
    """Search for keyword in message content"""
    results = []

    for json_file in DATA_DIR.rglob("*.json"):
        try:
            with open(json_file) as f:
                data = json.load(f)

                searchable = ' '.join([
                    data.get('content', ''),
                    data.get('subject', ''),
                    data.get('preview', ''),
                    data.get('from', '')
                ]).lower()

                if keyword.lower() in searchable:
                    results.append(data)
        except Exception as e:
            continue

    return sorted(results, key=lambda x: x.get('captured_at', ''), reverse=True)


def get_stats():
    """Get statistics about captured data"""
    items = get_all_items()

    stats = {
        'total_items': len(items),
        'by_source': defaultdict(int),
        'by_date': defaultdict(int),
        'first_capture': None,
        'last_capture': None
    }

    for item in items:
        # Count by source
        source = item.get('source', 'unknown')
        stats['by_source'][source] += 1

        # Count by date
        try:
            captured = datetime.fromisoformat(item['captured_at'].replace('Z', '+00:00'))
            date_key = captured.strftime('%Y-%m-%d')
            stats['by_date'][date_key] += 1

            # Track first and last
            if not stats['first_capture'] or captured < stats['first_capture']:
                stats['first_capture'] = captured
            if not stats['last_capture'] or captured > stats['last_capture']:
                stats['last_capture'] = captured
        except:
            continue

    return stats


def print_item(item, index=None):
    """Pretty print a single item"""
    prefix = f"[{index}] " if index is not None else ""
    source_emoji = "📧" if item['source'] == 'outlook' else "📱"

    print(f"\n{prefix}{source_emoji} {item['source'].upper()}")
    print("─" * 60)

    if item['source'] == 'outlook':
        print(f"From:    {item.get('from', 'Unknown')}")
        print(f"Subject: {item.get('subject', 'No subject')}")
        print(f"Preview: {item.get('preview', '')[:100]}")
    else:
        print(f"Content: {item.get('content', '')[:200]}")

    print(f"Time:    {item.get('timestamp', 'Unknown')}")
    print(f"Captured: {item.get('captured_at', 'Unknown')}")
    print(f"ID:      {item['id']}")


def main():
    parser = argparse.ArgumentParser(description='Read captured monitoring data')

    parser.add_argument('--recent', type=int, metavar='HOURS',
                        help='Show items from last N hours')
    parser.add_argument('--search', type=str, metavar='KEYWORD',
                        help='Search for keyword in messages')
    parser.add_argument('--stats', action='store_true',
                        help='Show statistics')
    parser.add_argument('--latest', type=int, metavar='N',
                        help='Show latest N items')
    parser.add_argument('--source', choices=['teams', 'outlook'],
                        help='Filter by source')
    parser.add_argument('--export', type=str, metavar='FILE',
                        help='Export results to JSON file')

    args = parser.parse_args()

    # Get items based on arguments
    if args.search:
        items = search_content(args.search)
        print(f"\n🔍 Search results for '{args.search}':")
        print(f"   Found {len(items)} matching items\n")

    elif args.recent:
        items = get_recent_items(hours=args.recent)
        print(f"\n🕐 Items from last {args.recent} hours:")
        print(f"   Found {len(items)} items\n")

    elif args.stats:
        stats = get_stats()
        print("\n📊 Monitoring Statistics")
        print("=" * 60)
        print(f"Total items captured: {stats['total_items']}")
        print(f"\nBy source:")
        for source, count in stats['by_source'].items():
            print(f"  {source:10s}: {count:5d}")

        if stats['first_capture'] and stats['last_capture']:
            print(f"\nFirst capture: {stats['first_capture'].strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Last capture:  {stats['last_capture'].strftime('%Y-%m-%d %H:%M:%S')}")

        print(f"\nBy date:")
        for date, count in sorted(stats['by_date'].items(), reverse=True)[:7]:
            print(f"  {date}: {count:5d} items")
        print()
        return

    else:
        items = get_all_items()
        print(f"\n📦 All captured items:")
        print(f"   Total: {len(items)} items\n")

    # Filter by source if requested
    if args.source:
        items = [item for item in items if item.get('source') == args.source]
        print(f"   Filtered to {args.source}: {len(items)} items\n")

    # Limit to latest N if requested
    if args.latest:
        items = items[:args.latest]

    # Display items
    for i, item in enumerate(items, 1):
        print_item(item, index=i)

        if i >= 10 and not args.export:
            remaining = len(items) - i
            if remaining > 0:
                print(f"\n... and {remaining} more items (use --latest to show more)")
                break

    # Export if requested
    if args.export:
        with open(args.export, 'w') as f:
            json.dump(items, f, indent=2)
        print(f"\n✓ Exported {len(items)} items to {args.export}")


if __name__ == "__main__":
    if not DATA_DIR.exists():
        print("⚠️  No data directory found. Run monitor.py first to capture some data.")
        print(f"   Expected location: {DATA_DIR}")
    else:
        main()
