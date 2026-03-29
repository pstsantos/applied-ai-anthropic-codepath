import warnings
from pawpal_system import User, Household, Pet, Task, TaskLog, Scheduler
from datetime import datetime, timedelta

# # Suppress vet warnings for this demo since we're setting them up intentionally
# warnings.filterwarnings("ignore", category=UserWarning)

# --- Setup ---

today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

owner = User(
    userId="u1",
    name="Sarah",
    email="sarah@email.com",
    phone="555-1001",
    availability={
        "Monday":    ["07:00-21:00"],
        "Tuesday":   ["07:00-21:00"],
        "Wednesday": ["07:00-21:00"],
        "Thursday":  ["07:00-21:00"],
        "Friday":    ["07:00-21:00"],
        "Saturday":  ["08:00-20:00"],
        "Sunday":    ["08:00-20:00"],
    }
)

household = Household(householdId="h1", name="The Santos House", members=[owner], pets=[])

mochi = Pet(
    petId="p1",
    name="Mochi",
    breed="Shiba Inu",
    age=3,
    householdId="",
    vetName="Dr. Kim",
    vetPhone="555-9001",
)

luna = Pet(
    petId="p2",
    name="Luna",
    breed="Domestic Shorthair",
    age=5,
    householdId="",
    vetName="Dr. Kim",
    vetPhone="555-9001",
)

mochi.addPet(household)
luna.addPet(household)

# --- Tasks ---

morning_walk = Task(
    taskId="t1",
    petId=mochi.petId,
    taskType="Morning Walk",
    scheduledTime=today.replace(hour=8, minute=0),
    assignedTo=owner,
    status="scheduled",
)

feeding = Task(
    taskId="t2",
    petId=luna.petId,
    taskType="Feeding",
    scheduledTime=today.replace(hour=12, minute=0),
    assignedTo=owner,
    status="scheduled",
)

evening_walk = Task(
    taskId="t3",
    petId=mochi.petId,
    taskType="Evening Walk",
    scheduledTime=today.replace(hour=18, minute=30),
    assignedTo=owner,
    status="scheduled",
)

vet_checkup = Task(
    taskId="t4",
    petId=luna.petId,
    taskType="Vet Check-up",
    scheduledTime=today.replace(hour=15, minute=0),
    assignedTo=owner,
    status="scheduled",
)

# Intentionally out of order to prove sorting works
all_tasks = [evening_walk, vet_checkup, morning_walk, feeding]

scheduler = Scheduler(household=household, tasks=all_tasks)

pet_lookup = {pet.petId: pet.name for pet in household.pets}


def print_tasks(tasks, label):
    print("=" * 50)
    print(f"  {label}")
    print("=" * 50)
    if not tasks:
        print("  (no tasks)")
    for task in tasks:
        pet_name = pet_lookup.get(task.petId, "?")
        time_str = task.scheduledTime.strftime("%I:%M %p")
        print(f"  {time_str}  |  {task.taskType:<20} |  {pet_name:<10}  |  {task.status}")
    print("=" * 50)


# 1 — Raw order (unsorted) to show the starting state
print_tasks(all_tasks, "RAW ORDER (as added)")

# 2 — Sorted by time using Scheduler.sort_by_time()
print_tasks(scheduler.sort_by_time(), "SORTED BY TIME — scheduler.sort_by_time()")

# 3 — Filter: scheduled tasks only
print_tasks(
    scheduler.filter_tasks(status="scheduled"),
    "FILTER — status='scheduled'",
)

# Mark one task completed to make the next filter interesting
morning_walk.markCompleted()

# 4 — Filter: completed tasks only
print_tasks(
    scheduler.filter_tasks(status="completed"),
    "FILTER — status='completed'",
)

# 5 — Filter: all tasks for Mochi
print_tasks(
    scheduler.filter_tasks(pet_name="Mochi"),
    "FILTER — pet_name='Mochi'",
)

# 6 — Filter: Mochi's scheduled tasks only (both filters stacked)
print_tasks(
    scheduler.filter_tasks(status="scheduled", pet_name="Mochi"),
    "FILTER — status='scheduled' + pet_name='Mochi'",
)
