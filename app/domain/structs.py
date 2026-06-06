import msgspec
from enum import Enum
from uuid import UUID

class UserRole(str, Enum):
    STUDENT = "student"
    DM = "dm"

class RoomCreate(msgspec.Struct):
    name: str
    description: str | None = None
    capacity: int = 5

class RoomResponse(msgspec.Struct):
    id: UUID
    name: str
    description: str | None
    capacity: int
    creator_id: UUID  
    status: str