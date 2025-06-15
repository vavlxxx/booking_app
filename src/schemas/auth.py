from pydantic import Field, EmailStr, PastDate

from src.schemas.base import BasePydanticModel


class _UserData(BasePydanticModel):
    first_name: str = Field(description="Имя", example="John")
    last_name: str = Field(description="Фамилия", example="Doe")
    gender: str = Field(description="Пол", example="M", pattern="^[МЖ]$")
    birthday: PastDate = Field(description="Дата рождения", example="1970-01-01")


class UserLoginRequest(BasePydanticModel):
    email: EmailStr = Field(description="Электронная почта", example="mymail@example.com")
    password: str = Field(description=" Пароль", example="qwerty123")


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
    