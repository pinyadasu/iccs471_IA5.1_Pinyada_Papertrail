import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from papertrail.deadlines import pending_summary
from papertrail.models import add_item, mark_done
from papertrail.storage import StorageError, load_items, save_items


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.path = Path(self.temp_dir.name) / "items.json"
        self.items = [
            {
                "name": "Passport renewal",
                "due_date": date(2026, 10, 31),
                "status": "pending",
                "next_action": "Collect documents",
            },
            {
                "name": "Tax filing",
                "due_date": date(2026, 11, 5),
                "status": "completed",
                "next_action": "",
            },
        ]

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_missing_file_returns_empty_list(self):
        self.assertEqual(load_items(self.path), [])

    def test_save_uses_iso_dates_and_load_converts_to_date(self):
        save_items(self.path, self.items)

        with self.path.open(encoding="utf-8") as file:
            stored_data = json.load(file)

        self.assertEqual(stored_data[0]["due_date"], "2026-10-31")
        self.assertEqual(load_items(self.path), self.items)
        self.assertIsInstance(load_items(self.path)[0]["due_date"], date)

    def test_c1_added_item_is_saved_and_due_soon(self):
        today = date(2026, 10, 29)
        items = add_item([], "Passport renewal", date(2026, 10, 31))

        save_items(self.path, items)
        loaded_items = load_items(self.path)
        summary = pending_summary(loaded_items, today)

        self.assertEqual(
            summary,
            [
                {
                    "name": "Passport renewal",
                    "due_date": date(2026, 10, 31),
                    "status": "pending",
                    "next_action": "",
                    "category": "due soon",
                }
            ],
        )
        self.assertEqual(loaded_items, items)

    def test_save_creates_missing_parent_directory(self):
        nested_path = Path(self.temp_dir.name) / "data" / "items.json"

        save_items(nested_path, self.items)

        self.assertTrue(nested_path.exists())
        self.assertEqual(load_items(nested_path), self.items)

    def test_thai_item_name_round_trips(self):
        thai_items = [
            {
                "name": "หนังสือเดินทาง",
                "due_date": date(2026, 10, 31),
                "status": "pending",
                "next_action": "",
            }
        ]

        save_items(self.path, thai_items)

        self.assertEqual(load_items(self.path), thai_items)
        self.assertIn("หนังสือเดินทาง", self.path.read_text(encoding="utf-8"))

    def test_loaded_missing_next_action_defaults_to_empty_string(self):
        self.path.write_text(
            json.dumps(
                [
                    {
                        "name": "Passport renewal",
                        "due_date": "2026-10-31",
                        "status": "pending",
                    }
                ]
            ),
            encoding="utf-8",
        )

        loaded = load_items(self.path)

        self.assertEqual(loaded[0]["next_action"], "")

    def test_corrupted_json_raises_clear_error(self):
        self.path.write_text("{not valid json", encoding="utf-8")

        with self.assertRaisesRegex(StorageError, "could not load items"):
            load_items(self.path)

    def test_invalid_loaded_record_raises_clear_error(self):
        self.path.write_text(
            json.dumps(
                [
                    {
                        "name": "Passport renewal",
                        "due_date": "2026-02-30",
                        "status": "pending",
                    }
                ]
            ),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(StorageError, "item 0 is invalid"):
            load_items(self.path)

    def test_invalid_status_raises_clear_error(self):
        self.path.write_text(
            json.dumps(
                [
                    {
                        "name": "Passport renewal",
                        "due_date": "2026-10-31",
                        "status": "done",
                    }
                ]
            ),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(StorageError, "status"):
            load_items(self.path)

    def test_failed_save_does_not_overwrite_existing_file(self):
        self.path.write_text("original data", encoding="utf-8")
        invalid_items = [
            {
                "name": "Passport renewal",
                "due_date": "not-a-date",
                "status": "pending",
                "next_action": "",
            }
        ]

        with self.assertRaises(StorageError):
            save_items(self.path, invalid_items)

        self.assertEqual(self.path.read_text(encoding="utf-8"), "original data")

    def test_failed_save_does_not_create_file(self):
        invalid_items = [
            {
                "name": "Passport renewal",
                "due_date": date(2026, 10, 31),
                "status": "invalid",
                "next_action": "",
            }
        ]

        with self.assertRaises(StorageError):
            save_items(self.path, invalid_items)

        self.assertFalse(self.path.exists())

    def test_failed_save_does_not_create_missing_parent_directory(self):
        nested_directory = Path(self.temp_dir.name) / "missing" / "data"
        nested_path = nested_directory / "items.json"
        invalid_items = [
            {
                "name": "Passport renewal",
                "due_date": "not-a-date",
                "status": "pending",
                "next_action": "",
            }
        ]

        with self.assertRaises(StorageError):
            save_items(nested_path, invalid_items)

        self.assertFalse(nested_directory.exists())
        self.assertFalse(nested_path.exists())

    def test_done_item_saved_and_reloaded_is_absent_from_pending_summary(self):
        items = add_item([], "Passport renewal", date(2026, 10, 31))
        completed_items = mark_done(items, "passport renewal")

        save_items(self.path, completed_items)
        loaded_items = load_items(self.path)

        self.assertEqual(loaded_items[0]["status"], "completed")
        self.assertEqual(
            pending_summary(loaded_items, date(2026, 10, 29)),
            [],
        )


if __name__ == "__main__":
    unittest.main()
