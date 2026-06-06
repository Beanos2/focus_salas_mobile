import os
from typing import Any
from dotenv import load_dotenv
from litestar.security.jwt import JWTAuth, Token
from litestar.connection import ASGIConnection

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "clave_super_secreta")

async def retrieve_user_handler(token: Token, connection: ASGIConnection) -> dict[str, Any]:
    extras = token.extras or {} 
    return {
        "sub": token.sub,
        "role": extras.get("role", "student"),
    }

jwt_auth = JWTAuth[dict[str, Any]](
    retrieve_user_handler=retrieve_user_handler,
    token_secret=SECRET_KEY,
    exclude=[
        "/schema",
        "/schema/swagger",
        "/schema/openapi.json",
        "/schema/redoc",
    ],
)