from sqlalchemy import delete, select, insert, update
from pydantic import BaseModel
from fastapi.exceptions import HTTPException


class BaseRepository:

    model = None
    

    def __init__(self, session):
        self.session = session


    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()
    

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()


    async def add(self, data: BaseModel):
        add_obj_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_obj_stmt)
        return result.scalars().one()


    async def is_only_one(self, **filter_by) -> bool:

        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        data = result.scalars().all()

        if len(data) > 1:
            raise HTTPException(status_code=400, detail="Got more than one objects. Try another filters")
        if len(data) == 0:
            raise HTTPException(status_code=404, detail="Object not found. Try another filters")



    async def edit(self, data: BaseModel, **filter_by):
        await self.is_only_one(**filter_by)
        edit_obj_stmt = update(self.model).filter_by(**filter_by).values(**data.model_dump())
        await self.session.execute(edit_obj_stmt)
    

    async def delete(self, **filter_by):
        await self.is_only_one(**filter_by)
        delete_obj_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_obj_stmt)
