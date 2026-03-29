import warnings
from datetime import datetime
from pawpal_system import User, Household, Pet, Task


def make_owner():
    return User(
        userId="u1",
        name="Sarah",
        email="sarah@email.com",
        phone="555-1001",
        availability={},
    )


def make_pet(pet_id, name):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        return Pet(petId=pet_id, name=name, breed="Mixed", age=2, householdId="")


def make_task(owner):
    return Task(
        taskId="t1",
        petId="p1",
        taskType="Walk",
        scheduledTime=datetime.now(),
        assignedTo=owner,
        status="scheduled",
    )


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
