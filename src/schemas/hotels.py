from pydantic import Field

from src.schemas.base import BasePydanticModel


class HotelNullable(BasePydanticModel):
    title: str | None = Field(default=None, description="Заголовок", example="Hotel Deluxe")
    location: str | None = Field(default=None, description="Адрес", example="г. Москва, ул. Пушкинская, д. 5")
    description: str | None = Field(default=None, description="Описание", example="Отель в центре Москвы")


class HotelAdd(HotelNullable):
    title: str = Field(description="Заголовок", example="Hotel Deluxe")
    location: str = Field(description="Адрес", example="г. Москва, ул. Пушкинская, д. 5")


class Hotel(HotelAdd):
    id: int