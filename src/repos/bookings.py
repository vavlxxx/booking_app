from src.repos.base import BaseRepository
from src.repos.rooms import RoomsRepository
from src.schemas.bookings import Booking, BookingWIthUser, BookingAdd
from src.models.bookings import BookingsOrm


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking
    not_found_message = "Бронирование по заданным id не найдено"

    async def add(self, data: BookingWIthUser):
        room = await RoomsRepository(self.session).check_existence(id=data.room_id)
        booking_to_add = BookingAdd(**data.model_dump(), price=room.discounted_price)
        booking = await super().add(booking_to_add)
        return booking