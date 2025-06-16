from fastapi import APIRouter, Body, HTTPException, Path

from src.api.dependencies import RoomWithIdsDep
from src.repos.rooms import RoomsRepository
from src.db import async_session_maker
from src.schemas.rooms import Room, RoomOptional
from src.helpers.rooms import ROOM_EXAMPLES

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получить все номера отеля")
async def get_rooms_by_hotel(hotel_id: int = Path(description="ID отеля", example=1)):
    async with async_session_maker() as session:
        rooms = await RoomsRepository(session).get_all(hotel_id=hotel_id)
    return rooms


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получить конкретный номер отеля")
async def get_room_by_id(
    room_ids: RoomWithIdsDep, 
):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).get_one_or_none(hotel_id=room_ids.hotel_id, id=room_ids.id)
        if room is None:
            raise HTTPException(status_code=404, detail="Такой номер не найден")
    return room


@router.post("/{hotel_id}/rooms", summary="Добавить номер для отеля")
async def create_room(
    hotel_id: int = Path(description="ID отеля", example=1),
    room_data: Room = Body(
        description="Данные о номере отеля",
        openapi_examples=ROOM_EXAMPLES
)):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data, hotel_id=hotel_id)
        await session.commit()
    return {"status": "OK", "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удалить номер отеля")
async def delete_room(room_ids: RoomWithIdsDep):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(
            id=room_ids.id, 
            hotel_id=room_ids.hotel_id
        )
        await session.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Обновить номер отеля")
async def update_hotel_put(
    room_ids: RoomWithIdsDep, 
    room_data: Room = Body(
        description="Данные о номере отеля",
        openapi_examples=ROOM_EXAMPLES
    )
):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, id=room_ids.id, hotel_id=room_ids.hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частично обновить номер отеля")
async def update_hotel_patch(
    room_ids: RoomWithIdsDep, 
    room_data: RoomOptional = Body(
        description="Данные о номере отеля",
        openapi_examples=ROOM_EXAMPLES
    )
):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, id=room_ids.id, hotel_id=room_ids.hotel_id)
        await session.commit()
    return {"status": "OK"}
