# Checks and decisions

> This file records what I checked, what actually happened, and why I accepted or changed the work. It does not repeat setup instructions or the implementation plan.

## Concrete checks

These checks were written before implementation. Actual results will be recorded after testing.

| Check / requirement | Given | When | Expected result | Actual result / pass or fail |
|---|---|---|---|---|
| C1 / R1, R2 — Add an item with a valid deadline | I want to track my passport renewal, and its due date is 2 days from today. | I add the item to PaperTrail and check the deadline summary. | The item is saved successfully and appears in the Due Soon category. | [Complete after checking.] |
| C2 / R3 — Reject an item without a name | I try to add a new item but leave its name empty. | I submit the item. | PaperTrail rejects the item, displays an error message, and does not save it. | [Complete after checking.] |

[Add rows only as needed to cover R1–R3.]

## Two review decisions

- Plan decision : [What I accepted or changed, and why. One or two sentences.]
- Code decision : [File/function/component, what I accepted or changed, and why. One or two sentences.]

## Automated tests

- Test file and behaviour checked : [...]
- Command I ran : [...]
- Final result : [Actual test count and outcome.]
- Correction and rerun, if needed : [Brief account, or None needed.]

## Realistic use and final judgment

- Task I tried : [One realistic use from start to finish.]
- Outcome : [What happened and whether it served the intended user/purpose.]
- Judgment : [Done / Partly done / Not done, with a brief reason based on the evidence.]
- Remaining limitation or unfinished work : [One specific item, or a useful next check.]