"""Deadline classification and pending-item summaries."""

from datetime import date
from typing import Any


def classify_deadline(due_date: date, today: date) -> str:
    """Classify a due date relative to an explicitly supplied date."""
    days_until_due = (due_date - today).days
    if days_until_due < 0:
        return "overdue"
    if days_until_due <= 3:
        return "due soon"
    return "upcoming"


def pending_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return pending items without changing the supplied list."""
    return [item for item in items if item.get("status") == "pending"]


def sort_by_due_date(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return items in ascending due-date order."""
    return sorted(items, key=lambda item: item["due_date"])


def pending_summary(
    items: list[dict[str, Any]], today: date
) -> list[dict[str, Any]]:
    """Return sorted pending items with their deadline classifications."""
    summary = []
    for item in sort_by_due_date(pending_items(items)):
        summary_item = dict(item)
        summary_item["category"] = classify_deadline(item["due_date"], today)
        summary.append(summary_item)
    return summary
