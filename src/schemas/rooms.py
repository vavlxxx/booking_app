from typing import Optional
from pydantic import Field

from src.schemas.base import BasePydanticModel 


class RoomDefault(BasePydanticModel):
    title: str
    description: Optional[str] = Field(default="Отсутствует")
    quantity: int
    price: float
    discount: Optional[int] = Field(default=0, le=100, ge=0)

class RoomAdd(RoomDefault):
    hotel_id: int

class RoomRequest(RoomDefault):
    additionals_ids: Optional[list[int]] = Field(default_factory=list)


class FullRoomData(RoomAdd):
    id: int
    discounted_price: float

class RoomDataWithEmptyRooms(FullRoomData):
    empty: int


class RoomOptional(BasePydanticModel):
    title: Optional[str] = Field(default="Отсутствует")
    description: Optional[str] = Field(default="Отсутствует")
    quantity: Optional[int] = Field(default=0)
    price: Optional[float] = Field(default=0.0)
    discount: Optional[int] = Field(default=0)

class FullRoomOptional(RoomOptional):
    additionals_ids: Optional[list[int]] = Field(default_factory=list)
    