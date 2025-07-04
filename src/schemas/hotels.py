from pydantic import ConfigDict, Field

from src.schemas.base import BasePydanticModel
from src.helpers.hotels import HOTEL_EXAMPLES


class HotelNullable(BasePydanticModel):
    title: str | None = Field(default=None, description="Заголовок")
    location: str | None = Field(default=None, description="Адрес")
    description: str | None = Field(default=None, description="Описание")

    model_config = ConfigDict(json_schema_extra=HOTEL_EXAMPLES)

class HotelAdd(HotelNullable):
    title: str = Field(description="Заголовок")
    location: str = Field(description="Адрес")

    model_config = ConfigDict(json_schema_extra=HOTEL_EXAMPLES)

class Hotel(HotelAdd):
    id: int