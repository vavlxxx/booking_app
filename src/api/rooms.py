from fastapi import APIRouter, Body, Path

from src.schemas.rooms import RoomRequest, FullRoomOptional
from src.services.rooms import RoomsService
from src.helpers.rooms import ROOM_EXAMPLES
from src.dependencies.rooms import RoomWithIdsDep, DateDep
from src.dependencies.db import DBDep

from src.utils.exceptions import (
    AdditionalNotFoundHTTPException,
    AdditionalNotFoundException,
    BookingStartDateException,
    BookingStartDateHTTPException,
    DatesMissMatchException,
    DatesMissMatchHTTPException,
    HotelNotFoundException,
    ObjectAlreadyExistsException,
    RoomAlreadyExistsHTTPException,
    RoomNotFoundException,
    RoomNotFoundHTTPException,
    HotelNotFoundHTTPException,
    InvalidDataHTTPException,
    InvalidDataException,
)


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получить все доступные номера отеля за указанный период")
async def get_rooms_by_hotel(
    db: DBDep, dates: DateDep, hotel_id: int = Path(description="ID отеля")
):
    try:
        rooms = await RoomsService(db).get_rooms(hotel_id=hotel_id, dates=dates)
    except HotelNotFoundException as exc:
        raise HotelNotFoundHTTPException from exc
    except BookingStartDateException as exc:
        raise BookingStartDateHTTPException from exc
    except DatesMissMatchException as exc:
        raise DatesMissMatchHTTPException from exc
    except InvalidDataException as exc:
        raise InvalidDataHTTPException from exc
    return rooms


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получить данные конкретного номера отеля")
async def get_room_by_id(db: DBDep, ids: RoomWithIdsDep):
    try:
        room = await RoomsService(db).get_room(ids.room_id, ids.hotel_id)
    except HotelNotFoundException as exc:
        raise HotelNotFoundHTTPException from exc
    except RoomNotFoundException as exc:
        raise RoomNotFoundHTTPException from exc
    except InvalidDataException as exc:
        raise InvalidDataHTTPException from exc
    return room


@router.post("/{hotel_id}/rooms", summary="Добавить номер для отеля")
async def create_room(
    db: DBDep,
    hotel_id: int = Path(description="ID отеля"),
    room_data: RoomRequest = Body(
        description="Данные о номере отеля", openapi_examples=ROOM_EXAMPLES
    ),
):
    try:
        room = await RoomsService(db).add_room(room_data, hotel_id)
    except ObjectAlreadyExistsException as exc:
        raise RoomAlreadyExistsHTTPException from exc
    except AdditionalNotFoundException as exc:
        raise AdditionalNotFoundHTTPException from exc
    except HotelNotFoundException as exc:
        raise HotelNotFoundHTTPException from exc
    except RoomNotFoundException as exc:
        raise RoomNotFoundHTTPException from exc
    except InvalidDataException as exc:
        raise InvalidDataHTTPException from exc
    return room


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удалить номер отеля")
async def delete_room(db: DBDep, ids: RoomWithIdsDep):
    try:
        await RoomsService(db).delete_room(ids.room_id, ids.hotel_id)
    except HotelNotFoundException as exc:
        raise HotelNotFoundHTTPException from exc
    except RoomNotFoundException as exc:
        raise RoomNotFoundHTTPException from exc
    except InvalidDataException as exc:
        raise InvalidDataHTTPException from exc
    return {"status": "OK"}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Обновить номер отеля")
async def update_room_put(
    db: DBDep,
    ids: RoomWithIdsDep,
    room_data: RoomRequest = Body(
        description="Данные о номере отеля", openapi_examples=ROOM_EXAMPLES
    ),
):
    try:
        await RoomsService(db).edit_room(room_data, ids.room_id, ids.hotel_id)
    except ObjectAlreadyExistsException as exc:
        raise RoomAlreadyExistsHTTPException from exc
    except AdditionalNotFoundException as exc:
        raise AdditionalNotFoundHTTPException from exc
    except HotelNotFoundException as exc:
        raise HotelNotFoundHTTPException from exc
    except RoomNotFoundException as exc:
        raise RoomNotFoundHTTPException from exc
    except InvalidDataException as exc:
        raise InvalidDataHTTPException from exc
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частично обновить номер отеля")
async def update_room_patch(
    db: DBDep,
    ids: RoomWithIdsDep,
    room_data: FullRoomOptional = Body(
        description="Данные о номере отеля", openapi_examples=ROOM_EXAMPLES
    ),
):
    try:
        await RoomsService(db).edit_room(room_data, ids.room_id, ids.hotel_id)
    except ObjectAlreadyExistsException as exc:
        raise RoomAlreadyExistsHTTPException from exc
    except AdditionalNotFoundException as exc:
        raise AdditionalNotFoundHTTPException from exc
    except HotelNotFoundException as exc:
        raise HotelNotFoundHTTPException from exc
    except RoomNotFoundException as exc:
        raise RoomNotFoundHTTPException from exc
    except InvalidDataException as exc:
        raise InvalidDataHTTPException from exc
    return {"status": "OK"}
