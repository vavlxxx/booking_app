from sqlalchemy import delete, select, insert, update

from src.schemas.base import BasePydanticModel


class BaseRepository:

    model = None
    schema: BasePydanticModel = None


    def __init__(self, session):
        self.session = session


    async def get_all_filtered(self, *filter, **filter_by):
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        return [self.schema.model_validate(obj) for obj in result.scalars().all()]


    async def get_all(self) -> list[BasePydanticModel]:
        return await self.get_all_filtered()


    async def get_one_or_none(self, **filter_by) -> BasePydanticModel | None:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        obj = result.scalars().one_or_none()
        if obj is None:
            return None
        return self.schema.model_validate(obj) 


    async def add_bulk(self, data: list[BasePydanticModel]):
        add_obj_stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_obj_stmt)


    async def add(self, data: BasePydanticModel, **params):
        add_obj_stmt = insert(self.model).values(**data.model_dump(), **params).returning(self.model)
        result = await self.session.execute(add_obj_stmt)
        obj = result.scalars().one()
        return self.schema.model_validate(obj)


    async def edit(self, data: BasePydanticModel, exclude_unset=True, exclude_fields=None, **filter_by):
        exclude_fields = exclude_fields or set()
        
        to_update = data.model_dump(
            exclude=exclude_fields, 
            exclude_unset=exclude_unset
        )

        if not to_update:
            return

        edit_obj_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**to_update)
        )
        await self.session.execute(edit_obj_stmt)


    async def delete(self, *filter, **filter_by):
        delete_obj_stmt = (
            delete(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
        )
        await self.session.execute(delete_obj_stmt)
    