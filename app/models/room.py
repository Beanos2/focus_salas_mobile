from sqlalchemy.orm import Mapped, mapped_column
from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import String, Integer, Uuid
from uuid import UUID

class RoomModel(UUIDAuditBase):
    __tablename__ = "rooms"

    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    capacity: Mapped[int] = mapped_column(Integer, default=5)
    creator_id: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    status: Mapped[str] = mapped_column(String, default="active")