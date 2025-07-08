from pydantic import Field

from src.schemas.base import BasePydanticModel

class _HotelWithDescription(BasePydanticModel):
    description: str | None = Field(default=None, description="Описание")

class HotelNullable(_HotelWithDescription):
    title: str | None = Field(default=None, description="Заголовок")
    location: str | None = Field(default=None, description="Адрес")

class HotelAdd(_HotelWithDescription):
    title: str = Field(description="Заголовок")
    location: str = Field(description="Адрес")

class Hotel(HotelAdd):
    id: int
