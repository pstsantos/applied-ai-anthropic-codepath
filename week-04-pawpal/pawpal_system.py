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
    
    def addUser(self):
        pass
    
    def updateAvailability(self):
        pass
    
    def getAvailability(self):
        pass


@dataclass
class Household:
    householdId: str
    name: str
    members: List[User]
    pets: List['Pet']
    
    def createHousehold(self):
        pass
    
    def addMember(self):
        pass
    
    def removeMember(self):
        pass
    
    def addPet(self):
        pass


@dataclass
class Pet:
    petId: str
    name: str
    age: int
    breed: str
    vetName: str
    vetPhone: str
    householdId: str
    
    def addPet(self):
        pass
    
    def removePet(self):
        pass
    
    def updatePetInfo(self):
        pass


@dataclass
class Task:
    taskId: str
    petId: str
    taskType: str
    scheduledTime: datetime
    assignedTo: User
    status: str
    
    def scheduleTask(self):
        pass
    
    def getTaskStatus(self):
        pass
    
    def markCompleted(self):
        pass
    
    def reassignTask(self):
        pass


@dataclass
class TaskLog:
    logId: str
    taskId: str
    actualTime: datetime
    completedBy: User
    timestamp: datetime
    
    def logTask(self):
        pass
    
    def getTaskHistory(self):
        pass


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
    
    def sendPing(self):
        pass
    
    def acceptPing(self):
        pass
    
    def declinePing(self):
        pass


class Scheduler:
    def getAvailableUsers(self):
        pass
    
    def isTimeInSlots(self):
        pass
    
    def findConflicts(self):
        pass