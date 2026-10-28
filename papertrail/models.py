"""Item data and pure operations for PaperTrail."""

from datetime import date
from typing import Any


def validate_name(name: Any) -> str:
    """Return a trimmed item name or raise ValueError."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("name is required")
    return name.strip()


def parse_due_date(value: Any) -> date:
    """Parse an ISO date in YYYY-MM-DD format."""
    if isinstance(value, date):
        return value
    if not isinstance(value, str):
        raise ValueError("due_date must be an ISO date in YYYY-MM-DD format")
    try:
        parsed = date.fromisoformat(value)
    except ValueError as error:
        raise ValueError(
            "due_date must be an ISO date in YYYY-MM-DD format"
        ) from error
    if parsed.isoformat() != value:
        raise ValueError("due_date must be an ISO date in YYYY-MM-DD format")
    return parsed


def validate_status(status: Any) -> str:
    """Return a supported item status or raise ValueError."""
    if status not in {"pending", "completed"}:
        raise ValueError("status must be 'pending' or 'completed'")
    return status


def add_item(
    items: list[dict[str, Any]],
    name: Any,
    due_date: Any,
    next_action: Any = "",
) -> list[dict[str, Any]]:
    """Return a new list with one validated pending item added."""
    validated_name = validate_name(name)
    validated_due_date = parse_due_date(due_date)
    if next_action is None:
        next_action = ""
    if not isinstance(next_action, str):
        raise ValueError("next_action must be a string")

    updated_items = [dict(item) for item in items]
    updated_items.append(
        {
            "name": validated_name,
            "due_date": validated_due_date,
            "status": "pending",
            "next_action": next_action,
        }
    )
    return updated_items


def mark_done(
    items: list[dict[str, Any]], name: Any
) -> list[dict[str, Any]]:
    """Return a new list with one uniquely matched item marked completed."""
    requested_name = validate_name(name).casefold()
    matching_indexes = [
        index
        for index, item in enumerate(items)
        if validate_name(item.get("name")).casefold() == requested_name
    ]

    if not matching_indexes:
        raise ValueError(f"no item named {name!r} was found")
    if len(matching_indexes) > 1:
        raise ValueError(f"more than one item named {name!r} was found")

    updated_items = [dict(item) for item in items]
    updated_items[matching_indexes[0]]["status"] = "completed"
    return updated_items
