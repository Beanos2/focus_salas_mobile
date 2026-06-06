import pytest
from uuid import uuid4
from unittest.mock import AsyncMock
from app.services.room_service import create_new_room, get_all_rooms, get_room_by_id
from app.models.room import RoomModel
from app.domain.structs import RoomCreate, RoomResponse 

@pytest.mark.asyncio
async def test_create_new_room_service():
    mock_repo = AsyncMock()
    data = RoomCreate(name="Sala de Prueba", description="Descripción", capacity=5)
    creator_id = uuid4()

    fake_room = RoomModel()
    fake_room.id = uuid4()
    fake_room.name = "Sala de Prueba"
    fake_room.description = "Descripción"
    fake_room.capacity = 5
    fake_room.creator_id = creator_id
    fake_room.status = "active"

    mock_repo.add.return_value = fake_room

    result = await create_new_room(data, creator_id, mock_repo)

    assert isinstance(result, RoomResponse)
    assert result.name == "Sala de Prueba"
    assert result.creator_id == creator_id
    assert result.capacity == 5
    mock_repo.add.assert_called_once()

@pytest.mark.asyncio
async def test_get_all_rooms_service():
    mock_repo = AsyncMock()

    fake_room = RoomModel()
    fake_room.id = uuid4()
    fake_room.name = "Sala 1"
    fake_room.description = None
    fake_room.capacity = 5
    fake_room.creator_id = uuid4()
    fake_room.status = "active"

    mock_repo.list.return_value = [fake_room]

    result = await get_all_rooms(mock_repo)

    assert len(result) == 1
    assert isinstance(result[0], RoomResponse)
    assert result[0].name == "Sala 1"

@pytest.mark.asyncio
async def test_get_room_by_id_service():
    mock_repo = AsyncMock()
    room_id = uuid4()

    fake_room = RoomModel()
    fake_room.id = room_id
    fake_room.name = "Sala VIP"
    fake_room.description = None
    fake_room.capacity = 5
    fake_room.creator_id = uuid4()
    fake_room.status = "active"

    mock_repo.get.return_value = fake_room

    result = await get_room_by_id(room_id, mock_repo)

    assert isinstance(result, RoomResponse)
    assert result.id == room_id
    assert result.name == "Sala VIP"