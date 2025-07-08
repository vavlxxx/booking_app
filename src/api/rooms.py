from fastapi import APIRouter, Body, Path
from fastapi.exceptions import HTTPException

from src.schemas.rooms import (
    RoomAdd, 
    RoomRequest, 
    FullRoomOptional, 
    FullRoomData,
    RoomsWithRels
)
from src.schemas.additionals import RoomsAdditionalsRequest
from src.helpers.rooms import ROOM_EXAMPLES
from src.dependencies.rooms import RoomWithIdsDep, DateDep
from src.dependencies.db import DBDep
from src.utils.exceptions import DatesMissMatchException, ObjectNotFoundException


router = APIRouter(
    prefix="/hotels", 
    tags=["Номера"]
)


@router.get("/{hotel_id}/rooms", summary="Получить все доступные номера отеля за указанный период")
async def get_rooms_by_hotel(
    db: DBDep,
    dates: DateDep,
    hotel_id: int = Path(description="ID отеля")
):  
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Отель не найден")

    try:
        rooms = await db.rooms.get_all_filtered_by_time(
            hotel_id=hotel_id,
            date_from=dates.date_from,
            date_to=dates.date_to
        )
    except DatesMissMatchException as ex:
        raise HTTPException(status_code=422, detail=ex.detail)
    return rooms


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получить данные конкретного номера отеля")
async def get_room_by_id(
    db: DBDep,
    ids: RoomWithIdsDep
):  
    try:
        await db.hotels.get_one(id=ids.hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Отель не найден")

    try:
        room: RoomsWithRels | None = await db.rooms.get_one_with_rel(
            hotel_id=ids.hotel_id, 
            id=ids.room_id
        )
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Номер в указанном отеле не найден")
    return room


@router.post("/{hotel_id}/rooms", summary="Добавить номер для отеля")
async def create_room(
    db: DBDep,
    hotel_id: int = Path(description="ID отеля"),
    room_data: RoomRequest = Body(
        description="Данные о номере отеля",
        openapi_examples=ROOM_EXAMPLES
)): 
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Отель не найден")

    _room_data = RoomAdd(**room_data.model_dump(exclude={"additionals_ids"}), hotel_id=hotel_id)
    room: FullRoomData = await db.rooms.add(_room_data) # type: ignore

    additionals = [
        RoomsAdditionalsRequest(
            additional_id=addit_id, 
            room_id=room.id
        ) for addit_id in room_data.additionals_ids] # type: ignore

    if additionals:
        await db.rooms_additionals.add_bulk(additionals)

    await db.commit()
    return {"status": "OK", "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удалить номер отеля")
async def delete_room(
    db: DBDep,
    ids: RoomWithIdsDep
):
    try:
        await db.hotels.get_one(id=ids.hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Отель не найден")
    
    try:
        await db.rooms.get_one(id=ids.room_id, hotel_id=ids.hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Номер в указанном отеле не найден")

    await db.rooms.delete(id=ids.room_id, hotel_id=ids.hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Обновить номер отеля")
async def update_room_put(
    db: DBDep,
    ids: RoomWithIdsDep, 
    room_data: RoomRequest = Body(
        description="Данные о номере отеля",
        openapi_examples=ROOM_EXAMPLES
    )
):  
    try:
        await db.rooms.get_one(id=ids.room_id, hotel_id=ids.hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Номер не найден")

    await db.rooms.edit(
        room_data, 
        id=ids.room_id, 
        hotel_id=ids.hotel_id,
        exclude_fields={"additionals_ids"}
    )
    await db.rooms_additionals.update_all(
        room_id=ids.room_id, 
        additionals_ids=room_data.additionals_ids
    )
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частично обновить номер отеля")
async def update_room_patch(
    db: DBDep,
    ids: RoomWithIdsDep, 
    room_data: FullRoomOptional = Body(
        description="Данные о номере отеля",
        openapi_examples=ROOM_EXAMPLES
    )
):  
    try:
        await db.rooms.get_one(id=ids.room_id, hotel_id=ids.hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Номер не найден")

    await db.rooms.edit(
        room_data, 
        id=ids.room_id, 
        hotel_id=ids.hotel_id,
        exclude_fields={"additionals_ids"}
    )
    _room_data = room_data.model_dump(exclude_unset=True)
    if "additionals_ids" in _room_data:
        await db.rooms_additionals.update_all(
            room_id=ids.room_id, 
            additionals_ids=room_data.additionals_ids
        )
    await db.commit()
    return {"status": "OK"}
