from fastapi import HTTPException
from sqlalchemy import delete, select, func

from src.schemas.hotels import Hotel
from src.models.hotels import HotelsOrm
from src.repos.base import BaseRepository


class HotelsRepository(BaseRepository):

    model = HotelsOrm
    schema = Hotel
    not_found_message = "Отель по заданному id не найден"

    async def get_all_filtered(self, location, title, limit, offset) -> list[Hotel]:
        query = select(self.model)

        if location:
            query = query.filter(
                func
                .lower(HotelsOrm.location)
                .contains(location.strip().lower())
            )
        if title:
            query = query.filter(
                func
                .lower(HotelsOrm.title)
                .contains(title.strip().lower())
            )

        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        hotels = [self.schema.model_validate(hotel) for hotel in result.scalars().all()]

        if not hotels:
            raise HTTPException(status_code=404, detail="По запрашиваемым данным отелей не найдено")
        return hotels
    

    async def delete(self, **filter_by):
        from src.repos.rooms import RoomsRepository
        
        await self.check_existence(**filter_by)
        rooms = await RoomsRepository(self.session).get_all_filtered(hotel_id=filter_by["id"])
        if rooms:
            raise HTTPException(status_code=400, detail="Нельзя удалить отель с номерами")

        delete_obj_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_obj_stmt)
    