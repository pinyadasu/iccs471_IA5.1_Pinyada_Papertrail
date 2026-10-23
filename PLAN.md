
# PaperTrail Implementation Plan

## Goal

Build a small command-line application that helps users track documents, deadlines, and follow-up actions.

## Proposed Design

- Use Python for the application.
- Use JSON to store items locally.
- Use `argparse` or a similarly simple approach for CLI commands.
- Use `unittest` for automated tests.
- Keep the deadline-classification logic separate from the CLI where practical.

## Proposed Implementation Steps

### Step 1 — Project Structure

Set up the Python files and test directory.

### Step 2 — Data Handling

Implement the functions needed to load, save, add, and list items.

### Step 3 — Deadline Logic

Implement deadline classification:
- Overdue : due date is before today.
- Due soon : due date is today or within the next 3 days.
- Upcoming : due date is more than 3 days away.

Completed items must not appear in the pending-item summary.

### Step 4 — Input Validation

Reject items with a missing name or an invalid date. Make sure invalid input does not create or corrupt a saved item.

### Step 5 — CLI Commands

Provide commands for adding items, listing items, viewing the deadline summary, and marking an item as completed.

### Step 6 — Automated Tests

Test normal item creation, deadline classification, invalid input, and completed-item handling.

### Step 7 — Final Verification

Run the full test suite, try a realistic end-to-end workflow, and update the README with the actual setup and usage commands.

## Plan Review

This is a proposed plan, not an approved final plan.

After reviewing Copilot's plan:
- Record which parts were accepted.
- Record any changes made and why.
- Update this file with the final approved plan before implementation begins.
