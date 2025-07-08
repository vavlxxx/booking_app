from sqlalchemy import select

from src.repos.base import BaseRepository
from src.repos.mappers.mappers import AuthMapper, AuthFullInfoMapper

from src.models.users import UsersOrm
from src.schemas.auth import UserFullInfo

class AuthRepository(BaseRepository):
    model = UsersOrm
    mapper = AuthMapper


    async def get_user_with_passwd(self, **filter_by) -> UserFullInfo:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        obj = result.scalars().one_or_none()
        return AuthFullInfoMapper.map_to_domain_entity(obj) # type: ignore
    