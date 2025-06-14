from datetime import date, datetime

from pydantic import Field, field_validator, EmailStr, PastDate
from pydantic_core import PydanticCustomError

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from src.schemas.base import BasePydanticModel


class UserAdd(BasePydanticModel):
    email: str
    first_name: str
    last_name: str
    birthday: date
    gender: str
    hashed_password: str


class UserAuthentication(BasePydanticModel):

    password: str = Field(description=" Пароль", example="qwerty123")
    first_name: str = Field(description="Имя", example="John")
    last_name: str = Field(description="Фамилия", example="Doe")
    gender: str = Field(description="Пол", example="M", pattern="^[МЖ]$")
    email: EmailStr = Field(description="Электронная почта", example="mymail@example.com")
    birthday: PastDate = Field(description="Дата рождения", example="1970-01-01")

    def hash_password(self):
        data = self.model_dump(exclude={"password"})
        data["hashed_password"] = pwd_context.hash(self.password)
        return UserAdd.model_validate(data)


class User(BasePydanticModel):
    id: int
    email: str
    gender: str
    birthday: date | str
    last_name: str
    first_name: str
