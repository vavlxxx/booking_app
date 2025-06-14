from src.repos.base import BaseRepository
from src.schemas.auth import User
from src.models.users import UsersOrm


class AuthRepository(BaseRepository):
    model = UsersOrm
    schema = User
