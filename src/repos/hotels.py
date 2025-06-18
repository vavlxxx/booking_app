from datetime import date
from fastapi import HTTPException
from sqlalchemy import delete, select, func

from src.models.rooms import RoomsOrm
from src.schemas.hotels import Hotel
from src.models.hotels import HotelsOrm
from src.repos.base import BaseRepository
from src.repos.utils import rooms_data_to_booking


class HotelsRepository(BaseRepository):

    model = HotelsOrm
    schema = Hotel
    not_found_message = "Отель по заданному id не найден"


    async def delete(self, **filter_by):
        from src.repos.rooms import RoomsRepository
        
        await self.check_existence(**filter_by)
        rooms = await RoomsRepository(self.session).get_all_filtered(hotel_id=filter_by["id"])
        if rooms:
            raise HTTPException(status_code=400, detail="Нельзя удалить отель с номерами")

        delete_obj_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_obj_stmt)


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
        filtered_hotels_data = [self.schema.model_validate(hotel) for hotel in result.scalars().all()]

        if not filtered_hotels_data:
            raise HTTPException(status_code=404, detail="По запрашиваемым данным отелей не найдено")
        return filtered_hotels_data
