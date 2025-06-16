from fastapi import HTTPException
from sqlalchemy import delete, insert

from src.repos.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import FullRoomData, Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = FullRoomData
    not_found_message = "Номер по заданным id не найден"

    async def add(self, data: Room, hotel_id: int):
        from src.repos.hotels import HotelsRepository
        
        hotel = await HotelsRepository(self.session).get_one_or_none(id=hotel_id)
        if hotel is None:
            raise HTTPException(
                status_code=404, 
                detail="К сожалению такого отеля не существует. Возможно вы ошиблись при вводе id"
            )
               
        add_obj_stmt = insert(self.model).values(**data.model_dump(), hotel_id=hotel_id).returning(self.model)
        result = await self.session.execute(add_obj_stmt)
        obj = result.scalars().one()
        return self.schema.model_validate(obj)
    