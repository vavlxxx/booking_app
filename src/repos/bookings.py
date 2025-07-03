from src.repos.base import BaseRepository
from src.repos.mappers.mappers import BookingsMapper

from src.models.bookings import BookingsOrm


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingsMapper
    