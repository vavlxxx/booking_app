from src.schemas.additionals import RoomsAdditionalsRequest
from src.services.base import BaseService, ExceptionsHandler
from src.schemas.rooms import FullRoomOptional, RoomAdd, FullRoomData, RoomRequest
from src.dependencies.rooms import DateDep
from src.utils.exceptions import AdditionalNotFoundException


class RoomsService(BaseService, ExceptionsHandler):
    
    async def get_rooms(
        self,
        hotel_id: int,
        dates: DateDep
    ):  
        await self.check_dates_validity(date_from=dates.date_from, date_to=dates.date_to)
        await self.get_hotel_and_check_existence(db=self.db, hotel_id=hotel_id)
        rooms = await self.db.rooms.get_all_filtered_by_time( 
            hotel_id=hotel_id,
            date_from=dates.date_from,
            date_to=dates.date_to
        )
        return rooms


    async def get_room(
        self,
        room_id: int,
        hotel_id: int
    ):
        room: FullRoomData = await self.get_room_and_check_existence(
            db=self.db, 
            hotel_id=hotel_id, 
            room_id=room_id,
            room_with_rel=True
        )
        return room
    

    async def add_room(
        self,
        room_data: RoomRequest,
        hotel_id: int
    ):
        await self.get_hotel_and_check_existence(db=self.db, hotel_id=hotel_id)
        
        additionals_ids = await self.db.additionals.get_all_filtered_by_ids(ids_list=room_data.additionals_ids) # type: ignore
        if len(additionals_ids) != len(room_data.additionals_ids):
            raise AdditionalNotFoundException

        _room_data = RoomAdd(**room_data.model_dump(exclude={"additionals_ids"}), hotel_id=hotel_id)
        room: FullRoomData = await self.db.rooms.add(_room_data) # type: ignore

        additionals = [
            RoomsAdditionalsRequest(
                additional_id=addit_id, 
                room_id=room.id
            ) for addit_id in room_data.additionals_ids]

        if additionals:
            await self.db.rooms_additionals.add_bulk(additionals)

        await self.db.commit()

        added_room_with_rels = await self.get_room_and_check_existence(
            db=self.db, 
            hotel_id=hotel_id, 
            room_id=room.id,
            room_with_rel=True
        )
        return added_room_with_rels


    async def delete_room(
        self,
        room_id: int,
        hotel_id: int
    ):
        await self.get_room_and_check_existence(
            db=self.db, 
            hotel_id=hotel_id, 
            room_id=room_id, 
            room_with_rel=False
        )

        await self.db.rooms_additionals.delete(room_id=room_id)
        await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await self.db.commit()


    async def edit_room(
        self,
        room_data: RoomRequest | FullRoomOptional,
        room_id: int,
        hotel_id: int,
    ):
        await self.get_room_and_check_existence(
            db=self.db, 
            hotel_id=hotel_id, 
            room_id=room_id, 
            room_with_rel=False
        )

        await self.db.rooms.edit(
            room_data, 
            id=room_id, 
            hotel_id=hotel_id,
            exclude_fields={"additionals_ids"}
        )
        
        _room_data = room_data.model_dump(exclude_unset=True)
        if "additionals_ids" in _room_data:
            additionals_ids = await self.db.additionals.get_all_filtered_by_ids(ids_list=room_data.additionals_ids) # type: ignore
            if len(additionals_ids) != len(room_data.additionals_ids):
                raise AdditionalNotFoundException
            
            await self.db.rooms_additionals.update_all(
                room_id=room_id, 
                additionals_ids=room_data.additionals_ids
            )
        await self.db.commit()
