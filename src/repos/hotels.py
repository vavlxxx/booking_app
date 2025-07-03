from datetime import date
from sqlalchemy import select, func

from src.models.hotels import HotelsOrm

from src.repos.base import BaseRepository
from src.repos.utils import rooms_data_to_booking
from src.repos.mappers.mappers import HotelsMapper


class HotelsRepository(BaseRepository):

    model = HotelsOrm
    mapper = HotelsMapper

    async def get_all_filtered_by_time(
            self, 
            date_to: date, 
            date_from: date,
            limit: int, 
            offset: int,
            location: str | None = None,
            title: str | None = None,
    ):
        rooms_data_to_get = rooms_data_to_booking(date_from=date_from, date_to=date_to)
        hotels_ids_to_get = (
            select(rooms_data_to_get.c.hotel_id).distinct()
            .select_from(rooms_data_to_get)
        )
        hotels = select(self.model).filter(HotelsOrm.id.in_(hotels_ids_to_get))
        
        if location:
            hotels = hotels.filter(
                func
                .lower(HotelsOrm.location)
                .contains(location.strip().lower())
            )
        if title:
            hotels = hotels.filter(
                func
                .lower(HotelsOrm.title)
                .contains(title.strip().lower())
            )

        hotels = hotels.limit(limit).offset(offset)
        result = await self.session.execute(hotels)
        filtered_hotels_data = [self.mapper.map_to_domain_entity(hotel) for hotel in result.scalars().all()]
        return filtered_hotels_data
