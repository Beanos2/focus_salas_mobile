import os
import pytest
from datetime import datetime, timedelta, timezone
from uuid import uuid4
from unittest.mock import patch as mock_patch, AsyncMock

from litestar import Litestar
from litestar.testing import TestClient
from litestar.di import Provide
from litestar.security.jwt import Token, JWTAuth
from typing import Any
from litestar.connection import ASGIConnection

from app.api.v1.roomsController import RoomsController
from app.schemas.room import RoomSchema
from app.repositories.room_repository import RoomRepository

TEST_SECRET = "clave_super_secreta_larga_32bytes!"

def create_test_token(role: str, user_id: str = "user-123"):
    token = Token(
        sub=user_id,
        exp=datetime.now(timezone.utc) + timedelta(hours=1),
        extras={"role": role},
    )
    return token.encode(secret=TEST_SECRET, algorithm="HS256")

async def retrieve_user_handler(token: Token, connection: ASGIConnection) -> dict[str, Any]:
    return {
        "sub": token.sub,
        "role": token.extras.get("role"),
    }

test_jwt_auth = JWTAuth[dict[str, Any]](
    retrieve_user_handler=retrieve_user_handler,
    token_secret=TEST_SECRET,
    exclude=["/schema"],
)

@pytest.fixture
def mock_repo():
    return AsyncMock(spec=RoomRepository)

@pytest.fixture
def client(mock_repo):
    test_app = Litestar(
        route_handlers=[RoomsController],
        on_app_init=[test_jwt_auth.on_app_init],
        dependencies={"room_repo": Provide(lambda: mock_repo, sync_to_thread=False)},
        debug=True,
    )
    with TestClient(app=test_app, raise_server_exceptions=True) as client:
        yield client

@mock_patch("app.api.v1.roomsController.create_new_room", new_callable=AsyncMock)
def test_create_room_endpoint(mock_create, client: TestClient) -> None:
    fake_uuid = uuid4()
    token = create_test_token(role="dm")

    mock_create.return_value = RoomSchema(
        id=fake_uuid,
        name="Sala de Estudio",
        description="Una sala tranquila",
        capacity=10,
        creator_id="user-123"
    )

    response = client.post(
        "/api/v1/rooms/",
        json={"name": "Sala de Estudio", "description": "Una sala tranquila", "capacity": 10},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Sala de Estudio"
    assert data["id"] == str(fake_uuid)

def test_create_room_forbidden_for_student(client: TestClient) -> None:
    token = create_test_token(role="student")

    response = client.post(
        "/api/v1/rooms/",
        json={"name": "Sala Prohibida", "capacity": 5},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403
    assert "Solo los Dungeon Masters" in response.json()["detail"]

@mock_patch("app.api.v1.roomsController.get_all_rooms", new_callable=AsyncMock)
def test_list_rooms_endpoint(mock_get_all, client: TestClient) -> None:
    mock_get_all.return_value = [RoomSchema(id=uuid4(), name="Sala 1", creator_id="1")]
    token = create_test_token(role="student")

    response = client.get("/api/v1/rooms/", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert len(response.json()) == 1

@mock_patch("app.api.v1.roomsController.get_room_by_id", new_callable=AsyncMock)
def test_get_single_room_endpoint(mock_get_by_id, client: TestClient) -> None:
    room_id = uuid4()
    mock_get_by_id.return_value = RoomSchema(id=room_id, name="Sala Única", creator_id="1")
    token = create_test_token(role="student")

    response = client.get(f"/api/v1/rooms/{room_id}", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json()["name"] == "Sala Única"