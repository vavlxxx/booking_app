from src.repos.base import BaseRepository
from src.schemas.rooms import FullRoomData, RoomDataWithEmptyRooms
from src.models.rooms import RoomsOrm
from src.repos.utils import rooms_data_to_booking


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = FullRoomData


    async def get_all_filtered_by_time(self, hotel_id, date_from, date_to):
        empty_rooms_data_to_get = rooms_data_to_booking(date_from, date_to, hotel_id)
        result = await self.session.execute(empty_rooms_data_to_get)
        return [RoomDataWithEmptyRooms.model_validate(obj) for obj in result.all()]
    