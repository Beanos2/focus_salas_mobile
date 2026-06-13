from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Uuid, ForeignKey
from uuid import UUID

class RoomMemberModel(UUIDAuditBase):
    __tablename__ = "room_members"

    room_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("rooms.id"), nullable=False)
    user_id: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    role: Mapped[str] = mapped_column(String, default="student")