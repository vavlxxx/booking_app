from sqlalchemy import delete, select, insert, update
from fastapi.exceptions import HTTPException

from src.schemas.base import BasePydanticModel


class BaseRepository:

    model = None
    schema: BasePydanticModel = None
    not_found_message = "Объект не найден. Попробуйте ещё раз"


    def __init__(self, session):
        self.session = session


    async def get_all(self, **filter_by) -> list[BasePydanticModel]:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        objs = [self.schema.model_validate(obj) for obj in result.scalars().all()]
        return objs


    async def get_one_or_none(self, **filter_by) -> BasePydanticModel | None:
        query = select(self.model).filter_by(**filter_by)
        # print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        obj = result.scalars().one_or_none()

        if obj is None:
            raise HTTPException(status_code=404, detail=self.not_found_message)

        return self.schema.model_validate(obj) 


    async def add(self, data: BasePydanticModel):
        add_obj_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_obj_stmt)
        obj = result.scalars().one()
        return self.schema.model_validate(obj)


    async def edit(self, data: BasePydanticModel, exclude_unset=True, **filter_by):
        await self.get_one_or_none(**filter_by)        
        edit_obj_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(edit_obj_stmt)
    

    async def delete(self, **filter_by):
        await self.get_one_or_none(**filter_by)
        delete_obj_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_obj_stmt)
    