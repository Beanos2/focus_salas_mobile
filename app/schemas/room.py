import msgspec
from uuid import UUID

class RoomSchema(msgspec.Struct):
    id: UUID
    name: str
    creator_id: str
    description: str | None = None
    capacity: int = 5
    status: str = "active"