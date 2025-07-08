from typing import cast
from fastapi import APIRouter, Body, HTTPException

from src.schemas.bookings import BookingAdd, BookingRequest
from src.schemas.rooms import FullRoomData
from src.helpers.bookings import BOOKING_EXAMPLES

from src.dependencies.db import DBDep
from src.dependencies.auth import UserIdDep
from src.utils.exceptions import AllRoomsAreBookedException, ObjectNotFoundException

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("/", summary="Добавить новое бронирование")
async def create_booking(
    db: DBDep,
    user_id: UserIdDep,
    booking_data: BookingRequest = Body(
        description="Данные о бронировании", 
        openapi_examples=BOOKING_EXAMPLES
)): 
    try:
        room: FullRoomData = await db.rooms.get_one(
            id=booking_data.room_id
        ) # type: ignore
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Номер не найден")

    room = cast(FullRoomData, room)

    _booking_data = BookingAdd(
        **booking_data.model_dump(), 
        user_id=user_id,
        price=room.discounted_price
    )

    try:
        booking = await db.bookings.add_booking(
            booking_data=_booking_data,
            hotel_id=room.hotel_id
        )
    except AllRoomsAreBookedException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    
    await db.commit()
    return booking


@router.get("/me", summary="Получить все бронирования аутентифицированного пользователя")
async def get_user_bookings(
    db: DBDep,
    user_id: UserIdDep
):
    bookings = await db.bookings.get_all_filtered(
        user_id=user_id
    )
    return bookings


@router.get("/", summary="Получить список бронирований")
async def get_all_bookings(
    db: DBDep
):
    bookings = await db.bookings.get_all()
    return bookings
