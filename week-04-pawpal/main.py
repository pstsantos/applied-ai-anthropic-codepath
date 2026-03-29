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

all_tasks = [morning_walk, feeding, vet_checkup, evening_walk]

# --- Print Today's Schedule ---

pet_lookup = {pet.petId: pet.name for pet in household.pets}

print("=" * 40)
print(f"  TODAY'S SCHEDULE — {today.strftime('%A, %b %d')}")
print(f"  Household: {household.name}")
print("=" * 40)

for task in sorted(all_tasks, key=lambda t: t.scheduledTime):
    pet_name = pet_lookup.get(task.petId, "Unknown Pet")
    time_str = task.scheduledTime.strftime("%I:%M %p")
    print(f"  {time_str}  |  {task.taskType:<20} |  {pet_name:<10}  |  {task.status}")

print("=" * 40)
print(f"  Owner: {owner.name}    Pets: {len(household.pets)}    Tasks: {len(all_tasks)}")
print("=" * 40)
