from src.repos.additionals import AdditionalsRepository, RoomsAdditionalsRepository
from src.repos.hotels import HotelsRepository
from src.repos.auth import AuthRepository
from src.repos.rooms import RoomsRepository
from src.repos.bookings import BookingsRepository


class DBManager:

    def __init__(self, session_factory) -> None:
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        self.hotels = HotelsRepository(self.session)
        self.auth = AuthRepository(self.session)
        self.rooms = RoomsRepository(self.session)
        self.bookings = BookingsRepository(self.session)
        self.additionals = AdditionalsRepository(self.session)
        self.rooms_additionals = RoomsAdditionalsRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
