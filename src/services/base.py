from datetime import date
from typing import Any

from src.schemas.rooms import FullRoomData, RoomsWithRels
from src.utils.db_manager import DBManager
from src.utils.exceptions import (
    DatesMissMatchException, 
    HotelNotFoundException, 
    ObjectNotFoundException, 
    RoomNotFoundException
)


class BaseService:
    db: DBManager| None 

    def __init__(self, db: DBManager | None = None) -> None:
        self.db = db
    

class ExceptionsHandler:

    @staticmethod
    async def check_dates_validity(date_from: date, date_to: date):
        # date_from_ = datetime.strptime(date_from, "%Y-%m-%d").date()
        # date_to_ = datetime.strptime(date_to, "%Y-%m-%d").date()
        if date_from >= date_to or date_from <= date.today():
            raise DatesMissMatchException

    @staticmethod
    async def get_hotel_and_check_existence(db: DBManager, hotel_id: int):
        try:
            hotel = await db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException as exc:
            raise HotelNotFoundException from exc
        return hotel


    @staticmethod
    async def get_room_and_check_existence(
        db: DBManager, 
        room_id: int, 
        hotel_id: int | None = None, 
        room_with_rel: bool = False
    ) -> FullRoomData | RoomsWithRels | Any:
        if hotel_id is not None:
            await ExceptionsHandler.get_hotel_and_check_existence(db, hotel_id)

        try:
            if room_with_rel:
                room = await db.rooms.get_one_with_rel(id=room_id)
            else:
                room = await db.rooms.get_one(id=room_id)
        except ObjectNotFoundException as exc:
            raise RoomNotFoundException from exc
        
        return room
        