import jwt

from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

from src.services.base import BaseService
from src.config import get_settings
from src.schemas.auth import (
    UserFullInfo,
    UserLoginRequest,
    UserRegister,
    UserRegisterRequest,
    UserUpdateRequest,
)
from src.utils.exceptions import (
    IncorrentLoginDataException,
    ObjectAlreadyExistsException,
    ObjectNotFoundException,
    UserAlreadyExistsException,
    UserNotFoundException,
)


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def _hash_password(self, password) -> str:
        return self.pwd_context.hash(password)

    def _verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    async def add_user(self, user_data: UserRegisterRequest):
        hashed_password = self._hash_password(user_data.password)
        data = user_data.model_dump(exclude={"password"})
        new_user_data = UserRegister(**data, hashed_password=hashed_password)

        try:
            user = await self.db.auth.add(new_user_data)
        except ObjectAlreadyExistsException as exc:
            raise UserAlreadyExistsException from exc

        await self.db.commit()
        return user

    async def edit_user(self, user_data: UserUpdateRequest, user_id: int):
        try:
            await self.db.auth.get_one(id=user_id)
        except ObjectNotFoundException as exc:
            raise UserNotFoundException from exc
        await self.db.auth.edit(user_data, id=user_id)
        await self.db.commit()

    async def login_user(self, user_data: UserLoginRequest, response):
        try:
            user: UserFullInfo = await self.db.auth.get_user_with_passwd(email=user_data.email)
        except ObjectNotFoundException as exc:
            raise IncorrentLoginDataException from exc

        if not self._verify_password(user_data.password, user.hashed_password):
            raise IncorrentLoginDataException

        access_token = self.create_access_token({"user_id": user.id})
        response.set_cookie(key="access_token", value=access_token)
        return access_token

    async def get_user(self, user_id: int):
        try:
            user = await self.db.auth.get_one(id=user_id)
        except ObjectNotFoundException as exc:
            raise UserNotFoundException from exc
        return user

    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=get_settings().JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, get_settings().JWT_SECRET_KEY, algorithm=get_settings().JWT_ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def decode_access_token(access_token) -> dict[str, str]:
        try:
            return jwt.decode(
                access_token,
                get_settings().JWT_SECRET_KEY,
                algorithms=[get_settings().JWT_ALGORITHM],
            )
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Неверный токен")
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(
                status_code=401, detail="Срок действия токена истёк. Пожалуйста войдите заново"
            )
