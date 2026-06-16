import os
from dotenv import load_dotenv
from advanced_alchemy.extensions.litestar import SQLAlchemyPlugin, SQLAlchemyAsyncConfig
from app.models.base import Base
from app.models.room import RoomModel
from app.models.room_member import RoomMemberModel

load_dotenv(override=True)

DATABASE_URL = os.getenv(
    "DATABASE_URL" 
)

db_config = SQLAlchemyAsyncConfig(
    connection_string= DATABASE_URL,
    create_all=True,
    metadata=Base.metadata
)

db_plugin = SQLAlchemyPlugin(config=db_config)
