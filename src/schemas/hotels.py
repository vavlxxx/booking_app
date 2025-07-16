from pydantic import Field, field_validator

from src.schemas.base import BasePydanticModel

class _HotelWithDescription(BasePydanticModel):
    description: str | None = Field(default=None, description="Описание")

class HotelNullable(_HotelWithDescription):
    title: str | None = Field(default=None, description="Заголовок")
    location: str | None = Field(default=None, description="Адрес")

class HotelAdd(_HotelWithDescription):
    title: str = Field(description="Заголовок")
    location: str = Field(description="Адрес")
    
    @field_validator("title")
    def title_is_not_empty(cls, value: str):
        if not value.strip():
            raise ValueError("title option is required")
        return value
    
    @field_validator("location")
    def location_is_not_empty(cls, value: str):
        if not value.strip():
            raise ValueError("location option is required")
        return value

class Hotel(HotelAdd):
    id: int
