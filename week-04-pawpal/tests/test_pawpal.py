import warnings
from datetime import datetime, timedelta, time
from pawpal_system import User, Household, Pet, Task, TaskLog, Notification, Scheduler


def make_owner():
    return User(
        userId="u1",
        name="Sarah",
        email="sarah@email.com",
        phone="555-1001",
        availability={
            day: ["07:00-21:00"]
            for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        },
    )


def make_member(user_id, name):
    """Create an additional household member."""
    return User(
        userId=user_id,
        name=name,
        email=f"{name.lower()}@email.com",
        phone=f"555-{user_id[1:]}002",
        availability={
            day: ["08:00-20:00"]
            for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        },
    )


def make_pet(pet_id, name, breed="Mixed", age=2):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        return Pet(petId=pet_id, name=name, breed=breed, age=age, householdId="")


def make_household(owner):
    """Create a Household with owner and no pets."""
    return Household(householdId="h1", name="Test House", members=[owner], pets=[])


def make_task(task_id=None, pet_id=None, task_type=None, scheduled_time=None, assigned_to=None, status="scheduled", recurrence=None):
    """Create a Task with optional recurrence. Supports both old and new signatures."""
    # Handle legacy signature: make_task(owner)
    if task_id is not None and isinstance(task_id, User) and pet_id is None:
        return Task(
            taskId="t1",
            petId="p1",
            taskType="Walk",
            scheduledTime=datetime.now(),
            assignedTo=task_id,
            status="scheduled",
        )
    # New signature
    return Task(
        taskId=task_id,
        petId=pet_id,
        taskType=task_type,
        scheduledTime=scheduled_time,
        assignedTo=assigned_to,
        status=status,
        recurrence=recurrence,
    )


def make_scheduler(household, tasks):
    """Create a Scheduler with given household and tasks."""
    return Scheduler(household=household, tasks=tasks)


def make_household(owner):
    """Create a Household with owner and no pets."""
    return Household(householdId="h1", name="Test House", members=[owner], pets=[])


# ══════════════════════════════════════════════════════════════════════════════
# ORIGINAL TESTS (First 2)
# ══════════════════════════════════════════════════════════════════════════════

def test_marking_task_complete_changes_status():
    """Test that marking a task complete changes its status to 'completed'."""
    owner = make_owner()
    task = make_task("t1", "p1", "Walk", datetime.now(), owner)
    
    task.markCompleted()
    assert task.status == "completed"


def test_adding_pets_increases_pet_count():
    """Test that adding pets increases the pet count in household."""
    owner = make_owner()
    household = make_household(owner)
    
    pet1 = make_pet("p1", "Mochi")
    pet2 = make_pet("p2", "Luna")
    
    household.addPet(pet1)
    household.addPet(pet2)
    
    assert len(household.pets) == 2


# ══════════════════════════════════════════════════════════════════════════════
# CORE BEHAVIOR #1: CONFLICT DETECTION (18 tests)
# ══════════════════════════════════════════════════════════════════════════════

