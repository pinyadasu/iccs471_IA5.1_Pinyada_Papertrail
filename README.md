# PaperTrail

> This file explains who the project is for, what it should do, and how to run it.

## Purpose

PaperTrail is a command-line tool for people who need to keep track of personal documents and follow-up tasks. It helps users manage due dates, identify items that need attention, and remember their next actions.

## Requirements

- R1 : Users can add and view items with a name, due date, status, and next action, and can mark an existing item as completed.
- R2 : The program classifies pending items as overdue, due soon, or upcoming, and displays them in deadline order. Due soon means the due date is today or within the next 3 days.
- R3 : The program rejects invalid input, such as a missing name or an invalid date, and excludes completed items from the pending-item summary.

## Setup and use

- Prerequisites : Python 3.12. No external Python packages are required.
- Setup : Clone the repository. No packages to install.
- Run : From the repository root, run `python3 -m papertrail.cli add "Passport renewal" 2026-10-31 --next-action "Collect documents"`, then use `list`, `summary`, or `done "Passport renewal"`. Data is saved in `data/items.json`.
- Run tests : `python3 -m unittest discover -s tests -v`

## Author and acknowledgements

- Name / student ID : Pinyada Suthisopha-aphorn 6580511
- AI tools used : GitHub Copilot (planning and implementation), Chatgpt (reviewing drafts)
- External code/resources : [Python official documentation](https://docs.python.org/3/), used as a reference for Python development.

See PLAN.md for the implementation plan and EVIDENCE.md for results and decisions.