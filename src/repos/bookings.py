from datetime import date

from fastapi import HTTPException
from sqlalchemy import select

from src.repos.base import BaseRepository
from src.repos.mappers.mappers import BookingsMapper
from src.repos.utils import rooms_data_to_booking
from src.schemas.bookings import BookingAdd
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
    

    async def add_booking(
        self, 
        booking_data: BookingAdd,
        hotel_id: int
    ):
        rooms_data = rooms_data_to_booking(
            booking_data.date_from, 
            booking_data.date_to,
            hotel_id
        )
        result = await self.session.execute(rooms_data)
        results = result.scalars().all()
        if booking_data.room_id not in results:
            raise HTTPException(status_code=400, detail="Комната полностью занята. Пожалуйста, выберите другую")
        
        return await super().add(booking_data)
