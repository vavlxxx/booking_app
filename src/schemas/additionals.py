from typing import Optional
from src.schemas.base import BasePydanticModel


class AdditionalsRequest(BasePydanticModel):
    name: str
    description: Optional[str]


class AdditionalsData(AdditionalsRequest):
    id: int


class RoomsAdditionalsRequest(BasePydanticModel):
    additional_id: int
    room_id: int


class RoomsAdditionalsData(RoomsAdditionalsRequest):
    id: int
    