from sqlalchemy import delete, insert, select

from src.models.additionals import AdditionalsOrm, RoomsAdditionalsOrm

from src.repos.base import BaseRepository
from src.repos.mappers.mappers import AdditionalsMapper, RoomsAdditionalsMapper


class AdditionalsRepository(BaseRepository):
    model = AdditionalsOrm
    mapper = AdditionalsMapper

    async def get_all_filtered_by_ids(self, ids_list: list):
        query = (
            select(self.model.id) # type: ignore
            .select_from(self.model)
            .filter(
                self.model.id.in_(ids_list), # type: ignore
            )
        )
        result = await self.session.execute(query)
        return result.scalars().all()
    

class RoomsAdditionalsRepository(BaseRepository):
    model: RoomsAdditionalsOrm = RoomsAdditionalsOrm # type: ignore
    mapper = RoomsAdditionalsMapper

    async def update_all(self, room_id: int, additionals_ids: list[int]):

        ids_to_delete = (
            select(self.model.id) # type: ignore
            .select_from(self.model)
            .filter(
                self.model.room_id == room_id,
                self.model.additional_id.notin_(additionals_ids), # type: ignore
            )
        )

        delete_stmt = (
            delete(self.model) # type: ignore
            .filter(
                self.model.room_id == room_id, # type: ignore
                self.model.id.in_(ids_to_delete), # type: ignore
            )
        )

        await self.session.execute(delete_stmt)

        add_new_rooms_addits = (
            insert(self.model) # type: ignore
            .from_select(
                ["room_id", "additional_id"],
                select(room_id, AdditionalsOrm.id) # type: ignore
                .filter(
                    AdditionalsOrm.id.in_(additionals_ids),
                    AdditionalsOrm.id.notin_(
                        select(self.model.additional_id) # type: ignore
                        .select_from(self.model)
                        .filter(self.model.room_id == room_id)
                    )
                )
            )
        )

        await self.session.execute(add_new_rooms_addits)
