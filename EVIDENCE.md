# Checks and decisions

> This file records what I checked, what actually happened, and why I accepted or changed the work. It does not repeat setup instructions or the implementation plan.

## Concrete checks

These checks were written before implementation. Actual results will be recorded after testing.

| Check / requirement | Given | When | Expected result | Actual result / pass or fail |
|---|---|---|---|---|
| C1 / R1, R2 — Add an item with a valid deadline | I want to track my passport renewal, and its due date is 2 days from today. | I add the item to PaperTrail and check the deadline summary. | The item is saved successfully and appears in the Due Soon category. | I added `Passport renewal` with a due date 2 days after the day I ran it. The summary listed it under Due Soon. **Pass.** |
| C2 / R3 — Reject an item without a name | I try to add a new item but leave its name empty. | I submit the item. | PaperTrail rejects the item, displays an error message, and does not save it. | Output: `Error: name is required`, exit code `1`. Running `list` afterwards did not show the item. **Pass.** |
| C3 / R1, R3 — Mark an item as completed | Two pending items: `Passport renewal` (due in 2 days) and `Library book` (due in 12 days). | I run `done "passport renewal"`, then `summary` and `list`. | The summary shows only `Library book`. The full list still shows both items, with `Passport renewal` marked as completed. | The observed result matched the expected result. **Pass.** |
| C4 / R3 — Reject an invalid date | I try to add an item with the date `2026-02-30`. | I run `add "Bad date" 2026-02-30`. | The program displays an error, exits with code `1`, and does not save the item. | Output: `Error: due_date must be an ISO date in YYYY-MM-DD format`, exit code `1`. **Pass.** |
| C5 / R2 — Check deadline categories and order | Four items are due 2 days ago, today, in 3 days, and in 4 days. | I run `summary`. | Items are grouped into Overdue, Due Soon (today and within the next 3 days), and Upcoming (in 4 days), in deadline order. | The observed result matched the expected result. **Pass.** |
| C6 / R3 — Handle a corrupted data file | The data file contains `{not valid json`. | I try to add an item using that file. | The program displays a clear error, exits with code `1`, and leaves the file unchanged. | Output: `Error: could not load items...`, exit code `1`. The file content remained unchanged. **Pass.** |

## Two review decisions

- Plan decision : When I checked Copilot's first plan, I noticed that there was no way to mark an item as completed. This would make it hard to test R3, which requires completed items to be excluded from the pending summary. So, I asked Copilot to add a `done` command and update R1. I also asked it to move the add and done logic from `cli.py` to `models.py` so I could test them separately.
- Code decision : In `storage.py`, `save_items` validates the items and builds the JSON text before opening the file, which helps prevent a failed save from damaging existing data. I accepted this design but found that it did not create the `data/` directory on a fresh copy, so I asked Copilot to create the parent directory only after validation succeeds.

## Automated tests

- Test file and behaviour checked : `tests/test_validation.py` checks name and date validation, `add_item`, and `mark_done`. `tests/test_deadlines.py` checks deadline categories, boundaries, sorting, and excluding completed items. `tests/test_storage.py` checks saving and loading data, corrupted files, and failed saves. The automated tests also check the C1 and C2 cases.
- Command I ran : `python3 -m unittest discover -s tests -v`
- Final result : All 35 tests passed.
- Correction and rerun, if needed : The first version of `save_items` did not create a missing `data/` directory. I found this by reviewing the code and asked Copilot to fix it and add a test. I also noticed that the first C2 test did not call `save_items`, so it could not check whether the item was saved. I asked Copilot to update the test. After these changes, all 35 tests passed.

## Realistic use and final judgment

- Task I tried : I tracked four documents with different deadlines: 2 days overdue, due today, due in 3 days, and due in 4 days. I marked one item as completed and checked the summary and full list.
- Outcome : The summary grouped the items by deadline and displayed them in date order. The completed item no longer appeared in the summary but remained in the full list. Invalid names and dates were rejected without changing the saved data. The program was useful for tracking documents from the terminal.
- Judgment : Done. R1–R3 work as described in the checks, and all 35 automated tests passed. PaperTrail was usable for tracking a few documents from the terminal.
- Remaining limitation or unfinished work : Items with the same name cannot be distinguished when marking them as completed because the program has no unique item ID. Items also cannot be edited or deleted.