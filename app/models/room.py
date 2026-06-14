from sqlalchemy.orm import Mapped, mapped_column
from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import String, Integer, Uuid, DateTime, Float
from uuid import UUID
from datetime import datetime

class RoomModel(UUIDAuditBase):
    __tablename__ = "rooms"

    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    capacity: Mapped[int] = mapped_column(Integer, default=5)
    creator_id: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    status: Mapped[str] = mapped_column(String, default="active")
    invitation_code: Mapped[str] = mapped_column(String(8), nullable=True, unique=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    ended_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    xp_multiplier: Mapped[float] = mapped_column(Float, default=1.3)