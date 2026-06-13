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
    invitation_code: str | None = None
    qr_code: str | None = None

class JoinRoomRequest(msgspec.Struct):
    invitation_code: str

class MemberResponse(msgspec.Struct):
    message: str
    room_id: str | None = None