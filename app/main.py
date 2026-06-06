from litestar import Litestar
from litestar.di import Provide
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.roomsController import RoomsController
from app.repositories.room_repository import RoomRepository
from app.core.db_config import db_plugin
from app.core.security import jwt_auth
from app.core.exceptions import GLOBAL_EXCEPTION_HANDLERS

async def provide_room_repo(db_session: AsyncSession) -> RoomRepository:
    return RoomRepository(session=db_session)

app = Litestar(
    route_handlers=[
        RoomsController
    ],
    on_app_init=[jwt_auth.on_app_init],
    plugins=[db_plugin],
    dependencies={
        "room_repo": Provide(provide_room_repo)
    },
    exception_handlers=GLOBAL_EXCEPTION_HANDLERS,
    debug=False
)