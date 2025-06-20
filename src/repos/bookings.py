from src.repos.base import BaseRepository
from src.schemas.bookings import Booking
from src.models.bookings import BookingsOrm


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking
    