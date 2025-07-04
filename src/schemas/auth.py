from pydantic import Field, EmailStr, PastDate

from src.schemas.base import BasePydanticModel


class _UserData(BasePydanticModel):
    first_name: str = Field(description="Имя")
    last_name: str = Field(description="Фамилия")
    gender: str = Field(description="Пол", pattern="^[МЖ]$")
    birthday: PastDate = Field(description="Дата рождения")


class UserLoginRequest(BasePydanticModel):
    email: EmailStr = Field(description="Электронная почта")
    password: str = Field(description=" Пароль")


class UserRegisterRequest(UserLoginRequest, _UserData):
    ...


class UserRegister(_UserData):
    hashed_password: str
    email: EmailStr

   
class User(_UserData):
    id: int
    email: EmailStr

class UserFullInfo(User):
    hashed_password: str
    