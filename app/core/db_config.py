import os
from dotenv import load_dotenv
from advanced_alchemy.extensions.litestar import SQLAlchemyPlugin, SQLAlchemyAsyncConfig

load_dotenv(override=True)

DATABASE_URL = os.getenv(
    "DATABASE_URL" 
)

db_config = SQLAlchemyAsyncConfig(
    connection_string= DATABASE_URL,
    create_all=True
)

db_plugin = SQLAlchemyPlugin(config=db_config)
