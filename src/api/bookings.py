from fastapi import APIRouter, Body

from src.schemas.bookings import BookingAdd, BookingRequest
from src.helpers.bookings import BOOKING_EXAMPLES

from src.dependencies.db import DBDep
from src.dependencies.auth import UserIdDep

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("/", summary="Добавить новое бронирование")
async def create_booking(
    db: DBDep,
    user_id: UserIdDep,
    booking_data: BookingRequest = Body(
        description="Данные о бронировании", 
        openapi_examples=BOOKING_EXAMPLES
)): 
    room = await db.rooms.get_one_or_none(
        id=booking_data.room_id
    )

    _booking_data = BookingAdd(
        **booking_data.model_dump(), 
        user_id=user_id,
        price=room.discounted_price
    )

    booking = await db.bookings.add(_booking_data)
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
