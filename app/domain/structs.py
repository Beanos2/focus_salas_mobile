import msgspec
from enum import Enum

class UserRole(str, Enum):
    STUDENT = "student"
    DM = "dm"

class RoomCreate(msgspec.Struct):
    name: str
    description: str | None = None
    capacity: int = 5