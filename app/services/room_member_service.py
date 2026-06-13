import random
import string
import qrcode
import io
import base64
from uuid import UUID
from litestar.exceptions import NotFoundException, ClientException
from app.models.room_member import RoomMemberModel
from app.repositories.room_repository import RoomRepository
from app.repositories.room_member_repository import RoomMemberRepository

def generate_invitation_code(length: int = 8) -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def generate_qr_base64(data: str) -> str:
    qr = qrcode.make(data)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

async def join_room(
    invitation_code: str,
    user_id: UUID,
    room_repo: RoomRepository,
    member_repo: RoomMemberRepository
) -> dict:
    result = await room_repo.get_many()
    rooms = list(result)
    room = next((r for r in rooms if r.invitation_code == invitation_code), None)

    if not room:
        raise NotFoundException("Sala no encontrada con ese código.")

    room_id = room.id  # guardamos antes de que la sesión cierre

    members_result = await member_repo.get_many()
    members = list(members_result)
    already_in = next((m for m in members if m.room_id == room_id and m.user_id == user_id), None)

    if already_in:
        raise ClientException("Ya estás en esta sala.")

    member = RoomMemberModel(room_id=room_id, user_id=user_id)
    await member_repo.add(member, auto_commit=True)

    return {"message": "Te uniste a la sala exitosamente", "room_id": str(room_id)}

async def leave_room(
    room_id: UUID,
    user_id: UUID,
    member_repo: RoomMemberRepository
) -> dict:
    result = await member_repo.get_many()
    members = list(result)
    member = next((m for m in members if m.room_id == room_id and m.user_id == user_id), None)

    if not member:
        raise NotFoundException("No estás en esta sala.")

    await member_repo.delete(member.id, auto_commit=True)
    return {"message": "Saliste de la sala exitosamente"}