from pydantic import Field, model_validator

from src.schemas.base import BasePydanticModel


class _HotelWithDescription(BasePydanticModel):
    description: str | None = Field(default=None, description="Описание")


class HotelNullable(_HotelWithDescription):
    title: str | None = Field(default=None, description="Заголовок")
    location: str | None = Field(default=None, description="Адрес")

    @model_validator(mode="after")
    def validate_all_fields_are_provide(self):
        values = tuple(self.model_dump().values())
        if all(map(lambda val: val is None, values)):
            raise ValueError("provide at least one non-empty field")
        return self


class HotelAdd(_HotelWithDescription):
    title: str = Field(description="Заголовок")
    location: str = Field(description="Адрес")


class Hotel(HotelAdd):
    id: int
