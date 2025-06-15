from fastapi import HTTPException
from sqlalchemy import select

from src.repos.base import BaseRepository
from src.schemas.auth import User, UserRegister, UserFullInfo
from src.models.users import UsersOrm


class AuthRepository(BaseRepository):
    model = UsersOrm
    schema = User

    async def add(self, data: UserRegister):
        result = await self.get_one_or_none(email=data.email)
        if result is not None:
            raise HTTPException(status_code=400, detail="User with that email address already exists. Try another")
        
        return await super().add(data)
    
    
    async def get_user_with_passwd(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        obj = result.scalars().one_or_none()

        if obj is None:
            return None
            
        return UserFullInfo.model_validate(obj)
    