from typing import Annotated
from uuid import UUID
from litestar import Controller, post, get, Request, params
from litestar.exceptions import PermissionDeniedException
from app.domain.structs import RoomCreate
from app.services.room_service import create_new_room, get_all_rooms, get_room_by_id
from app.repositories.room_repository import RoomRepository
from app.schemas.room import RoomSchema

class RoomsController(Controller):
    path = "/api/v1/rooms"

    @post("/", status_code=201)
    async def create_room(
        self,
        data: RoomCreate,
        room_repo: RoomRepository,
        request: Request
    ) -> RoomSchema:
        user_data = request.user
        if user_data.get("role") != "dm":
            raise PermissionDeniedException("Solo los Dungeon Masters pueden crear salas.")
        creator_id = user_data.get("sub")
        return await create_new_room(data, creator_id, room_repo)

    @get("/")
    async def list_rooms(
        self,
        room_repo: RoomRepository,
    ) -> list[RoomSchema]:
        return await get_all_rooms(room_repo)

    @get("/{room_id:uuid}")
    async def get_room(
        self,
        room_id: Annotated[UUID, params.Parameter()],
        room_repo: RoomRepository,
    ) -> RoomSchema:
        return await get_room_by_id(room_id, room_repo)