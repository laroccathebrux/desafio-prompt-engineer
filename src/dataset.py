"""
Bug Report Dataset for the LangSmith Prompt Optimization Challenge.

This module contains 15 sample bug reports categorized by complexity:
- 5 simple bugs: Clear, straightforward issues
- 7 medium bugs: Multiple aspects to consider
- 3 complex bugs: Edge cases, multiple systems, or unclear requirements

Each bug report follows a consistent schema with title, description,
severity, and optional fields like steps_to_reproduce.
"""

from typing import Dict, List, Any


# Simple bugs (5): Clear, single-issue reports
SIMPLE_BUGS: List[Dict[str, Any]] = [
    {
        "id": "BUG-001",
        "title": "Login button not responding on mobile",
        "description": "Users report that the login button does not respond to taps on mobile devices. The button appears but clicking it has no effect.",
        "severity": "High",
        "category": "simple",
        "steps_to_reproduce": [
            "Open the app on a mobile device",
            "Navigate to login page",
            "Tap the login button",
            "Nothing happens"
        ],
        "expected_behavior": "User should be logged in or see validation errors",
        "actual_behavior": "Button does not respond to taps"
    },
    {
        "id": "BUG-002",
        "title": "Password reset email not sent",
        "description": "When users request a password reset, the confirmation message appears but no email is received.",
        "severity": "High",
        "category": "simple",
        "steps_to_reproduce": [
            "Click 'Forgot Password'",
            "Enter email address",
            "Click 'Send Reset Link'",
            "Check email inbox"
        ],
        "expected_behavior": "User receives password reset email within 5 minutes",
        "actual_behavior": "No email received after 30 minutes"
    },
    {
        "id": "BUG-003",
        "title": "Profile picture upload fails",
        "description": "Users cannot upload profile pictures. The upload progress reaches 100% but the image never appears.",
        "severity": "Medium",
        "category": "simple",
        "steps_to_reproduce": [
            "Go to profile settings",
            "Click 'Change Photo'",
            "Select an image file",
            "Wait for upload to complete"
        ],
        "expected_behavior": "New profile picture is displayed",
        "actual_behavior": "Upload completes but old picture remains"
    },
    {
        "id": "BUG-004",
        "title": "Search results show deleted items",
        "description": "Deleted products still appear in search results, leading to 404 errors when clicked.",
        "severity": "Medium",
        "category": "simple",
        "steps_to_reproduce": [
            "Search for a product name",
            "View search results",
            "Click on a result that was recently deleted"
        ],
        "expected_behavior": "Only active products appear in search",
        "actual_behavior": "Deleted products shown, clicking leads to error page"
    },
    {
        "id": "BUG-005",
        "title": "Date picker shows wrong timezone",
        "description": "The date picker component displays dates in UTC instead of the user's local timezone.",
        "severity": "Low",
        "category": "simple",
        "steps_to_reproduce": [
            "Open any form with date picker",
            "Select a date",
            "Compare displayed time with local time"
        ],
        "expected_behavior": "Dates should show in user's local timezone",
        "actual_behavior": "Dates show in UTC, causing confusion"
    }
]

