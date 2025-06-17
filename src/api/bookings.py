from fastapi import APIRouter, Body

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingRequest, BookingWIthUser
from src.helpers.bookings import BOOKING_EXAMPLES

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("/", summary="Добавить новое бронирование")
async def create_booking(
    db: DBDep,
    user_id: UserIdDep,
    booking_data: BookingRequest = Body(
        description="Данные о бронировании", 
        openapi_examples=BOOKING_EXAMPLES
)):  
    new_booking_data = BookingWIthUser(**booking_data.model_dump(), user_id=user_id)
    booking = await db.bookings.add(new_booking_data)
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
