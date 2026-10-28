"""JSON persistence for PaperTrail items."""

import json
from os import PathLike
from pathlib import Path
from typing import Any

from .models import parse_due_date, validate_name, validate_status


class StorageError(ValueError):
    """Raised when PaperTrail data cannot be loaded or saved."""


def _validate_item(item: Any, index: int) -> dict[str, Any]:
    if not isinstance(item, dict):
        raise StorageError(f"item {index} must be an object")

    try:
        name = validate_name(item["name"])
        due_date = parse_due_date(item["due_date"])
        status = validate_status(item["status"])
    except (KeyError, TypeError, ValueError) as error:
        raise StorageError(f"item {index} is invalid: {error}") from error

    next_action = item.get("next_action", "")
    if next_action is None:
        next_action = ""
    if not isinstance(next_action, str):
        raise StorageError(f"item {index} has an invalid next_action")

    return {
        "name": name,
        "due_date": due_date,
        "status": status,
        "next_action": next_action,
    }


def _validate_items(items: Any) -> list[dict[str, Any]]:
    if not isinstance(items, list):
        raise StorageError("stored data must be a list")
    return [_validate_item(item, index) for index, item in enumerate(items)]


def load_items(path: str | PathLike[str]) -> list[dict[str, Any]]:
    """Load and validate items from a JSON file."""
    try:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    except (OSError, json.JSONDecodeError) as error:
        raise StorageError(f"could not load items from {path}: {error}") from error

    try:
        return _validate_items(data)
    except StorageError as error:
        raise StorageError(f"could not load items from {path}: {error}") from error


def save_items(
    path: str | PathLike[str], items: list[dict[str, Any]]
) -> None:
    """Validate and save items as JSON with ISO-formatted dates."""
    validated_items = _validate_items(items)
    serialized_items = [
        {
            **item,
            "due_date": item["due_date"].isoformat(),
        }
        for item in validated_items
    ]
    try:
        contents = json.dumps(
            serialized_items, indent=2, ensure_ascii=False
        ) + "\n"
    except (TypeError, ValueError) as error:
        raise StorageError(f"could not serialize items for {path}: {error}") from error

    try:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as file:
            file.write(contents)
    except OSError as error:
        raise StorageError(f"could not save items to {path}: {error}") from error
