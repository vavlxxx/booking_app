from sqlalchemy import delete, insert, select

from src.models.additionals import AdditionalsOrm, RoomsAdditionalsOrm
from src.schemas.additionals import RoomsAdditionalsData

from src.repos.base import BaseRepository
from src.repos.mappers.mappers import AdditionalsMapper


class AdditionalsRepository(BaseRepository):
    model = AdditionalsOrm
    mapper = AdditionalsMapper


class RoomsAdditionalsRepository(BaseRepository):
    model = RoomsAdditionalsOrm
    mapper = RoomsAdditionalsData
    
    
    async def update_all(self, room_id: int, additionals_ids: list[int]):

        ids_to_delete = (
            select(self.model.id)
            .select_from(self.model)
            .filter(
                self.model.room_id == room_id,
                self.model.additional_id.notin_(additionals_ids),
            )
        )

        delete_stmt = (
            delete(self.model)
            .filter(
                self.model.room_id == room_id,
                self.model.id.in_(ids_to_delete),
            )
        )

        await self.session.execute(delete_stmt)

        add_new_rooms_addits = (
            insert(self.model)
            .from_select(
                ["room_id", "additional_id"],
                select(room_id, AdditionalsOrm.id).
                filter(
                    AdditionalsOrm.id.in_(additionals_ids),
                    AdditionalsOrm.id.notin_(
                        select(self.model.additional_id)
                        .select_from(self.model)
                        .filter(self.model.room_id == room_id)
                    )
                )
            )
        )

        await self.session.execute(add_new_rooms_addits)