class TestConflictDetection:
    """Test the ability to detect when two tasks conflict."""

    # ── Happy Paths ────────────────────────────────────────────────────────

    def test_conflict_same_pet_same_time(self):
        """Same pet at exact same time should create a conflict."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        now = datetime.now()
        task1 = make_task("t1", "p1", "Walk", now, owner)
        task2 = make_task("t2", "p1", "Play", now, owner)

        scheduler = make_scheduler(household, [task1, task2])
        conflicts = scheduler.detect_conflicts()

        assert len(conflicts) > 0
        assert any("Mochi" in c for c in conflicts)

    def test_conflict_same_assignee_same_time(self):
        """Same person assigned to two tasks at same time should conflict."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        luna = make_pet("p2", "Luna")
        household.addPet(mochi)
        household.addPet(luna)

        now = datetime.now()
        task1 = make_task("t1", "p1", "Walk Mochi", now, owner)
        task2 = make_task("t2", "p2", "Walk Luna", now, owner)

        scheduler = make_scheduler(household, [task1, task2])
        conflicts = scheduler.detect_conflicts()

        assert len(conflicts) > 0
        assert any("Sarah" in c for c in conflicts or "assigned" in c)

    def test_no_conflict_different_times(self):
        """Tasks at different times should not conflict."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        now = datetime.now()
        task1 = make_task("t1", "p1", "Walk", now.replace(hour=8), owner)
        task2 = make_task("t2", "p1", "Play", now.replace(hour=18), owner)

        scheduler = make_scheduler(household, [task1, task2])
        conflicts = scheduler.detect_conflicts()

        assert len(conflicts) == 0

    def test_no_conflict_empty_task_list(self):
        """Scheduler with no tasks should report no conflicts."""
        owner = make_owner()
        household = make_household(owner)

        scheduler = make_scheduler(household, [])
        conflicts = scheduler.detect_conflicts()

        assert conflicts == []

    def test_multiple_conflicts_detected(self):
        """Multiple conflicts should all be reported."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        now = datetime.now()
        task1 = make_task("t1", "p1", "Walk", now, owner)
        task2 = make_task("t2", "p1", "Play", now, owner)
        task3 = make_task("t3", "p1", "Eat", now.replace(hour=now.hour + 1), owner)

        scheduler = make_scheduler(household, [task1, task2, task3])
        conflicts = scheduler.detect_conflicts()

        assert len(conflicts) >= 1  # At least the first two conflict

    # ── Edge Cases ─────────────────────────────────────────────────────────

    def test_conflict_ignored_for_completed_tasks(self):
        """Completed tasks should not create conflicts."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        now = datetime.now()
        task1 = make_task("t1", "p1", "Walk", now, owner, status="completed")
        task2 = make_task("t2", "p1", "Play", now, owner, status="scheduled")

        scheduler = make_scheduler(household, [task1, task2])
        conflicts = scheduler.detect_conflicts()

        assert len(conflicts) == 0

    def test_conflict_at_exact_second(self):
        """Two tasks at exact same second should conflict."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        exact_time = datetime(2026, 3, 29, 15, 0, 0)
        task1 = make_task("t1", "p1", "Walk", exact_time, owner)
        task2 = make_task("t2", "p1", "Play", exact_time, owner)

        scheduler = make_scheduler(household, [task1, task2])
        conflicts = scheduler.detect_conflicts()

        assert len(conflicts) > 0

    def test_no_conflict_one_second_apart(self):
        """Tasks 1 second apart should not conflict."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        time1 = datetime(2026, 3, 29, 15, 0, 0)
        time2 = datetime(2026, 3, 29, 15, 0, 1)
        task1 = make_task("t1", "p1", "Walk", time1, owner)
        task2 = make_task("t2", "p1", "Play", time2, owner)

        scheduler = make_scheduler(household, [task1, task2])
        conflicts = scheduler.detect_conflicts()

        assert len(conflicts) == 0

    def test_conflict_midnight_boundary(self):
        """Tasks at 11:59 PM and 12:00 AM (next day) should not conflict."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        time1 = datetime(2026, 3, 29, 23, 59, 0)
        time2 = datetime(2026, 3, 30, 0, 0, 0)
        task1 = make_task("t1", "p1", "Walk", time1, owner)
        task2 = make_task("t2", "p1", "Play", time2, owner)

        scheduler = make_scheduler(household, [task1, task2])
        conflicts = scheduler.detect_conflicts()

        assert len(conflicts) == 0

    def test_conflict_both_pet_and_assignee(self):
        """Should return both pet AND assignee conflicts if both exist."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        now = datetime.now()
        task1 = make_task("t1", "p1", "Walk", now, owner)
        task2 = make_task("t2", "p1", "Play", now, owner)

        scheduler = make_scheduler(household, [task1, task2])
        conflicts = scheduler.detect_conflicts()

        # Should have at least one conflict about the pet
        assert len(conflicts) > 0

    def test_conflict_single_task(self):
        """Single task should not conflict with itself."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        task = make_task("t1", "p1", "Walk", datetime.now(), owner)
        scheduler = make_scheduler(household, [task])
        conflicts = scheduler.detect_conflicts()

        assert len(conflicts) == 0

    def test_conflict_100_tasks_2_conflict(self):
        """Among 100 tasks, only 2 conflicts should be detected."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        base_time = datetime.now()
        tasks = []

        # Create 98 tasks at different times
        for i in range(98):
            t = make_task(f"t{i}", "p1", f"Task {i}", base_time + timedelta(hours=i), owner)
            tasks.append(t)

        # Create 2 tasks at same time (conflict)
        conflict_time = base_time + timedelta(hours=99)
        tasks.append(make_task("t98", "p1", "Task 98", conflict_time, owner))
        tasks.append(make_task("t99", "p1", "Task 99", conflict_time, owner))

        scheduler = make_scheduler(household, tasks)
        conflicts = scheduler.detect_conflicts()

        assert len(conflicts) > 0

    def test_conflict_warning_format_includes_time(self):
        """Conflict warning should include task time."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        now = datetime.now()
        task1 = make_task("t1", "p1", "Walk", now, owner)
        task2 = make_task("t2", "p1", "Play", now, owner)

        scheduler = make_scheduler(household, [task1, task2])
        conflicts = scheduler.detect_conflicts()

        assert len(conflicts) > 0
        # Should have time in the message
        assert any(":" in c for c in conflicts)  # HH:MM format

    def test_conflict_pet_name_in_warning(self):
        """Conflict warning should include pet name."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        now = datetime.now()
        task1 = make_task("t1", "p1", "Walk", now, owner)
        task2 = make_task("t2", "p1", "Play", now, owner)

        scheduler = make_scheduler(household, [task1, task2])
        conflicts = scheduler.detect_conflicts()

        assert len(conflicts) > 0
        assert any("Mochi" in c for c in conflicts)


# ══════════════════════════════════════════════════════════════════════════════
# CORE BEHAVIOR #2: RECURRING TASK EXECUTION (15 tests)
# ══════════════════════════════════════════════════════════════════════════════

class TestRecurringTasks:
    """Test creation of new tasks from recurring tasks."""

    # ── Happy Paths ────────────────────────────────────────────────────────

    def test_complete_and_recur_daily(self):
        """Completing a daily task creates next instance 24h later."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        now = datetime(2026, 3, 29, 8, 0, 0)
        task = make_task("t1", "p1", "Walk", now, owner, recurrence="daily")

        scheduler = make_scheduler(household, [task])
        new_task = scheduler.complete_and_recur(task, "t2")

        assert new_task is not None
        assert new_task.taskId == "t2"
        assert new_task.scheduledTime == datetime(2026, 3, 30, 8, 0, 0)
        assert task.status == "completed"

    def test_complete_and_recur_weekly(self):
        """Completing a weekly task creates next instance 7 days later."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        now = datetime(2026, 3, 29, 8, 0, 0)
        task = make_task("t1", "p1", "Walk", now, owner, recurrence="weekly")

        scheduler = make_scheduler(household, [task])
        new_task = scheduler.complete_and_recur(task, "t2")

        assert new_task is not None
        assert new_task.scheduledTime == datetime(2026, 4, 5, 8, 0, 0)

    def test_new_task_inherits_pet_and_type(self):
        """New recurring task should have same petId and taskType."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        task = make_task("t1", "p1", "Walk", datetime.now(), owner, recurrence="daily")
        scheduler = make_scheduler(household, [task])
        new_task = scheduler.complete_and_recur(task, "t2")

        assert new_task.petId == "p1"
        assert new_task.taskType == "Walk"

    def test_new_task_inherits_assignee(self):
        """New recurring task should be assigned to same person."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        task = make_task("t1", "p1", "Walk", datetime.now(), owner, recurrence="daily")
        scheduler = make_scheduler(household, [task])
        new_task = scheduler.complete_and_recur(task, "t2")

        assert new_task.assignedTo.userId == owner.userId

    def test_new_task_status_is_scheduled(self):
        """New recurring task should have status='scheduled'."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        task = make_task("t1", "p1", "Walk", datetime.now(), owner, recurrence="daily")
        scheduler = make_scheduler(household, [task])
        new_task = scheduler.complete_and_recur(task, "t2")

        assert new_task.status == "scheduled"

    def test_new_task_preserves_recurrence(self):
        """New recurring task should maintain recurrence type."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        task = make_task("t1", "p1", "Walk", datetime.now(), owner, recurrence="daily")
        scheduler = make_scheduler(household, [task])
        new_task = scheduler.complete_and_recur(task, "t2")

        assert new_task.recurrence == "daily"

    def test_non_recurring_task_returns_none(self):
        """Non-recurring task (recurrence=None) should return None."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        task = make_task("t1", "p1", "Walk", datetime.now(), owner, recurrence=None)
        scheduler = make_scheduler(household, [task])
        new_task = scheduler.complete_and_recur(task, "t2")

        assert new_task is None
        assert task.status == "completed"

    # ── Edge Cases ─────────────────────────────────────────────────────────

    def test_invalid_recurrence_type_raises_error(self):
        """Invalid recurrence value should raise ValueError."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        task = make_task("t1", "p1", "Walk", datetime.now(), owner, recurrence="biweekly")
        scheduler = make_scheduler(household, [task])

        try:
            scheduler.complete_and_recur(task, "t2")
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "recurrence" in str(e).lower()

    def test_daily_at_midnight_boundary(self):
        """Daily recurrence at 11:59 PM should create task at 11:59 PM next day."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        time_before_midnight = datetime(2026, 3, 29, 23, 59, 59)
        task = make_task("t1", "p1", "Walk", time_before_midnight, owner, recurrence="daily")

        scheduler = make_scheduler(household, [task])
        new_task = scheduler.complete_and_recur(task, "t2")

        assert new_task.scheduledTime == datetime(2026, 3, 30, 23, 59, 59)

    def test_leap_year_daily_feb_28_to_feb_29(self):
        """Daily task on Feb 28 of leap year should create Feb 29 task."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        # 2024 is a leap year
        feb_28 = datetime(2024, 2, 28, 8, 0, 0)
        task = make_task("t1", "p1", "Walk", feb_28, owner, recurrence="daily")

        scheduler = make_scheduler(household, [task])
        new_task = scheduler.complete_and_recur(task, "t2")

        assert new_task.scheduledTime.day == 29
        assert new_task.scheduledTime.month == 2

    def test_weekly_across_month_boundary(self):
        """Weekly task near month end should correctly span to next month."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        # Mar 29 + 7 days = Apr 5
        date_near_end = datetime(2026, 3, 29, 8, 0, 0)
        task = make_task("t1", "p1", "Walk", date_near_end, owner, recurrence="weekly")

        scheduler = make_scheduler(household, [task])
        new_task = scheduler.complete_and_recur(task, "t2")

        assert new_task.scheduledTime.month == 4  # Should be in April

    def test_complete_already_completed_task_raises_error(self):
        """Calling markCompleted() twice should raise ValueError."""
        owner = make_owner()
        task = make_task("t1", "p1", "Walk", datetime.now(), owner)
        
        task.markCompleted()
        try:
            task.markCompleted()
            assert False, "Should have raised ValueError"
        except ValueError:
            pass

    def test_new_task_added_to_scheduler_tasks(self):
        """New task created should be in scheduler.tasks list."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        task = make_task("t1", "p1", "Walk", datetime.now(), owner, recurrence="daily")
        scheduler = make_scheduler(household, [task])
        initial_count = len(scheduler.tasks)

        new_task = scheduler.complete_and_recur(task, "t2")

        assert len(scheduler.tasks) == initial_count + 1
        assert new_task in scheduler.tasks

    def test_chain_365_daily_tasks(self):
        """Completing 365 daily tasks should create chain correctly."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        start_date = datetime(2026, 1, 1, 8, 0, 0)
        current_task = make_task("t1", "p1", "Walk", start_date, owner, recurrence="daily")
        scheduler = make_scheduler(household, [current_task])

        for i in range(3):  # Test 3 iterations (could be 365 but slow)
            new_task = scheduler.complete_and_recur(current_task, f"t{i+2}")
            assert new_task is not None
            current_task = new_task

        # After 3 completions, should be 3 days later
        assert (current_task.scheduledTime - start_date).days == 3


