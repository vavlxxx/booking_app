from fastapi import APIRouter, Body, Path

from src.api.dependencies import RoomWithIdsDep, DBDep
from src.schemas.rooms import Room, RoomOptional
from src.helpers.rooms import ROOM_EXAMPLES

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получить все номера отеля")
async def get_rooms_by_hotel(
    db: DBDep,
    hotel_id: int = Path(description="ID отеля", example=1)
):
    rooms = await db.rooms.get_all_filtered(hotel_id=hotel_id)
    return rooms


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получить конкретный номер отеля")
async def get_room_by_id(
    room_ids: RoomWithIdsDep,
    db: DBDep 
):
    room = await db.rooms.check_existence(
        hotel_id=room_ids.hotel_id, 
        id=room_ids.id
    )
    return room


@router.post("/{hotel_id}/rooms", summary="Добавить номер для отеля")
async def create_room(
    db: DBDep,
    hotel_id: int = Path(description="ID отеля", example=1),
    room_data: Room = Body(
        description="Данные о номере отеля",
        openapi_examples=ROOM_EXAMPLES
)):
    room = await db.rooms.add(room_data, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK", "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удалить номер отеля")
async def delete_room(
    db: DBDep,
    room_ids: RoomWithIdsDep
):
    await db.rooms.delete(id=room_ids.id, hotel_id=room_ids.hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Обновить номер отеля")
async def update_hotel_put(
    db: DBDep,
    room_ids: RoomWithIdsDep, 
    room_data: Room = Body(
        description="Данные о номере отеля",
        openapi_examples=ROOM_EXAMPLES
    )
):
    await db.rooms.edit(
        room_data, 
        id=room_ids.id, 
        hotel_id=room_ids.hotel_id
    )
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частично обновить номер отеля")
async def update_hotel_patch(
    db: DBDep,
    room_ids: RoomWithIdsDep, 
    room_data: RoomOptional = Body(
        description="Данные о номере отеля",
        openapi_examples=ROOM_EXAMPLES
    )
):  
    await db.rooms.edit(
        room_data, 
        id=room_ids.id, 
        hotel_id=room_ids.hotel_id
    )
    await db.commit()
    return {"status": "OK"}
