import logging

from datetime import date

from asyncpg import DataError

from sqlalchemy import select, func
from sqlalchemy.exc import DBAPIError

from src.models.hotels import HotelsOrm
from src.repos.base import BaseRepository
from src.repos.utils import rooms_data_to_booking
from src.repos.mappers.mappers import HotelsMapper
from src.utils.exceptions import (
    DatesMissMatchException,
    InvalidDataException
)


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
        
        if date_from >= date_to:
            raise DatesMissMatchException

        rooms_data_to_get = rooms_data_to_booking(date_from=date_from, date_to=date_to)
        hotels_ids_to_get = (
            select(rooms_data_to_get.selected_columns.hotel_id).distinct()
            .select_from(rooms_data_to_get) # type: ignore
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

        try:
            result = await self.session.execute(hotels)
        except DBAPIError as exc:
            logging.error(f"Cannot get data from DB, exc_type={exc.orig}")
            if isinstance(exc.orig.__cause__, DataError): # type: ignore
                raise InvalidDataException  from exc
            logging.error(f"Unknown unhandled exception")
            raise

        filtered_hotels_data = [self.mapper.map_to_domain_entity(hotel) for hotel in result.scalars().all()]
        return filtered_hotels_data
