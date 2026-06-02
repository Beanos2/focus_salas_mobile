from uuid import UUID
from app.models.room import RoomModel
from app.domain.structs import RoomCreate
from app.repositories.room_repository import RoomRepository
from app.schemas.room import RoomSchema

async def create_new_room(data: RoomCreate, creator_id: str, room_repo: RoomRepository) -> RoomSchema:
    new_room = RoomModel(
        name=data.name,
        description=data.description,
        capacity=data.capacity,
        creator_id=creator_id
    )
    created = await room_repo.add(new_room, auto_commit=True)
    return RoomSchema(
        id=created.id,
        name=created.name,
        description=created.description,
        capacity=created.capacity,
        creator_id=created.creator_id,
        status=created.status
    )

async def get_all_rooms(room_repo: RoomRepository) -> list[RoomSchema]:
    rooms = await room_repo.list()
    return [
        RoomSchema(
            id=r.id,
            name=r.name,
            description=r.description,
            capacity=r.capacity,
            creator_id=r.creator_id,
            status=r.status
        ) for r in rooms
    ]

async def get_room_by_id(room_id: UUID, room_repo: RoomRepository) -> RoomSchema:
    r = await room_repo.get(room_id)
    return RoomSchema(
        id=r.id,
        name=r.name,
        description=r.description,
        capacity=r.capacity,
        creator_id=r.creator_id,
        status=r.status
    )