from datetime import date

from sqlalchemy import select, func

from src.repos.base import BaseRepository
from src.repos.mappers.mappers import BookingsMapper

from src.models.bookings import BookingsOrm


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingsMapper
    

    async def get_today_checkin(self):
        query = (
            select(self.model)
            .filter(self.model.date_from == date.today())
        )
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(obj) for obj in result.scalars().all()]