# Medium bugs (7): Multiple aspects or moderate complexity
MEDIUM_BUGS: List[Dict[str, Any]] = [
    {
        "id": "BUG-006",
        "title": "Shopping cart loses items after page refresh",
        "description": "Items added to shopping cart disappear when the page is refreshed. This only happens for guest users who are not logged in.",
        "severity": "High",
        "category": "medium",
        "steps_to_reproduce": [
            "Browse as guest user (not logged in)",
            "Add items to cart",
            "Refresh the page",
            "Check cart contents"
        ],
        "expected_behavior": "Cart items persist across page refreshes",
        "actual_behavior": "Cart is empty after refresh for guest users"
    },
    {
        "id": "BUG-007",
        "title": "Notification preferences not saving correctly",
        "description": "Users update their notification preferences but changes revert to defaults after logging out and back in. Email preferences save correctly but push notification settings do not.",
        "severity": "Medium",
        "category": "medium",
        "steps_to_reproduce": [
            "Go to notification settings",
            "Disable push notifications",
            "Save changes",
            "Log out and log back in",
            "Check notification settings"
        ],
        "expected_behavior": "All notification preferences persist",
        "actual_behavior": "Push notification settings reset to defaults"
    },
    {
        "id": "BUG-008",
        "title": "Payment fails silently with certain card types",
        "description": "Payments made with American Express cards fail without any error message. The page just reloads to the payment form. Visa and Mastercard work correctly.",
        "severity": "Critical",
        "category": "medium",
        "steps_to_reproduce": [
            "Add items to cart",
            "Proceed to checkout",
            "Enter American Express card details",
            "Click 'Pay Now'"
        ],
        "expected_behavior": "Payment processes or clear error message displayed",
        "actual_behavior": "Page reloads silently, no feedback given"
    },
    {
        "id": "BUG-009",
        "title": "Report export produces corrupted Excel files",
        "description": "When exporting reports to Excel format, files larger than 10MB become corrupted and cannot be opened. PDF export works for all sizes.",
        "severity": "Medium",
        "category": "medium",
        "steps_to_reproduce": [
            "Generate a large report (>1000 rows)",
            "Click 'Export to Excel'",
            "Download the file",
            "Try to open in Excel"
        ],
        "expected_behavior": "Excel file opens correctly",
        "actual_behavior": "Excel shows 'file is corrupted' error"
    },
    {
        "id": "BUG-010",
        "title": "Search autocomplete shows irrelevant suggestions",
        "description": "The search autocomplete suggests products from categories the user has never browsed. Suggestions seem random rather than based on user history or popular items.",
        "severity": "Low",
        "category": "medium",
        "steps_to_reproduce": [
            "Type a few characters in search box",
            "View autocomplete suggestions",
            "Compare with browsing history"
        ],
        "expected_behavior": "Suggestions based on user history and popular searches",
        "actual_behavior": "Seemingly random suggestions unrelated to user activity"
    },
    {
        "id": "BUG-011",
        "title": "Dashboard widgets overlap on tablet view",
        "description": "On tablet devices in portrait mode, dashboard widgets overlap each other making data unreadable. Landscape mode and desktop views work correctly.",
        "severity": "Medium",
        "category": "medium",
        "steps_to_reproduce": [
            "Open dashboard on tablet",
            "Rotate to portrait mode",
            "Observe widget layout"
        ],
        "expected_behavior": "Widgets stack vertically and remain readable",
        "actual_behavior": "Widgets overlap, text becomes unreadable"
    },
    {
        "id": "BUG-012",
        "title": "Two-factor authentication codes expire too quickly",
        "description": "2FA codes sent via SMS expire before users can enter them. Users report codes become invalid within 30 seconds instead of the expected 5 minutes.",
        "severity": "High",
        "category": "medium",
        "steps_to_reproduce": [
            "Enable 2FA on account",
            "Log in from new device",
            "Wait for SMS code",
            "Enter code within 1 minute"
        ],
        "expected_behavior": "Code valid for 5 minutes",
        "actual_behavior": "Code expires within 30 seconds"
    }
]

# Complex bugs (3): Edge cases, multiple systems, or unclear requirements
COMPLEX_BUGS: List[Dict[str, Any]] = [
    {
        "id": "BUG-013",
        "title": "Data sync conflicts between mobile and web cause duplicate entries",
        "description": "Users who edit data on both mobile app and web simultaneously experience data sync issues. Sometimes changes are lost, other times duplicate entries are created. The conflict resolution seems inconsistent.",
        "severity": "Critical",
        "category": "complex",
        "steps_to_reproduce": [
            "Open same account on mobile and web",
            "Edit the same record on both platforms",
            "Save changes on mobile first",
            "Save changes on web within 5 seconds",
            "Sync and check results"
        ],
        "expected_behavior": "Consistent conflict resolution with user choice or last-write-wins",
        "actual_behavior": "Unpredictable results: sometimes data lost, sometimes duplicated"
    },
    {
        "id": "BUG-014",
        "title": "Internationalization breaks currency formatting in edge cases",
        "description": "The currency formatting works for most locales but fails for certain combinations. Japanese Yen displays with decimal places (¥1,234.00 instead of ¥1,234). Swiss Franc rounds incorrectly for prices ending in .05 or .95.",
        "severity": "Medium",
        "category": "complex",
        "steps_to_reproduce": [
            "Change locale to Japanese",
            "View product prices",
            "Change locale to Swiss German",
            "View prices ending in .05 or .95"
        ],
        "expected_behavior": "Correct formatting per locale (JPY no decimals, CHF rounds to .05)",
        "actual_behavior": "JPY shows unnecessary decimals, CHF rounding errors"
    },
    {
        "id": "BUG-015",
        "title": "Batch processing fails silently after 10,000 records",
        "description": "Large batch operations appear to complete successfully but actually stop processing after exactly 10,000 records. No error is logged, progress bar reaches 100%, but remaining records are not processed. Affects imports, exports, and bulk updates.",
        "severity": "Critical",
        "category": "complex",
        "steps_to_reproduce": [
            "Prepare a batch of 15,000 records",
            "Start batch import",
            "Wait for completion",
            "Check database for all records"
        ],
        "expected_behavior": "All 15,000 records processed",
        "actual_behavior": "Only first 10,000 processed, no warning shown"
    }
]


