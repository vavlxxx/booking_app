import logging

from asyncpg import DataError

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import DBAPIError

from src.repos.base import BaseRepository
from src.repos.mappers.mappers import RoomsMapper, RoomsRelsMapper
from src.schemas.rooms import RoomsWithRels
from src.models.rooms import RoomsOrm
from src.repos.utils import rooms_data_to_booking
from src.utils.exceptions import (
    DatesMissMatchException, 
    ObjectNotFoundException,
    InvalidDataException
)

class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomsMapper


    async def get_all_filtered_by_time(self, hotel_id, date_from, date_to):

        if date_from >= date_to:
            raise DatesMissMatchException
        
        empty_rooms_data_to_get = rooms_data_to_booking(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            .select_from(self.model)
            .options(joinedload(self.model.additionals)) # type: ignore
            .filter(self.model.id.in_( # type: ignore
                    select(empty_rooms_data_to_get.c.id)
                    .select_from(empty_rooms_data_to_get) # type: ignore
                )
            )
        )
        result = await self.session.execute(query)
        return [RoomsRelsMapper.map_to_domain_entity(obj) for obj in result.unique().scalars().all()]
    

    async def get_one_or_none_with_rel(self, **filter_by) -> RoomsWithRels | None:
        query = (
            select(self.model)
            .filter_by(**filter_by)
            .options(joinedload(self.model.additionals)) # type: ignore
        )
        
        try:
            result = await self.session.execute(query)
        except DBAPIError as exc:
            logging.error(f"Cannot get data from DB, {filter_by=}, exc_type={exc.orig}")
            if isinstance(exc.orig.__cause__, DataError): # type: ignore
                raise InvalidDataException from exc 
            logging.error(f"Unknown unhandled exception")
            raise exc
        obj = result.scalars().unique().one_or_none()
        if obj is None:
            return None
        
        return RoomsRelsMapper.map_to_domain_entity(obj) # type: ignore
    
    
    async def get_one_with_rel(self, **filter_by) -> RoomsWithRels:
        result = await self.get_one_or_none_with_rel(**filter_by)
        if result is None:
            raise ObjectNotFoundException
        return result
    