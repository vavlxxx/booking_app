from pydantic import Field, EmailStr, PastDate

from src.schemas.base import BasePydanticModel


class _UserData(BasePydanticModel):
    first_name: str | None = Field(description="Имя", default=None)
    last_name: str | None = Field(description="Фамилия", default=None)
    gender: str | None = Field(description="Пол", pattern="^[МЖ]$", default=None)
    birthday: PastDate | None = Field(description="Дата рождения", default=None)


class UserLoginRequest(BasePydanticModel):
    email: EmailStr = Field(description="Электронная почта")
    password: str = Field(description=" Пароль", min_length=8, max_length=256)


class UserRegisterRequest(UserLoginRequest):
    ...


class UserRegister(BasePydanticModel):
    hashed_password: str
    email: EmailStr

   
class User(_UserData):
    id: int
    email: EmailStr

class UserFullInfo(User):
    hashed_password: str
    