def get_all_bugs() -> List[Dict[str, Any]]:
    """
    Get all bug reports from the dataset.

    Returns:
        List of all 15 bug report dictionaries.

    Example:
        >>> bugs = get_all_bugs()
        >>> len(bugs)
        15
    """
    return SIMPLE_BUGS + MEDIUM_BUGS + COMPLEX_BUGS


def get_bugs_by_category(category: str) -> List[Dict[str, Any]]:
    """
    Get bug reports filtered by category.

    Args:
        category: One of 'simple', 'medium', or 'complex'.

    Returns:
        List of bug reports matching the specified category.

    Raises:
        ValueError: If category is not one of the valid options.

    Example:
        >>> simple_bugs = get_bugs_by_category('simple')
        >>> len(simple_bugs)
        5
    """
    if category == 'simple':
        return SIMPLE_BUGS
    elif category == 'medium':
        return MEDIUM_BUGS
    elif category == 'complex':
        return COMPLEX_BUGS
    else:
        raise ValueError(f"Invalid category: {category}. Must be 'simple', 'medium', or 'complex'.")


def get_bug_by_id(bug_id: str) -> Dict[str, Any]:
    """
    Get a specific bug report by its ID.

    Args:
        bug_id: The bug ID (e.g., 'BUG-001').

    Returns:
        The bug report dictionary.

    Raises:
        ValueError: If no bug with the specified ID exists.

    Example:
        >>> bug = get_bug_by_id('BUG-001')
        >>> bug['title']
        'Login button not responding on mobile'
    """
    all_bugs = get_all_bugs()
    for bug in all_bugs:
        if bug['id'] == bug_id:
            return bug
    raise ValueError(f"Bug not found: {bug_id}")


def format_bug_for_prompt(bug: Dict[str, Any]) -> str:
    """
    Format a bug report as a string suitable for prompt input.

    Args:
        bug: A bug report dictionary.

    Returns:
        Formatted string representation of the bug.

    Example:
        >>> bug = get_bug_by_id('BUG-001')
        >>> formatted = format_bug_for_prompt(bug)
        >>> 'Title:' in formatted
        True
    """
    lines = [
        f"Title: {bug['title']}",
        f"Description: {bug['description']}",
        f"Severity: {bug['severity']}"
    ]

    if 'steps_to_reproduce' in bug:
        lines.append("Steps to Reproduce:")
        for i, step in enumerate(bug['steps_to_reproduce'], 1):
            lines.append(f"  {i}. {step}")

    if 'expected_behavior' in bug:
        lines.append(f"Expected Behavior: {bug['expected_behavior']}")

    if 'actual_behavior' in bug:
        lines.append(f"Actual Behavior: {bug['actual_behavior']}")

    return "\n".join(lines)


# Dataset statistics
DATASET_STATS = {
    "total": 15,
    "simple": 5,
    "medium": 7,
    "complex": 3,
    "by_severity": {
        "Critical": 3,
        "High": 5,
        "Medium": 5,
        "Low": 2
    }
}


if __name__ == "__main__":
    # Print dataset summary for verification
    print("Bug Dataset Summary")
    print("=" * 40)
    print(f"Total bugs: {len(get_all_bugs())}")
    print(f"  Simple: {len(get_bugs_by_category('simple'))}")
    print(f"  Medium: {len(get_bugs_by_category('medium'))}")
    print(f"  Complex: {len(get_bugs_by_category('complex'))}")
    print()
    print("Sample bug (formatted):")
    print("-" * 40)
    print(format_bug_for_prompt(get_bug_by_id('BUG-001')))
