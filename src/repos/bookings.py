from src.repos.base import BaseRepository
from src.repos.rooms import RoomsRepository
from src.schemas.bookings import Booking, BookingWIthUser, BookingAdd
from src.models.bookings import BookingsOrm


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking
    