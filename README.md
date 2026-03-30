# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smarter Scheduling

The scheduler in `pawpal_system.py` considers constraints at three levels:

- **Conflict detection** — tasks with overlapping time windows are flagged before being added, preventing double-booking across all pets.
- **Priority-first ordering** — the daily schedule sorts by `high → medium → low` priority, then by earliest deadline, then alphabetically as a tiebreaker.
- **Species and age preferences** — walk duration and frequency are derived automatically from the pet's species and age (e.g. cats skip walks; animals under 1 year get at least 4 walks/day). Feeding tasks are always generated as high-priority.
- **Efficient next-task lookup** — `get_next_task` uses `min()` instead of sorting the full list, so retrieving the top task is O(n) rather than O(n log n).

> Note: owner availability windows are stored but not yet enforced — a future improvement.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
