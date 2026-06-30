import msgspec
from enum import Enum
from uuid import UUID
from datetime import datetime, time


class UserRole(str, Enum):
    STUDENT = "student"
    DM = "dm"

class RoomCreate(msgspec.Struct):
    name: str
    description: str | None = None
    capacity: int = 5
    xp_multiplier: float = 1.3
    valid_from_time: time | None = None
    valid_until_time: time | None = None


class RoomResponse(msgspec.Struct):
    id: UUID
    name: str
    description: str | None
    capacity: int
    creator_id: UUID
    status: str
    xp_multiplier: float
    invitation_code: str | None = None
    qr_code: str | None = None
    started_at: datetime | None = None
    ended_at: datetime | None = None
    valid_from_time: time | None = None
    valid_until_time: time | None = None

class JoinRoomRequest(msgspec.Struct):
    invitation_code: str

class MemberResponse(msgspec.Struct):
    message: str
    room_id: str | None = None