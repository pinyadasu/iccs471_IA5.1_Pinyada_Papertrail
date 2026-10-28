import unittest
from datetime import date

from papertrail.models import add_item, mark_done, parse_due_date


class AddItemTests(unittest.TestCase):
    def test_add_item_returns_item_with_valid_fields(self):
        items = []

        updated = add_item(items, "Passport renewal", "2026-10-30")

        self.assertEqual(items, [])
        self.assertEqual(updated, [
            {
                "name": "Passport renewal",
                "due_date": date(2026, 10, 30),
                "status": "pending",
                "next_action": "",
            }
        ])

    def test_add_item_accepts_optional_next_action(self):
        updated = add_item(
            [],
            "Passport renewal",
            date(2026, 10, 30),
            "Collect documents",
        )

        self.assertEqual(updated[0]["next_action"], "Collect documents")

    def test_add_item_trims_name(self):
        updated = add_item([], "  Passport renewal  ", "2026-10-30")

        self.assertEqual(updated[0]["name"], "Passport renewal")

    def test_add_item_rejects_missing_name(self):
        with self.assertRaisesRegex(ValueError, "name is required"):
            add_item([], "   ", "2026-10-30")

    def test_add_item_rejects_invalid_date(self):
        with self.assertRaisesRegex(ValueError, "due_date"):
            add_item([], "Passport renewal", "2026-02-30")

    def test_add_item_does_not_mutate_existing_items(self):
        items = [
            {
                "name": "Tax filing",
                "due_date": date(2026, 11, 1),
                "status": "pending",
                "next_action": "",
            }
        ]

        updated = add_item(items, "Passport renewal", "2026-10-30")

        self.assertEqual(len(items), 1)
        self.assertEqual(len(updated), 2)
        self.assertIsNot(updated, items)


class MarkDoneTests(unittest.TestCase):
    def setUp(self):
        self.items = [
            {
                "name": "Passport renewal",
                "due_date": date(2026, 10, 30),
                "status": "pending",
                "next_action": "",
            }
        ]

    def test_mark_done_matches_trimmed_name_case_insensitively(self):
        updated = mark_done(self.items, "  PASSPORT RENEWAL ")

        self.assertEqual(updated[0]["status"], "completed")
        self.assertEqual(self.items[0]["status"], "pending")
        self.assertIsNot(updated, self.items)

    def test_mark_done_rejects_missing_match_without_mutating(self):
        with self.assertRaisesRegex(ValueError, "no item"):
            mark_done(self.items, "Unknown document")

        self.assertEqual(self.items[0]["status"], "pending")

    def test_mark_done_rejects_multiple_matches_without_mutating(self):
        duplicate_items = self.items + [dict(self.items[0])]

        with self.assertRaisesRegex(ValueError, "more than one"):
            mark_done(duplicate_items, "passport renewal")

        self.assertEqual(
            [item["status"] for item in duplicate_items],
            ["pending", "pending"],
        )

    def test_mark_done_accepts_already_completed_item(self):
        completed_items = [dict(self.items[0], status="completed")]

        updated = mark_done(completed_items, "Passport renewal")

        self.assertEqual(updated[0]["status"], "completed")
        self.assertIsNot(updated, completed_items)


class DateParsingTests(unittest.TestCase):
    def test_parse_due_date_returns_date(self):
        self.assertEqual(parse_due_date("2026-10-30"), date(2026, 10, 30))

    def test_parse_due_date_rejects_non_iso_format(self):
        with self.assertRaisesRegex(ValueError, "YYYY-MM-DD"):
            parse_due_date("30-10-2026")


if __name__ == "__main__":
    unittest.main()
