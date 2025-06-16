from fastapi import HTTPException
from sqlalchemy import select

from src.repos.base import BaseRepository
from src.schemas.auth import User, UserRegister, UserFullInfo
from src.models.users import UsersOrm


class AuthRepository(BaseRepository):
    model = UsersOrm
    schema = User
    not_found_message = "Пользователь не найден"

    async def add(self, data: UserRegister):
        result = await self.get_one_or_none(email=data.email)
        if result is not None:
            raise HTTPException(status_code=400, detail="Пользователь с таким логином уже существует")
        
        return await super().add(data)
    
    
    async def get_user_with_passwd(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        obj = result.scalars().one_or_none()

        if obj is None:
            raise HTTPException(status_code=404, detail=self.not_found_message)
            
        return UserFullInfo.model_validate(obj)
    