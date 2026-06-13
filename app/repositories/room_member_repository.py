from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from app.models.room_member import RoomMemberModel

class RoomMemberRepository(SQLAlchemyAsyncRepository[RoomMemberModel]):
    model_type = RoomMemberModel