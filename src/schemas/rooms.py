from pydantic import Field, model_validator

from src.schemas.additionals import AdditionalsData
from src.schemas.base import BasePydanticModel 


class RoomDefault(BasePydanticModel):
    title: str
    description: str | None = Field(default=None)
    quantity: int = Field(ge=0)
    price: float = Field(ge=0)
    discount: int | None = Field(default=0, le=100, ge=0)


class RoomAdd(RoomDefault):
    hotel_id: int

class RoomRequest(RoomDefault):
    additionals_ids: list[int] = Field(default_factory=list)

class FullRoomData(RoomAdd):
    id: int
    discounted_price: float

class RoomsWithRels(FullRoomData):
    additionals: list[AdditionalsData]

class RoomOptional(BasePydanticModel):
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    quantity: int | None = Field(default=None, ge=0)
    price: float | None = Field(default=None, ge=0)
    discount: int | None = Field(default=None, ge=0, le=100)

    @model_validator(mode="after")
    def validate_all_fields_are_provide(self):
        values = tuple(self.model_dump().values())
        if all(map(lambda val: val is None, values)):
            raise ValueError("provide at least one non-empty field")
        return self 

class FullRoomOptional(RoomOptional):
    additionals_ids: list[int] | None = Field(default=None)
    