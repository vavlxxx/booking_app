from typing import Optional
from src.schemas.base import BasePydanticModel


class AdditionalRequest(BasePydanticModel):
    name: str
    description: Optional[str]


class Additional(AdditionalRequest):
    id: int


class RoomAdditionalRequest(BasePydanticModel):
    additional_id: int
    room_id: int


class RoomAdditional(RoomAdditionalRequest):
    id: int
    