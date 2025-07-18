from src.services.base import BaseService, ExceptionsHandler
from src.utils.exceptions import NotEmptyHotelException
from src.schemas.hotels import HotelAdd, HotelNullable
from src.dependencies.hotels import HoteParamsDep, PaginationDep
from src.dependencies.rooms import DateDep


class HotelsService(BaseService, ExceptionsHandler):
    async def get_hotels(
        self, pagination: PaginationDep, hotel_filter_data: HoteParamsDep, dates: DateDep
    ):
        await self.check_dates_validity(date_from=dates.date_from, date_to=dates.date_to)
        hotels = await self.db.hotels.get_all_filtered_by_time(
            location=hotel_filter_data.location,
            title=hotel_filter_data.title,
            limit=pagination.per_page,
            offset=pagination.offset,
            date_from=dates.date_from,
            date_to=dates.date_to,
        )
        return hotels

    async def get_hotel(self, hotel_id: int):
        hotel = await self.get_hotel_and_check_existence(db=self.db, hotel_id=hotel_id)
        return hotel

    async def add_hotel(self, hotel_data: HotelAdd):
        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return hotel

    async def edit_hotel(self, hotel_data: HotelAdd | HotelNullable, hotel_id: int):
        await self.get_hotel_and_check_existence(db=self.db, hotel_id=hotel_id)
        await self.db.hotels.edit(hotel_data, id=hotel_id)
        await self.db.commit()

    async def delete_hotel(self, hotel_id: int):
        await self.get_hotel_and_check_existence(db=self.db, hotel_id=hotel_id)
        rooms = await self.db.rooms.get_all_filtered(hotel_id=hotel_id)
        if rooms and len(rooms) > 0:
            raise NotEmptyHotelException

        await self.db.hotels.delete(id=hotel_id)  # type: ignore
        await self.db.commit()
