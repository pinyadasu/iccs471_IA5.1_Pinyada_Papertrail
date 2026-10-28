import unittest
from datetime import date

from papertrail.deadlines import (
    classify_deadline,
    pending_items,
    pending_summary,
    sort_by_due_date,
)


TODAY = date(2026, 10, 29)


class DeadlineClassificationTests(unittest.TestCase):
    def test_date_before_today_is_overdue(self):
        self.assertEqual(
            classify_deadline(date(2026, 10, 28), TODAY),
            "overdue",
        )

    def test_today_is_due_soon(self):
        self.assertEqual(
            classify_deadline(TODAY, TODAY),
            "due soon",
        )

    def test_three_days_ahead_is_due_soon(self):
        self.assertEqual(
            classify_deadline(date(2026, 11, 1), TODAY),
            "due soon",
        )

    def test_four_days_ahead_is_upcoming(self):
        self.assertEqual(
            classify_deadline(date(2026, 11, 2), TODAY),
            "upcoming",
        )


class PendingSummaryTests(unittest.TestCase):
    def setUp(self):
        self.items = [
            {
                "name": "Upcoming document",
                "due_date": date(2026, 11, 2),
                "status": "pending",
                "next_action": "",
            },
            {
                "name": "Completed document",
                "due_date": date(2026, 10, 27),
                "status": "completed",
                "next_action": "",
            },
            {
                "name": "Overdue document",
                "due_date": date(2026, 10, 28),
                "status": "pending",
                "next_action": "",
            },
            {
                "name": "Due soon document",
                "due_date": date(2026, 11, 1),
                "status": "pending",
                "next_action": "",
            },
        ]

    def test_pending_items_excludes_completed_items(self):
        pending = pending_items(self.items)

        self.assertEqual(
            [item["name"] for item in pending],
            ["Upcoming document", "Overdue document", "Due soon document"],
        )
        self.assertEqual(self.items[1]["status"], "completed")

    def test_sort_by_due_date_returns_ascending_order(self):
        sorted_items = sort_by_due_date(pending_items(self.items))

        self.assertEqual(
            [item["name"] for item in sorted_items],
            ["Overdue document", "Due soon document", "Upcoming document"],
        )

    def test_pending_summary_filters_sorts_and_classifies(self):
        summary = pending_summary(self.items, TODAY)

        self.assertEqual(
            [(item["name"], item["category"]) for item in summary],
            [
                ("Overdue document", "overdue"),
                ("Due soon document", "due soon"),
                ("Upcoming document", "upcoming"),
            ],
        )
        self.assertNotIn("category", self.items[0])

    def test_pending_summary_does_not_mutate_source_list(self):
        original_items = [dict(item) for item in self.items]

        pending_summary(self.items, TODAY)

        self.assertEqual(self.items, original_items)


if __name__ == "__main__":
    unittest.main()
