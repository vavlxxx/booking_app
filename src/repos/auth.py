from sqlalchemy import select

from src.repos.base import BaseRepository
from src.schemas.auth import User, UserFullInfo
from src.models.users import UsersOrm


class AuthRepository(BaseRepository):
    model = UsersOrm
    schema = User


    async def get_user_with_passwd(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        obj = result.scalars().one_or_none()
        return UserFullInfo.model_validate(obj)
    