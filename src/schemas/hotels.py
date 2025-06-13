from pydantic import Field
from src.schemas.base import BasePydanticModel

class HotelAdd(BasePydanticModel):
    title: str = Field(description="Заголовок", example="Hotel Deluxe")
    location: str = Field(description="Адрес", example="г. Москва, ул. Пушкинская, д. 5")


class Hotel(HotelAdd):
    id: int


class HotelNullable(BasePydanticModel):
    title: str | None = Field(default=None, description="Заголовок", example="Hotel Deluxe")
    location: str | None = Field(default=None, description="Адрес", example="г. Москва, ул. Пушкинская, д. 5")
