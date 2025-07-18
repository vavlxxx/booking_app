from schemas.bookings import BookingAdd
from schemas.rooms import FullRoomData
from src.services.base import BaseService, ExceptionsHandler
from src.utils.exceptions import ObjectNotFoundException, RoomNotFoundException


class BookingsService(BaseService, ExceptionsHandler):
    async def add_booking(self, booking_data, user_id):
        await self.check_dates_validity(
            date_from=booking_data.date_from, date_to=booking_data.date_to
        )

        try:
            room: FullRoomData = await self.get_room_and_check_existence(
                db=self.db, room_id=booking_data.room_id
            )
        except ObjectNotFoundException as exc:
            raise RoomNotFoundException from exc

        _booking_data = BookingAdd(
            **booking_data.model_dump(), user_id=user_id, price=room.discounted_price
        )

        booking = await self.db.bookings.add_booking(
            booking_data=_booking_data, hotel_id=room.hotel_id
        )

        await self.db.commit()
        return booking

    async def get_user_bookings(self, user_id: int):
        return await self.db.bookings.get_all_filtered(user_id=user_id)

    async def get_all_bookings(self):
        return await self.db.bookings.get_all()
