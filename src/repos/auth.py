from fastapi import HTTPException
from sqlalchemy import select
from src.repos.base import BaseRepository
from src.schemas.auth import User, UserAdd
from src.models.users import UsersOrm


class AuthRepository(BaseRepository):
    model = UsersOrm
    schema = User

    async def add(self, data: UserAdd):
        result = await self.get_one_or_none(email=data.email)
        if result is not None:
            raise HTTPException(status_code=400, detail="User with that email address already exists. Try another")
        
        return await super().add(data)