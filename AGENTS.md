
# Instructions for GitHub Copilot

## Before Making Changes

- Read `README.md`, `PLAN.md`, and `EVIDENCE.md` before working.
- Follow the requirements R1, R2, and R3 in `README.md`.
- If a requirement or design decision is unclear, ask before making a major change.

## Project Scope

- Build a small Python command-line application called PaperTrail.
- Use JSON for local data storage.
- Keep the implementation simple and suitable for a small student project.
- Do not add a web interface, database server, login system, external API, or unrelated features.
- Do not add external dependencies unless necessary and approved.

## Code Quality

- Use clear function and variable names.
- Separate deadline and validation logic from command-line input/output where practical.
- Handle invalid user input without crashing.
- Keep changes small and focused.
- Avoid unnecessary abstractions and duplicated code.

## Testing

- Use Python's built-in `unittest` framework.
- Run the relevant tests after each implementation step.
- Run the full test suite before reporting the task as complete.
- Do not change expected test results just to make the implementation pass.
- Include tests for deadline classification and invalid input.

## Student Review

- Explain the purpose of important code changes.
- Identify assumptions and limitations.
- Do not decide the student's final evaluation or write personal reflections on their behalf.
- Do not change the requirements or expected results recorded by the student without asking.
- Do not claim a test passed unless it was actually run and passed.

## Final Report

After making changes, report:
- Files changed
- Features implemented
- Tests run and their actual results
- Known limitations
- Any unfinished requirements
