"""Command-line interface for PaperTrail."""

import argparse
import sys
from datetime import date
from pathlib import Path
from typing import Any

from .deadlines import pending_summary
from .models import add_item, mark_done
from .storage import StorageError, load_items, save_items


DEFAULT_DATA_PATH = Path("data/items.json")
SUMMARY_LABELS = {
    "overdue": "Overdue",
    "due soon": "Due Soon",
    "upcoming": "Upcoming",
}


def _add_data_option(parser: argparse.ArgumentParser, *, suppress_default: bool) -> None:
    kwargs: dict[str, Any] = {
        "dest": "data",
        "type": Path,
        "help": "path to the JSON data file",
    }
    if suppress_default:
        kwargs["default"] = argparse.SUPPRESS
    else:
        kwargs["default"] = DEFAULT_DATA_PATH
    parser.add_argument("--data", **kwargs)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="papertrail")
    _add_data_option(parser, suppress_default=False)
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="add a pending item")
    add_parser.add_argument("name")
    add_parser.add_argument("due_date")
    add_parser.add_argument("--next-action", default="")
    _add_data_option(add_parser, suppress_default=True)

    list_parser = subparsers.add_parser("list", help="list all items")
    _add_data_option(list_parser, suppress_default=True)

    summary_parser = subparsers.add_parser(
        "summary", help="show the pending deadline summary"
    )
    _add_data_option(summary_parser, suppress_default=True)

    done_parser = subparsers.add_parser(
        "done", help="mark an item as completed"
    )
    done_parser.add_argument("name")
    _add_data_option(done_parser, suppress_default=True)

    return parser


def _data_path(arguments: argparse.Namespace) -> Path:
    return arguments.data


def _display_item(item: dict[str, Any]) -> None:
    print(
        f"Name: {item['name']}\n"
        f"Due date: {item['due_date'].isoformat()}\n"
        f"Status: {item['status']}\n"
        f"Next action: {item['next_action']}"
    )


def _display_list(items: list[dict[str, Any]]) -> None:
    if not items:
        print("No items.")
        return
    for index, item in enumerate(items):
        if index:
            print()
        _display_item(item)


def _display_summary(summary: list[dict[str, Any]]) -> None:
    if not summary:
        print("No pending items.")
        return
    for index, item in enumerate(summary):
        if index:
            print()
        print(SUMMARY_LABELS[item["category"]])
        _display_item(item)


def _run_command(arguments: argparse.Namespace) -> None:
    path = _data_path(arguments)
    items = load_items(path)

    if arguments.command == "add":
        updated_items = add_item(
            items,
            arguments.name,
            arguments.due_date,
            arguments.next_action,
        )
        save_items(path, updated_items)
        print(f"Added: {updated_items[-1]['name']}")
    elif arguments.command == "list":
        _display_list(items)
    elif arguments.command == "summary":
        _display_summary(pending_summary(items, date.today()))
    elif arguments.command == "done":
        updated_items = mark_done(items, arguments.name)
        save_items(path, updated_items)
        print(f"Completed: {arguments.name.strip()}")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    arguments = parser.parse_args(argv)
    try:
        _run_command(arguments)
    except (ValueError, StorageError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
