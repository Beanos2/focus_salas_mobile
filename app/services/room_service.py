from uuid import UUID
from datetime import datetime, timezone
from litestar.exceptions import NotFoundException, PermissionDeniedException
from app.models.room import RoomModel
from app.domain.structs import RoomCreate, RoomResponse
from app.repositories.room_repository import RoomRepository

async def create_new_room(
    data: RoomCreate,
    creator_id: UUID,
    room_repo: RoomRepository,
    invitation_code: str
) -> RoomResponse:
    new_room = RoomModel(
        name=data.name,
        description=data.description,
        capacity=data.capacity,
        creator_id=creator_id,
        invitation_code=invitation_code,
        status="active",
        xp_multiplier=data.xp_multiplier,
        started_at=datetime.now(timezone.utc)
    )
    created = await room_repo.add(new_room, auto_commit=True)
    return _to_response(created)

async def get_all_rooms(
    room_repo: RoomRepository
) -> list[RoomResponse]:
    result = await room_repo.get_many()
    return [_to_response(r) for r in result]

async def get_room_by_id(
    room_id: UUID,
    room_repo: RoomRepository
) -> RoomResponse:
    r = await room_repo.get(room_id)
    return _to_response(r)

async def end_room(
    room_id: UUID,
    creator_id: UUID,
    room_repo: RoomRepository
) -> RoomResponse:
    room = await room_repo.get(room_id)

    if not room:
        raise NotFoundException("Sala no encontrada.")
    if str(room.creator_id) != str(creator_id):
        raise PermissionDeniedException("Solo el DM puede cerrar la sala.")
    if room.status != "active":
        raise PermissionDeniedException("La sala ya está cerrada.")

    room.status = "closed"
    room.ended_at = datetime.now(timezone.utc)
    updated = await room_repo.update(room, auto_commit=True)
    return _to_response(updated)

def _to_response(r: RoomModel, qr_code: str | None = None) -> RoomResponse:
    return RoomResponse(
        id=r.id,
        name=r.name,
        description=r.description,
        capacity=r.capacity,
        creator_id=r.creator_id,
        status=r.status,
        xp_multiplier=r.xp_multiplier,
        invitation_code=r.invitation_code,
        qr_code=qr_code,
        started_at=r.started_at,
        ended_at=r.ended_at
    )