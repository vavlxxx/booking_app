from fastapi import APIRouter, Body

from src.schemas.bookings import BookingRequest
from src.helpers.bookings import BOOKING_EXAMPLES
from src.services.bookings import BookingsService
from src.dependencies.db import DBDep
from src.dependencies.auth import UserIdDep
from src.utils.exceptions import (
    AllRoomsAreBookedException,
    AllRoomsAreBookedHTTPException,
    BookingStartDateException,
    BookingStartDateHTTPException,
    DatesMissMatchException,
    DatesMissMatchHTTPException,
    RoomNotFoundException,
    RoomNotFoundHTTPException,
    InvalidDataHTTPException,
    InvalidDataException
)

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
        booking = await BookingsService(db).add_booking(booking_data, user_id)
    except BookingStartDateException as exc:
        raise BookingStartDateHTTPException from exc
    except DatesMissMatchException as exc:
        raise DatesMissMatchHTTPException from exc
    except RoomNotFoundException as exc:
        raise RoomNotFoundHTTPException from exc
    except AllRoomsAreBookedException as exc:
        raise AllRoomsAreBookedHTTPException from exc 
    except InvalidDataException as exc:
        raise InvalidDataHTTPException from exc
    
    return {
        "detail": "Бронирование было успешно добавлено",
        "data": booking
    }


@router.get("/me", summary="Получить все бронирования аутентифицированного пользователя")
async def get_user_bookings(
    db: DBDep,
    user_id: UserIdDep
):
    bookings = await BookingsService(db).get_user_bookings(user_id=user_id)
    return {
        "detail": "Бронирования пользователя были успешно получены" if bookings else "Бронирования пользователя не найдены",
        "data": bookings
    }


@router.get("/", summary="Получить список бронирований")
async def get_all_bookings(
    db: DBDep
):  
    bookings = await BookingsService(db).get_all_bookings()
    return {
        "detail": "Бронирования были успешно получены" if bookings else "Бронирований не найдено",
        "data": bookings
    }
