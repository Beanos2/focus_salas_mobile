from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from app.models.room import RoomModel

class RoomRepository(SQLAlchemyAsyncRepository[RoomModel]):
    model_type = RoomModel