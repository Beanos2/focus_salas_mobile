from sqlalchemy.orm import Mapped, mapped_column
from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import String, Integer

class RoomModel(UUIDAuditBase):
    __tablename__ = "rooms"

    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    capacity: Mapped[int] = mapped_column(Integer, default=5)
    # Aquí podrías guardar el ID del DM que la creó
    creator_id: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, default="active")