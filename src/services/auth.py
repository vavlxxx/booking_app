import jwt

from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

from src.config import get_settings


class AuthService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

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
            return jwt.decode(access_token, get_settings().JWT_SECRET_KEY, algorithms=[get_settings().JWT_ALGORITHM])
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Неверный токен")
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Срок действия токена истёк. Пожалуйста войдите заново")
        