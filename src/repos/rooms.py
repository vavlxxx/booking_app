from fastapi import HTTPException
from sqlalchemy import func, insert, select

from src.models.bookings import BookingsOrm
from src.repos.base import BaseRepository
from src.schemas.rooms import FullRoomData, Room, RoomDataWithEmptyRooms
from src.models.rooms import RoomsOrm
from src.db import engine

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
    

    async def get_all_filtered_by_time(self, hotel_id, date_from, date_to):
        
        rooms_count = (
            select(BookingsOrm.room_id, func.count(BookingsOrm.room_id).label("booked_rooms"))
            .select_from(BookingsOrm)
            .filter(
                BookingsOrm.date_from <= date_to, 
                BookingsOrm.date_to >= date_from
            )
            .group_by(BookingsOrm.room_id)
            .cte(name="rooms_count")
        )

        rooms_left = (
            select(
                RoomsOrm.id.label("room_id"), 
                (RoomsOrm.quantity - func.coalesce(rooms_count.c.booked_rooms, 0)).label("empty_rooms")
            )
            .select_from(RoomsOrm)
            .outerjoin(rooms_count, RoomsOrm.id == rooms_count.c.room_id)
            .cte(name="rooms_left")
        )

        rooms_ids_by_hotel = (
            select(RoomsOrm.id)
            .select_from(RoomsOrm)
            .filter_by(hotel_id=hotel_id)
            .subquery(name="rooms_ids_by_hotel")
        )

        empty_rooms_data_to_get = (
            select(
                RoomsOrm.id,
                RoomsOrm.hotel_id,
                RoomsOrm.title,
                RoomsOrm.description,
                RoomsOrm.price,
                RoomsOrm.quantity,
                RoomsOrm.discount,
                RoomsOrm.discounted_price,
                rooms_left.c.empty_rooms
            )
            .select_from(rooms_left)
            .join(RoomsOrm, RoomsOrm.id == rooms_left.c.room_id)
            .filter(
                rooms_left.c.empty_rooms > 0,
                rooms_left.c.room_id.in_(rooms_ids_by_hotel)
            )
        )
        # print(empty_rooms_data_to_get.compile(compile_kwargs={"literal_binds": True}, bind=engine))
        result = await self.session.execute(empty_rooms_data_to_get)
        return [RoomDataWithEmptyRooms.model_validate(obj) for obj in result.all()]
    