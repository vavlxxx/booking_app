from datetime import date
from typing import Annotated

from fastapi import Depends, Path, Query

from src.schemas.base import BasePydanticModel


class DatesParams(BasePydanticModel):
    date_from: date
    date_to: date

def get_dates_params(
    date_from: Annotated[date, Query(description="Дата въезда", example=date(2025, 8, 1))],
    date_to: Annotated[date, Query(description="Дата выезда", example=date(2025, 8, 10))]
):
    return DatesParams(date_from=date_from, date_to=date_to)

DateDep = Annotated[DatesParams, Depends(get_dates_params)]


class RoomWithIds(BasePydanticModel):
    room_id: int
    hotel_id: int

def get_rooms_with_ids(
    room_id: int = Path(description="ID номера", example=1), 
    hotel_id: int = Path(description="ID отеля", example=1)
):
    return RoomWithIds(room_id=room_id, hotel_id=hotel_id)

RoomWithIdsDep = Annotated[RoomWithIds, Depends(get_rooms_with_ids)]
