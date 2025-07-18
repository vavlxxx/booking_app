from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from src.repos.base import BaseRepository
from src.repos.mappers.mappers import AuthMapper, AuthFullInfoMapper
from src.utils.exceptions import ObjectNotFoundException
from src.models.users import UsersOrm
from src.schemas.auth import UserFullInfo


class AuthRepository(BaseRepository):
    model = UsersOrm
    mapper = AuthMapper

    async def get_user_with_passwd(self, **filter_by) -> UserFullInfo:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            obj = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException
        return AuthFullInfoMapper.map_to_domain_entity(obj)  # type: ignore
