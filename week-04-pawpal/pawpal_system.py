import warnings
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class User:
    userId: str
    name: str
    email: str
    phone: str
    availability: dict

    def addUser(self) -> dict:
        """Validate required fields and return a summary of the registered user."""
        if not all([self.userId, self.name, self.email, self.phone]):
            raise ValueError("userId, name, email, and phone are all required.")
        return {
            "userId": self.userId,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
        }

    def updateAvailability(self, availability: dict) -> None:
        """Replace the user's availability schedule.

        Expected format: {"Monday": ["09:00-12:00", "14:00-18:00"], ...}
        """
        if not isinstance(availability, dict):
            raise TypeError("availability must be a dict mapping day names to time slot lists.")
        self.availability = availability

    def getAvailability(self) -> dict:
        """Return the user's current availability schedule."""
        return self.availability


@dataclass
class Household:
    householdId: str
    name: str
    members: List[User]
    pets: List['Pet']

    def createHousehold(self) -> dict:
        """Validate and return a summary of the household."""
        if not self.householdId or not self.name:
            raise ValueError("householdId and name are required.")
        return {
            "householdId": self.householdId,
            "name": self.name,
            "memberCount": len(self.members),
            "petCount": len(self.pets),
        }

    def addMember(self, user: User) -> None:
        """Add a user to the household if they are not already a member."""
        if any(m.userId == user.userId for m in self.members):
            raise ValueError(f"User '{user.userId}' is already a member of this household.")
        self.members.append(user)

    def removeMember(self, user_id: str) -> None:
        """Remove a member by userId, raising an error if not found."""
        for i, member in enumerate(self.members):
            if member.userId == user_id:
                del self.members[i]
                return
        raise ValueError(f"No member with userId '{user_id}' found in this household.")

    def addPet(self, pet: 'Pet') -> None:
        """Add a pet to the household if it is not already registered."""
        if any(p.petId == pet.petId for p in self.pets):
            raise ValueError(f"Pet '{pet.petId}' is already in this household.")
        pet.householdId = self.householdId
        self.pets.append(pet)


@dataclass
class Pet:
    petId: str
    name: str
    age: int
    breed: str
    householdId: str
    vetName: Optional[str] = None
    vetPhone: Optional[str] = None

    def __post_init__(self):
        if not self.vetName or not self.vetPhone:
            warnings.warn(
                f"Pet '{self.name}' has no vet information. Adding a vet is highly recommended.",
                UserWarning,
                stacklevel=2,
            )

    def addPet(self, household: Household) -> None:
        """Register this pet into the given household."""
        household.addPet(self)

    def removePet(self, household: Household) -> None:
        """Remove this pet from the given household."""
        for i, pet in enumerate(household.pets):
            if pet.petId == self.petId:
                del household.pets[i]
                self.householdId = ""
                return
        raise ValueError(f"Pet '{self.petId}' not found in household '{household.householdId}'.")

    def updatePetInfo(self, **kwargs) -> None:
        """Update one or more pet fields by keyword argument.

        Accepted keys: name, age, breed, vetName, vetPhone
        """
        allowed = {"name", "age", "breed", "vetName", "vetPhone"}
        invalid = set(kwargs) - allowed
        if invalid:
            raise ValueError(f"Invalid field(s): {invalid}. Allowed: {allowed}")
        for field, value in kwargs.items():
            setattr(self, field, value)


@dataclass
class Task:
    taskId: str
    petId: str
    taskType: str
    scheduledTime: datetime
    assignedTo: User
    status: str

    def scheduleTask(self, scheduled_time: datetime, assigned_to: User) -> None:
        """Set the task's time and assignee, then mark it as 'scheduled'."""
        self.scheduledTime = scheduled_time
        self.assignedTo = assigned_to
        self.status = "scheduled"

    def getTaskStatus(self) -> str:
        """Return the current status of the task."""
        return self.status

    def markCompleted(self) -> None:
        """Mark the task as completed. Raises if already completed."""
        if self.status == "completed":
            raise ValueError(f"Task '{self.taskId}' is already marked as completed.")
        self.status = "completed"

    def reassignTask(self, user: User) -> None:
        """Reassign the task to a different household member."""
        self.assignedTo = user


@dataclass
class TaskLog:
    logId: str
    taskId: str
    actualTime: datetime
    completedBy: User
    timestamp: datetime

    @classmethod
    def logTask(cls, log_id: str, task: Task, completed_by: User, actual_time: datetime) -> 'TaskLog':
        """Create and return a TaskLog entry for a completed task.

        Also marks the task as completed if it isn't already.
        """
        if task.status != "completed":
            raise ValueError(f"Task '{task.taskId}' must be marked completed before logging.")
        return cls(
            logId=log_id,
            taskId=task.taskId,
            actualTime=actual_time,
            completedBy=completed_by,
            timestamp=datetime.now(),
        )

    @staticmethod
    def getTaskHistory(logs: List['TaskLog'], task_id: str) -> List['TaskLog']:
        """Return all log entries for a given taskId, ordered by timestamp."""
        return sorted(
            [log for log in logs if log.taskId == task_id],
            key=lambda log: log.timestamp,
        )


@dataclass
class Notification:
    pingId: str
    taskId: str
    fromUser: User
    toUser: User
    message: str
    status: str
    createdAt: datetime
    respondedAt: Optional[datetime] = None

    def sendPing(self) -> None:
        """Mark the notification as sent."""
        if self.status != "pending":
            raise ValueError(f"Notification '{self.pingId}' has already been sent or responded to.")
        self.status = "sent"

    def acceptPing(self) -> None:
        """Record that the recipient accepted the task ping."""
        if self.status not in ("sent", "pending"):
            raise ValueError(f"Notification '{self.pingId}' cannot be accepted (status: '{self.status}').")
        self.status = "accepted"
        self.respondedAt = datetime.now()

    def declinePing(self) -> None:
        """Record that the recipient declined the task ping."""
        if self.status not in ("sent", "pending"):
            raise ValueError(f"Notification '{self.pingId}' cannot be declined (status: '{self.status}').")
        self.status = "declined"
        self.respondedAt = datetime.now()


@dataclass
class Scheduler:
    household: Household
    tasks: List[Task]

    def getAvailableUsers(self, scheduled_time: datetime) -> List[User]:
        """Return household members who are available at the given datetime."""
        day = scheduled_time.strftime("%A")  # e.g. "Monday"
        return [
            member for member in self.household.members
            if self.isTimeInSlots(scheduled_time, member.availability.get(day, []))
        ]

    def isTimeInSlots(self, time: datetime, slots: List[str]) -> bool:
        """Check whether a datetime falls within any of the provided time slots.

        Each slot is a string in "HH:MM-HH:MM" format, e.g. "09:00-17:00".
        """
        t = time.time()
        for slot in slots:
            start_str, end_str = slot.split("-")
            start = datetime.strptime(start_str.strip(), "%H:%M").time()
            end = datetime.strptime(end_str.strip(), "%H:%M").time()
            if start <= t <= end:
                return True
        return False

