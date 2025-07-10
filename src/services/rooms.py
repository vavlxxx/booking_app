from src.schemas.additionals import RoomsAdditionalsRequest
from src.services.base import BaseService
from src.schemas.rooms import FullRoomOptional, RoomAdd, FullRoomData, RoomRequest, RoomsWithRels
from src.dependencies.rooms import DateDep
from src.utils.exceptions import HotelNotFoundException, ObjectNotFoundException, RoomNotFoundException


class RoomsService(BaseService):
    
    @BaseService._db_required
    async def get_rooms(
        self,
        hotel_id: int,
        dates: DateDep
    ):  
        try:
            await self.db.hotels.get_one(id=hotel_id) 
        except ObjectNotFoundException:
            raise HotelNotFoundException

        rooms = await self.db.rooms.get_all_filtered_by_time( 
            hotel_id=hotel_id,
            date_from=dates.date_from,
            date_to=dates.date_to
        )
        return rooms


    @BaseService._db_required
    async def get_room(
        self,
        room_id: int,
        hotel_id: int
    ):
        try:
            await self.db.hotels.get_one(id=hotel_id) 
        except ObjectNotFoundException:
            raise HotelNotFoundException

        try:
            room: RoomsWithRels | None = await self.db.rooms.get_one_with_rel( 
                hotel_id=hotel_id, 
                id=room_id
            )
        except ObjectNotFoundException:
            raise RoomNotFoundException

        return room
    

    @BaseService._db_required
    async def add_room(
        self,
        room_data: RoomRequest,
        hotel_id: int
    ):
        try:
            await self.db.hotels.get_one(id=hotel_id) 
        except ObjectNotFoundException:
            raise HotelNotFoundException
        
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

        room = await self.db.rooms.get_one_with_rel( 
            hotel_id=hotel_id, 
            id=room.id
        )
        return room


    @BaseService._db_required
    async def delete_room(
        self,
        room_id: int,
        hotel_id: int
    ):
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
        try:
            await self.db.rooms.get_one(id=room_id, hotel_id=hotel_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException

        await self.db.rooms_additionals.delete(room_id=room_id)
        await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await self.db.commit()


    @BaseService._db_required
    async def edit_room(
        self,
        room_data: RoomRequest | FullRoomOptional,
        room_id: int,
        hotel_id: int,
    ):
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
        try:
            await self.db.rooms.get_one(id=room_id, hotel_id=hotel_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException

        await self.db.rooms.edit(
            room_data, 
            id=room_id, 
            hotel_id=hotel_id,
            exclude_fields={"additionals_ids"}
        )
        
        await self.db.rooms_additionals.update_all(
            room_id=room_id, 
            additionals_ids=room_data.additionals_ids
        )
        await self.db.commit()

        room = await self.db.rooms.get_one_with_rel( 
            hotel_id=hotel_id, 
            id=room_id
        )
        return room

    async def edit_partialy(
        self,
        room_data: FullRoomOptional,
        room_id: int,
        hotel_id: int
    ):
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
        try:
            await self.db.rooms.get_one(id=room_id, hotel_id=hotel_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException

        await self.db.rooms.edit(
            room_data, 
            id=room_id, 
            hotel_id=hotel_id,
            exclude_fields={"additionals_ids"}
        )
        _room_data = room_data.model_dump(exclude_unset=True)
        if "additionals_ids" in _room_data:
            await self.db.rooms_additionals.update_all(
                room_id=room_id, 
                additionals_ids=room_data.additionals_ids
            )
        await self.db.commit()
        room = await self.db.rooms.get_one_with_rel(
            hotel_id=hotel_id, 
            id=room_id
        )
        return room
    