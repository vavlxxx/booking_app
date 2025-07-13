from pydantic import Field

from src.schemas.additionals import AdditionalsData
from src.schemas.base import BasePydanticModel 


class RoomDefault(BasePydanticModel):
    title: str
    description: str | None = Field(default="Отсутствует")
    quantity: int
    price: float
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
    title: str | None = Field(default="Отсутствует")
    description: str | None = Field(default="Отсутствует")
    quantity: int | None = Field(default=0)
    price: float | None = Field(default=0.0)
    discount: int | None = Field(default=0)

class FullRoomOptional(RoomOptional):
    additionals_ids: list[int] = Field(default_factory=list)
    