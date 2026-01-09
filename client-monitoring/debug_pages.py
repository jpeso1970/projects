#!/usr/bin/env python3
"""
Debug script to see what's actually on the Teams and Outlook pages
"""

import asyncio
from playwright.async_api import async_playwright
from pathlib import Path

SESSION_DIR = Path(__file__).parent / ".session"

async def debug_pages():
    playwright = await async_playwright().start()

    browser = await playwright.chromium.launch(headless=False)

    # Load saved session if it exists
    storage_state_path = SESSION_DIR / "auth.json"
    if storage_state_path.exists():
        context = await browser.new_context(storage_state=str(storage_state_path))
        print("✓ Loaded saved session")
    else:
        context = await browser.new_context()
        print("⚠ No saved session found")

    page = await context.new_page()

    # Test Teams
    print("\n" + "="*60)
    print("TESTING TEAMS")
    print("="*60)
    await page.goto("https://teams.microsoft.com", wait_until="networkidle", timeout=60000)
    await asyncio.sleep(5)

    print(f"Current URL: {page.url}")
    print(f"Page title: {await page.title()}")

    # Check for common elements
    elements_to_check = [
        ('tree', 'Chat tree'),
        ('button[aria-label*="Chat"]', 'Chat button'),
        ('div[data-tid]', 'Teams data elements'),
        ('[role="main"]', 'Main content area'),
        ('application', 'Application element'),
    ]

    for selector, name in elements_to_check:
        try:
            element = await page.wait_for_selector(selector, timeout=3000)
            if element:
                print(f"✓ Found: {name} ({selector})")
        except:
            print(f"✗ Not found: {name} ({selector})")

    # Test Outlook
    print("\n" + "="*60)
    print("TESTING OUTLOOK")
    print("="*60)
    await page.goto("https://outlook.office.com/mail", wait_until="networkidle", timeout=60000)
    await asyncio.sleep(5)

    print(f"Current URL: {page.url}")
    print(f"Page title: {await page.title()}")

    # Check for common elements
    elements_to_check = [
        ('listbox', 'Message listbox'),
        ('option[role="option"]', 'Email options'),
        ('[role="main"]', 'Main content area'),
        ('application', 'Application element'),
        ('button[aria-label*="Mail"]', 'Mail button'),
    ]

    for selector, name in elements_to_check:
        try:
            element = await page.wait_for_selector(selector, timeout=3000)
            if element:
                print(f"✓ Found: {name} ({selector})")
        except:
            print(f"✗ Not found: {name} ({selector})")

    print("\n" + "="*60)
    print("Press Enter to close the browser...")
    input()

    await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_pages())
