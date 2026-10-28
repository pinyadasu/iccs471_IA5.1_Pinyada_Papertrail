# Implementation plan

> This file records my project-specific steps reviewed before coding. Refer to R1–R3 rather than copying the requirements here.

## Steps

1. Create `papertrail/models.py` with item fields, validation for a required name and a valid ISO date (YYYY-MM-DD), an optional next action, and the pure functions `add_item` and `mark_done`. Both return a new list and never mutate the original. `mark_done` matches names case-insensitively, rejects no-match or multiple-match cases without changing data, and accepts an already completed item. Check with `tests/test_validation.py`. 
**Covers: R1, R3.**

2. Create `papertrail/deadlines.py` with `classify_deadline(due_date, today)` and a sorted pending summary that skips completed items. Check fixed-date boundaries for overdue, today, +3 days, and +4 days in `tests/test_deadlines.py`. 
**Covers: R2, R3.**

3. Create `papertrail/storage.py` with `load_items(path)` and `save_items(path, items)`. A corrupted file raises a clear error and is never overwritten; check with temporary files in `tests/test_storage.py`. 
**Covers: R1, R3.**

4. Create `papertrail/cli.py` with commands to add, list, show the pending summary, and mark an item done. It only reads input, calls the other modules, and displays results or errors. Check manually, including invalid input.
**Covers: R1, R2, R3.**

5. Turn C1 and C2 from `EVIDENCE.md` into automated tests and run `python -m unittest discover -s tests -v`. Then perform a realistic run by adding two documents, marking one done, and checking summary order and exclusion.
**Covers: R1, R2, R3.**

## Later changes, if any

Added a `done` command so completed items can be created, and updated the R1 wording to mention it.