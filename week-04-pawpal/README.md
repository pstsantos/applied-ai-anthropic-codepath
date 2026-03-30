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

### Running the App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

### Testing PawPal+

Run the comprehensive test suite:

```bash
PYTHONPATH=. python -m pytest tests/test_pawpal.py -v
```

### Smart Rescheduling

When a task is marked complete, the system automatically:
- Logs the completion in the task history
- Prompts the user to set recurrence (daily or weekly)
- If recurrence is enabled, creates the next task instance
- Validates the new task for conflicts with other scheduled tasks
- Maintains all properties (pet, assignee, task type) across recurrences

This prevents manual re-entry of repetitive tasks while ensuring no scheduling conflicts occur.

**Test Coverage (69 tests across 5 core behaviors):**

1. **Conflict Detection (16 tests)** — Validates that the system prevents double-booking
   - Same pet at same time
   - Same assignee at same time
   - Edge cases: completed tasks, midnight boundaries, microsecond precision
   - Scales to 100+ tasks correctly

2. **Recurring Task Execution (15 tests)** — Ensures tasks recur properly
   - Daily and weekly recurrence patterns
   - New tasks inherit pet, type, assignee, and recurrence
   - Edge cases: leap years, month boundaries, invalid recurrence types
   - Tasks marked as completed before recurrence

3. **Task Filtering & Queries (13 tests)** — Tests filtering by status and pet
   - Filter by status (scheduled, completed, or both)
   - Filter by pet name (case-insensitive)
   - Edge cases: empty lists, non-existent pets, large task sets (100+ tasks)

4. **Notification Workflow (12 tests)** — Validates the ping state machine
   - State transitions: pending → sent → accepted/declined
   - Timestamps set on response
   - Edge cases: empty messages allowed, double-acceptance prevention

5. **Task Sorting (9 tests)** — Confirms correct chronological ordering
   - Single and multiple tasks
   - Already-sorted vs unsorted task lists
   - Immutability of original list after sorting
   - Edge cases: same-time tasks, microsecond differences, midnight boundaries

6. **Integration Scenarios (5 tests)** — Cross-behavior validation
   - Recurring tasks detected for conflicts
   - Filter → Sort workflow maintains order
   - Ping acceptance with task state
   - Large complex scenarios with 10+ recurring tasks

    All tests pass with 100% success rate.

### Confidence Level

**4/5** — System's reliability based on test results

**Why 4/5:**

✅ **Strengths (What's solid):**
- 69 comprehensive tests with 100% pass rate
- Core scheduling logic fully validated (conflict detection, recurring tasks, filtering, sorting)
- Edge cases covered (leap years, midnight boundaries, microsecond precision, 100+ task scale)
- State machine for notifications is robust
- Business logic is well-isolated from UI

⚠️ **What's Incomplete (Why not 5/5):**
- No persistence layer — tasks lost on page refresh (in-memory only)
- Streamlit UI not fully stress-tested (works for ~100 tasks, untested at 1000+)
- No production logging/monitoring
- Performance optimizations not implemented (all queries are O(n) scans)
- Error handling could be more graceful

**To Reach 5/5:**
1. Add database persistence (PostgreSQL, SQLite, or Firebase)
2. Implement caching for availability parsing
3. Add indexed queries for pet-based lookups
4. Deploy with monitoring and error tracking
5. Load testing with 10k+ tasks 
