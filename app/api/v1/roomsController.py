from typing import Annotated
from uuid import UUID
from litestar import Controller, post, get, delete, Request, params
from litestar.exceptions import PermissionDeniedException
from litestar.response import Response
from app.services.room_service import create_new_room, get_all_rooms, get_room_by_id
from app.services.room_member_service import (
    generate_invitation_code, generate_qr_base64,
    join_room, leave_room
)
from app.repositories.room_repository import RoomRepository
from app.repositories.room_member_repository import RoomMemberRepository
from app.domain.structs import RoomResponse, RoomCreate, JoinRoomRequest, MemberResponse

class RoomsController(Controller):
    path = "/api/v1/rooms"

    @post("/", status_code=201)
    async def create_room(
        self,
        data: RoomCreate,
        room_repo: RoomRepository,
        request: Request
    ) -> RoomResponse:
        user_data = request.user
        if not isinstance(user_data, dict) or user_data.get("role") != "dm":
            raise PermissionDeniedException("Solo los Dungeon Masters pueden crear salas.")
        
        creator_id = UUID(str(user_data.get("sub")))
        invitation_code = generate_invitation_code()
        qr_code = generate_qr_base64(invitation_code)

        room = await create_new_room(data, creator_id, room_repo, invitation_code)
        room.qr_code = qr_code
        return room

    @get("/")
    async def list_rooms(
        self,
        room_repo: RoomRepository,
    ) -> list[RoomResponse]:
        return await get_all_rooms(room_repo)

    @get("/{room_id:uuid}")
    async def get_room(
        self,
        room_id: Annotated[UUID, params.Parameter()],
        room_repo: RoomRepository,
    ) -> RoomResponse:
        return await get_room_by_id(room_id, room_repo)

    @post("/{room_id:uuid}/join", status_code=200)
    async def join_room(
        self,
        data: JoinRoomRequest,
        room_repo: RoomRepository,
        member_repo: RoomMemberRepository,
        request: Request
    ) -> MemberResponse:
        user_data = request.user
        user_id = UUID(str(user_data.get("sub")))
        result = await join_room(data.invitation_code, user_id, room_repo, member_repo)
        return MemberResponse(**result)

    @delete("/{room_id:uuid}/leave", status_code=200)
    async def leave_room(
        self,
        room_id: Annotated[UUID, params.Parameter()],
        member_repo: RoomMemberRepository,
        request: Request
    ) -> MemberResponse:
        user_data = request.user
        user_id = UUID(str(user_data.get("sub")))
        result = await leave_room(room_id, user_id, member_repo)
        return MemberResponse(**result)