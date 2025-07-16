from pydantic import field_validator

from src.schemas.base import BasePydanticModel


class AdditionalsRequest(BasePydanticModel):
    name: str
    description: str | None

    @field_validator("name")
    def validate_name(cls, value):
        if not value:
            raise ValueError("name option is required")
        return value

    @field_validator("description")
    def validate_description(cls, value):
        if value == "":
            raise ValueError("description cannot be empty string")
        return value


class AdditionalsData(AdditionalsRequest):
    id: int


class RoomsAdditionalsRequest(BasePydanticModel):
    additional_id: int
    room_id: int


class RoomsAdditionalsData(RoomsAdditionalsRequest):
    id: int
    