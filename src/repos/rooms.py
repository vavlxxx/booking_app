from fastapi import HTTPException
from sqlalchemy import insert

from src.repos.base import BaseRepository
from src.schemas.rooms import FullRoomData, Room
from src.models.rooms import RoomsOrm


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = FullRoomData
    not_found_message = "Номер по заданным id не найден"


    async def add(self, data: Room, hotel_id: int):
        from src.repos.hotels import HotelsRepository
        
        await HotelsRepository(self.session).check_existence(id=hotel_id)
        add_obj_stmt = insert(self.model).values(**data.model_dump(), hotel_id=hotel_id).returning(self.model)
        result = await self.session.execute(add_obj_stmt)
        obj = result.scalars().one()
        return self.schema.model_validate(obj)
    
    async def delete(self, **filter_by):
        from src.repos.bookings import BookingsRepository

        bookings = await BookingsRepository(self.session).get_all_filtered(room_id=filter_by["id"])
        if bookings:
            raise HTTPException(status_code=400, detail="Нельзя удалить номер с бронированиями")
        return await super().delete(**filter_by)