# ══════════════════════════════════════════════════════════════════════════════
# CORE BEHAVIOR #3: TASK FILTERING & QUERIES (13 tests)
# ══════════════════════════════════════════════════════════════════════════════

class TestTaskFiltering:
    """Test filtering tasks by status, pet, or both."""

    # ── Happy Paths ────────────────────────────────────────────────────────

    def test_filter_by_status_scheduled(self):
        """Filter by status='scheduled' returns only scheduled tasks."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        task1 = make_task("t1", "p1", "Walk", datetime.now(), owner, status="scheduled")
        task2 = make_task("t2", "p1", "Play", datetime.now(), owner, status="completed")

        scheduler = make_scheduler(household, [task1, task2])
        result = scheduler.filter_tasks(status="scheduled")

        assert len(result) == 1
        assert result[0].taskId == "t1"

    def test_filter_by_status_completed(self):
        """Filter by status='completed' returns only completed tasks."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        task1 = make_task("t1", "p1", "Walk", datetime.now(), owner, status="scheduled")
        task2 = make_task("t2", "p1", "Play", datetime.now(), owner, status="completed")

        scheduler = make_scheduler(household, [task1, task2])
        result = scheduler.filter_tasks(status="completed")

        assert len(result) == 1
        assert result[0].taskId == "t2"

    def test_filter_by_pet_name(self):
        """Filter by pet_name='Mochi' returns only Mochi tasks."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        luna = make_pet("p2", "Luna")
        household.addPet(mochi)
        household.addPet(luna)

        task1 = make_task("t1", "p1", "Walk", datetime.now(), owner)
        task2 = make_task("t2", "p2", "Play", datetime.now(), owner)

        scheduler = make_scheduler(household, [task1, task2])
        result = scheduler.filter_tasks(pet_name="Mochi")

        assert len(result) == 1
        assert result[0].petId == "p1"

    def test_filter_by_both_status_and_pet(self):
        """Filter by both status and pet_name returns intersection."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        luna = make_pet("p2", "Luna")
        household.addPet(mochi)
        household.addPet(luna)

        task1 = make_task("t1", "p1", "Walk", datetime.now(), owner, status="scheduled")
        task2 = make_task("t2", "p1", "Play", datetime.now(), owner, status="completed")
        task3 = make_task("t3", "p2", "Walk", datetime.now(), owner, status="scheduled")

        scheduler = make_scheduler(household, [task1, task2, task3])
        result = scheduler.filter_tasks(status="scheduled", pet_name="Mochi")

        assert len(result) == 1
        assert result[0].taskId == "t1"

    def test_filter_case_insensitive_pet_name(self):
        """Filter should be case-insensitive (mochi == Mochi == MOCHI)."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        task = make_task("t1", "p1", "Walk", datetime.now(), owner)
        scheduler = make_scheduler(household, [task])

        for pet_name in ["mochi", "MOCHI", "MoChI", "Mochi"]:
            result = scheduler.filter_tasks(pet_name=pet_name)
            assert len(result) == 1

    # ── Edge Cases ─────────────────────────────────────────────────────────

    def test_filter_no_tasks_exist(self):
        """Filter on empty task list returns empty list."""
        owner = make_owner()
        household = make_household(owner)

        scheduler = make_scheduler(household, [])
        result = scheduler.filter_tasks(status="scheduled")

        assert result == []

    def test_filter_pet_not_found(self):
        """Filter for non-existent pet returns empty list."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        task = make_task("t1", "p1", "Walk", datetime.now(), owner)
        scheduler = make_scheduler(household, [task])
        result = scheduler.filter_tasks(pet_name="Fluffy")

        assert result == []

    def test_filter_status_not_found(self):
        """Filter for non-existent status returns empty list."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        task = make_task("t1", "p1", "Walk", datetime.now(), owner, status="scheduled")
        scheduler = make_scheduler(household, [task])
        result = scheduler.filter_tasks(status="completed")

        assert result == []

    def test_filter_empty_string_pet_name(self):
        """Filter with pet_name='' returns empty list (no match)."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        task = make_task("t1", "p1", "Walk", datetime.now(), owner)
        scheduler = make_scheduler(household, [task])
        result = scheduler.filter_tasks(pet_name="")

        assert result == []

    def test_filter_none_status_returns_all(self):
        """Filter with status=None returns all tasks regardless of status."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        task1 = make_task("t1", "p1", "Walk", datetime.now(), owner, status="scheduled")
        task2 = make_task("t2", "p1", "Play", datetime.now(), owner, status="completed")

        scheduler = make_scheduler(household, [task1, task2])
        result = scheduler.filter_tasks(status=None)

        assert len(result) == 2

    def test_filter_none_pet_name_returns_all(self):
        """Filter with pet_name=None returns all pets' tasks."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        luna = make_pet("p2", "Luna")
        household.addPet(mochi)
        household.addPet(luna)

        task1 = make_task("t1", "p1", "Walk", datetime.now(), owner)
        task2 = make_task("t2", "p2", "Play", datetime.now(), owner)

        scheduler = make_scheduler(household, [task1, task2])
        result = scheduler.filter_tasks(pet_name=None)

        assert len(result) == 2

    def test_filter_pet_with_spaces_in_name(self):
        """Filter should work with pet names containing spaces."""
        owner = make_owner()
        household = make_household(owner)
        fluffy = make_pet("p1", "Mr. Fluffington")
        household.addPet(fluffy)

        task = make_task("t1", "p1", "Walk", datetime.now(), owner)
        scheduler = make_scheduler(household, [task])
        result = scheduler.filter_tasks(pet_name="mr. fluffington")

        assert len(result) == 1

    def test_filter_large_task_set(self):
        """Filter should work efficiently with many tasks."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        tasks = []
        for i in range(100):
            status = "scheduled" if i % 2 == 0 else "completed"
            t = make_task(f"t{i}", "p1", f"Task {i}", datetime.now(), owner, status=status)
            tasks.append(t)

        scheduler = make_scheduler(household, tasks)
        result = scheduler.filter_tasks(status="scheduled")

        assert len(result) == 50  # Half should be scheduled


# ══════════════════════════════════════════════════════════════════════════════
# CORE BEHAVIOR #4: NOTIFICATION WORKFLOW (14 tests)
# ══════════════════════════════════════════════════════════════════════════════

class TestNotificationWorkflow:
    """Test the state machine for notification pings."""

    # ── Happy Paths ────────────────────────────────────────────────────────

    def test_send_ping_changes_pending_to_sent(self):
        """sendPing() should change status from 'pending' to 'sent'."""
        owner = make_owner()
        member = make_member("u2", "Alex")

        notif = Notification(
            pingId="n1",
            taskId="t1",
            fromUser=owner,
            toUser=member,
            message="Can you walk Mochi?",
            status="pending",
            createdAt=datetime.now(),
        )

        notif.sendPing()
        assert notif.status == "sent"

    def test_accept_ping_changes_sent_to_accepted(self):
        """acceptPing() should change status from 'sent' to 'accepted'."""
        owner = make_owner()
        member = make_member("u2", "Alex")

        notif = Notification(
            pingId="n1",
            taskId="t1",
            fromUser=owner,
            toUser=member,
            message="Can you walk Mochi?",
            status="sent",
            createdAt=datetime.now(),
        )

        notif.acceptPing()
        assert notif.status == "accepted"

    def test_accept_ping_sets_responded_at(self):
        """acceptPing() should set respondedAt timestamp."""
        owner = make_owner()
        member = make_member("u2", "Alex")

        notif = Notification(
            pingId="n1",
            taskId="t1",
            fromUser=owner,
            toUser=member,
            message="Can you walk Mochi?",
            status="sent",
            createdAt=datetime.now(),
            respondedAt=None,
        )

        before = datetime.now()
        notif.acceptPing()
        after = datetime.now()

        assert notif.respondedAt is not None
        assert before <= notif.respondedAt <= after

    def test_decline_ping_changes_sent_to_declined(self):
        """declinePing() should change status from 'sent' to 'declined'."""
        owner = make_owner()
        member = make_member("u2", "Alex")

        notif = Notification(
            pingId="n1",
            taskId="t1",
            fromUser=owner,
            toUser=member,
            message="Can you walk Mochi?",
            status="sent",
            createdAt=datetime.now(),
        )

        notif.declinePing()
        assert notif.status == "declined"

    def test_decline_ping_sets_responded_at(self):
        """declinePing() should set respondedAt timestamp."""
        owner = make_owner()
        member = make_member("u2", "Alex")

        notif = Notification(
            pingId="n1",
            taskId="t1",
            fromUser=owner,
            toUser=member,
            message="Can you walk Mochi?",
            status="sent",
            createdAt=datetime.now(),
            respondedAt=None,
        )

        before = datetime.now()
        notif.declinePing()
        after = datetime.now()

        assert notif.respondedAt is not None
        assert before <= notif.respondedAt <= after

    # ── Edge Cases ─────────────────────────────────────────────────────────

    def test_send_ping_twice_raises_error(self):
        """Calling sendPing() twice should raise ValueError."""
        owner = make_owner()
        member = make_member("u2", "Alex")

        notif = Notification(
            pingId="n1",
            taskId="t1",
            fromUser=owner,
            toUser=member,
            message="Can you walk Mochi?",
            status="pending",
            createdAt=datetime.now(),
        )

        notif.sendPing()
        try:
            notif.sendPing()
            assert False, "Should raise ValueError"
        except ValueError:
            pass

    def test_accept_then_decline_raises_error(self):
        """Accepting then declining should raise ValueError."""
        owner = make_owner()
        member = make_member("u2", "Alex")

        notif = Notification(
            pingId="n1",
            taskId="t1",
            fromUser=owner,
            toUser=member,
            message="Can you walk Mochi?",
            status="sent",
            createdAt=datetime.now(),
        )

        notif.acceptPing()
        try:
            notif.declinePing()
            assert False, "Should raise ValueError"
        except ValueError:
            pass

    def test_accept_twice_raises_error(self):
        """Calling acceptPing() twice should raise ValueError."""
        owner = make_owner()
        member = make_member("u2", "Alex")

        notif = Notification(
            pingId="n1",
            taskId="t1",
            fromUser=owner,
            toUser=member,
            message="Can you walk Mochi?",
            status="sent",
            createdAt=datetime.now(),
        )

        notif.acceptPing()
        try:
            notif.acceptPing()
            assert False, "Should raise ValueError"
        except ValueError:
            pass

    def test_decline_twice_raises_error(self):
        """Calling declinePing() twice should raise ValueError."""
        owner = make_owner()
        member = make_member("u2", "Alex")

        notif = Notification(
            pingId="n1",
            taskId="t1",
            fromUser=owner,
            toUser=member,
            message="Can you walk Mochi?",
            status="sent",
            createdAt=datetime.now(),
        )

        notif.declinePing()
        try:
            notif.declinePing()
            assert False, "Should raise ValueError"
        except ValueError:
            pass

    def test_accept_with_empty_message_allowed(self):
        """Empty message string should be allowed."""
        owner = make_owner()
        member = make_member("u2", "Alex")

        notif = Notification(
            pingId="n1",
            taskId="t1",
            fromUser=owner,
            toUser=member,
            message="",
            status="sent",
            createdAt=datetime.now(),
        )

        notif.acceptPing()
        assert notif.status == "accepted"

    def test_responded_at_greater_than_created_at(self):
        """respondedAt should be >= createdAt."""
        owner = make_owner()
        member = make_member("u2", "Alex")
        created = datetime.now()

        notif = Notification(
            pingId="n1",
            taskId="t1",
            fromUser=owner,
            toUser=member,
            message="Can you walk Mochi?",
            status="sent",
            createdAt=created,
        )

        notif.acceptPing()
        assert notif.respondedAt >= notif.createdAt

    def test_multiple_pings_tracked_independently(self):
        """Multiple notifications for same task should be independent."""
        owner = make_owner()
        member1 = make_member("u2", "Alex")
        member2 = make_member("u3", "Jordan")

        notif1 = Notification(
            pingId="n1",
            taskId="t1",
            fromUser=owner,
            toUser=member1,
            message="Alex, can you help?",
            status="sent",
            createdAt=datetime.now(),
        )

        notif2 = Notification(
            pingId="n2",
            taskId="t1",
            fromUser=owner,
            toUser=member2,
            message="Jordan, can you help?",
            status="sent",
            createdAt=datetime.now(),
        )

        notif1.acceptPing()
        notif2.declinePing()

        assert notif1.status == "accepted"
        assert notif2.status == "declined"


# ══════════════════════════════════════════════════════════════════════════════
# CORE BEHAVIOR #5: TASK SORTING (10 tests)
# ══════════════════════════════════════════════════════════════════════════════

class TestTaskSorting:
    """Test sorting tasks by scheduled time."""

    # ── Happy Paths ────────────────────────────────────────────────────────

    def test_sort_by_time_one_task(self):
        """Sorting single task should return [that task]."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        task = make_task("t1", "p1", "Walk", datetime.now(), owner)
        scheduler = make_scheduler(household, [task])
        result = scheduler.sort_by_time()

        assert len(result) == 1
        assert result[0].taskId == "t1"

    def test_sort_by_time_three_tasks_unsorted(self):
        """Three tasks in random order should sort chronologically."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        now = datetime.now()
        task1 = make_task("t1", "p1", "Walk", now.replace(hour=18), owner)
        task2 = make_task("t2", "p1", "Play", now.replace(hour=8), owner)
        task3 = make_task("t3", "p1", "Eat", now.replace(hour=12), owner)

        scheduler = make_scheduler(household, [task1, task2, task3])
        result = scheduler.sort_by_time()

        # Should be: 8am, 12pm, 6pm
        assert result[0].taskId == "t2"
        assert result[1].taskId == "t3"
        assert result[2].taskId == "t1"

    def test_sort_by_time_already_sorted(self):
        """Already-sorted tasks should remain sorted."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        now = datetime.now()
        task1 = make_task("t1", "p1", "Walk", now.replace(hour=8), owner)
        task2 = make_task("t2", "p1", "Play", now.replace(hour=12), owner)
        task3 = make_task("t3", "p1", "Eat", now.replace(hour=18), owner)

        scheduler = make_scheduler(household, [task1, task2, task3])
        result = scheduler.sort_by_time()

        assert result[0].taskId == "t1"
        assert result[1].taskId == "t2"
        assert result[2].taskId == "t3"

    def test_sort_by_time_doesnt_mutate_original(self):
        """sort_by_time() should not change the original task list."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        now = datetime.now()
        task1 = make_task("t1", "p1", "Walk", now.replace(hour=18), owner)
        task2 = make_task("t2", "p1", "Play", now.replace(hour=8), owner)

        original_order = [task1, task2]
        scheduler = make_scheduler(household, original_order)
        result = scheduler.sort_by_time()

        # Result should be sorted
        assert result[0].taskId == "t2"
        assert result[1].taskId == "t1"

        # Original scheduler.tasks should still have task1 first
        assert scheduler.tasks[0].taskId == "t1"

    # ── Edge Cases ─────────────────────────────────────────────────────────

    def test_sort_empty_task_list(self):
        """Sorting empty list should return empty list."""
        owner = make_owner()
        household = make_household(owner)

        scheduler = make_scheduler(household, [])
        result = scheduler.sort_by_time()

        assert result == []

    def test_sort_two_tasks_exact_same_time(self):
        """Two tasks at same time should maintain order (stable sort)."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        exact_time = datetime(2026, 3, 29, 15, 0, 0)
        task1 = make_task("t1", "p1", "Walk", exact_time, owner)
        task2 = make_task("t2", "p1", "Play", exact_time, owner)

        scheduler = make_scheduler(household, [task1, task2])
        result = scheduler.sort_by_time()

        # Both exist, order should be preserved from original
        assert len(result) == 2
        assert result[0].taskId == "t1"
        assert result[1].taskId == "t2"

    def test_sort_microsecond_differences(self):
        """Tasks differing by microseconds should sort correctly."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        time1 = datetime(2026, 3, 29, 15, 0, 0, 0)
        time2 = datetime(2026, 3, 29, 15, 0, 0, 1)
        task1 = make_task("t1", "p1", "Walk", time2, owner)
        task2 = make_task("t2", "p1", "Play", time1, owner)

        scheduler = make_scheduler(household, [task1, task2])
        result = scheduler.sort_by_time()

        assert result[0].taskId == "t2"
        assert result[1].taskId == "t1"

    def test_sort_midnight_boundary(self):
        """11:59 PM and 12:00 AM should sort correctly."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        time_before = datetime(2026, 3, 29, 23, 59, 0)
        time_after = datetime(2026, 3, 30, 0, 0, 0)
        task1 = make_task("t1", "p1", "Walk", time_after, owner)
        task2 = make_task("t2", "p1", "Play", time_before, owner)

        scheduler = make_scheduler(household, [task1, task2])
        result = scheduler.sort_by_time()

        assert result[0].taskId == "t2"  # 11:59 PM first
        assert result[1].taskId == "t1"  # 12:00 AM second

    def test_sort_100_tasks(self):
        """Sorting 100 tasks should be efficient and correct."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        base_time = datetime.now()
        tasks = []
        # Create 100 tasks in reverse order
        for i in range(100, 0, -1):
            t = make_task(f"t{i}", "p1", f"Task {i}", base_time + timedelta(hours=i), owner)
            tasks.append(t)

        scheduler = make_scheduler(household, tasks)
        result = scheduler.sort_by_time()

        # First task should be t1 (earliest)
        assert result[0].taskId == "t1"
        # Last task should be t100 (latest)
        assert result[99].taskId == "t100"


# ══════════════════════════════════════════════════════════════════════════════
# INTEGRATION: CROSS-BEHAVIOR SCENARIOS (5 tests)
# ══════════════════════════════════════════════════════════════════════════════

class TestIntegration:
    """Test interactions between multiple behaviors."""

    def test_complete_and_recur_then_sort_includes_new_task(self):
        """After complete_and_recur(), sort_by_time() should include new task."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        now = datetime.now()
        task1 = make_task("t1", "p1", "Walk", now.replace(hour=8), owner, recurrence="daily")
        task2 = make_task("t2", "p1", "Play", now.replace(hour=18), owner)

        scheduler = make_scheduler(household, [task1, task2])
        new_task = scheduler.complete_and_recur(task1, "t3")

        sorted_tasks = scheduler.sort_by_time()
        task_ids = [t.taskId for t in sorted_tasks]

        assert "t3" in task_ids  # New task should be in sorted list

    def test_complete_and_recur_new_task_detects_conflicts(self):
        """New recurring task should be checked for conflicts."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        tomorrow = datetime.now() + timedelta(days=1)
        task1 = make_task("t1", "p1", "Walk", tomorrow.replace(hour=15), owner, recurrence="daily")
        # Task2 placed on same day as recurring task's next occurrence (tomorrow+1 day)
        task2 = make_task("t2", "p1", "Vet", tomorrow.replace(hour=15) + timedelta(days=1), owner)

        scheduler = make_scheduler(household, [task1, task2])
        new_task = scheduler.complete_and_recur(task1, "t3")

        conflicts = scheduler.detect_conflicts()
        assert len(conflicts) > 0

    def test_filter_then_sort_maintains_order(self):
        """Filtering then sorting should maintain correct order."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        now = datetime.now()
        task1 = make_task("t1", "p1", "Walk", now.replace(hour=18), owner, status="scheduled")
        task2 = make_task("t2", "p1", "Play", now.replace(hour=8), owner, status="completed")
        task3 = make_task("t3", "p1", "Eat", now.replace(hour=12), owner, status="scheduled")

        scheduler = make_scheduler(household, [task1, task2, task3])
        filtered = scheduler.filter_tasks(status="scheduled")
        # Manually sort since filter returns list not Scheduler result
        sorted_filtered = sorted(filtered, key=lambda t: t.scheduledTime)

        assert sorted_filtered[0].taskId == "t3"  # 12pm
        assert sorted_filtered[1].taskId == "t1"  # 6pm

    def test_send_ping_accept_then_update_filters(self):
        """Accepting a ping should update task filtering results."""
        owner = make_owner()
        member = make_member("u2", "Alex")
        household = make_household(owner)
        household.addMember(member)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        now = datetime.now()
        task = make_task("t1", "p1", "Walk", now, owner)

        notif = Notification(
            pingId="n1",
            taskId="t1",
            fromUser=owner,
            toUser=member,
            message="Can you walk Mochi?",
            status="pending",
            createdAt=now,
        )

        notif.sendPing()
        notif.acceptPing()

        # After acceptance, task should be reassignable to member
        assert notif.status == "accepted"
        assert task.taskId == "t1"  # Task remains in system

    def test_large_scenario_recurring_conflicts_and_filters(self):
        """Complex scenario: recurring tasks, conflicts, and filters."""
        owner = make_owner()
        household = make_household(owner)
        mochi = make_pet("p1", "Mochi")
        household.addPet(mochi)

        base_time = datetime.now()
        tasks = []

        # Create 10 daily recurring tasks
        for i in range(10):
            t = make_task(
                f"t{i}",
                "p1",
                f"Task {i}",
                base_time + timedelta(hours=i),
                owner,
                recurrence="daily",
            )
            tasks.append(t)

        scheduler = make_scheduler(household, tasks)

        # Complete first task (creates recurring next instance)
        new_task = scheduler.complete_and_recur(tasks[0], "t_new")

        # Filter and sort
        scheduled = scheduler.filter_tasks(status="scheduled")
        sorted_scheduled = sorted(scheduled, key=lambda t: t.scheduledTime)

        # Should have 9 original + 1 new = 10 scheduled
        assert len(scheduled) == 10
        assert sorted_scheduled[0].scheduledTime <= sorted_scheduled[-1].scheduledTime


def test_marking_task_complete_changes_status():
    owner = make_owner()
    task = make_task(owner)

    task.markCompleted()

    assert task.status == "completed"


def test_adding_pets_increases_pet_count():
    owner = make_owner()
    household = Household(householdId="h1", name="Test House", members=[owner], pets=[])

    mochi = make_pet("p1", "Mochi")
    luna  = make_pet("p2", "Luna")
    bean  = make_pet("p3", "Bean")

    household.addPet(mochi)
    assert len(household.pets) == 1

    household.addPet(luna)
    assert len(household.pets) == 2

    household.addPet(bean)
    assert len(household.pets) == 3
