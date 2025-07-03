from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.repos.base import BaseRepository
from src.repos.mappers.mappers import RoomsMapper, RoomsRelsMapper

from src.models.rooms import RoomsOrm
from src.repos.utils import rooms_data_to_booking


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomsMapper


    async def get_all_filtered_by_time(self, hotel_id, date_from, date_to):
        empty_rooms_data_to_get = rooms_data_to_booking(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            .select_from(self.model)
            .options(joinedload(self.model.additionals))
            .filter(self.model.id.in_(
                    select(empty_rooms_data_to_get.c.id)
                    .select_from(empty_rooms_data_to_get)
                )
            )
        )
        result = await self.session.execute(query)
        return [RoomsRelsMapper.map_to_domain_entity(obj) for obj in result.unique().scalars().all()]
    

    async def get_one_or_none_with_rel(self, **filter_by):
        query = (
            select(self.model)
            .filter_by(**filter_by)
            .options(joinedload(self.model.additionals))
        )
        
        result = await self.session.execute(query)
        obj = result.scalars().unique().one_or_none()
        if obj is None:
            return None
        
        return RoomsRelsMapper.map_to_domain_entity(obj)
    