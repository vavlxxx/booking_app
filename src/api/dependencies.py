from typing import Annotated
from pydantic import BaseModel
from fastapi import Depends, Query


class PaginationParams(BaseModel):

    page: Annotated[int | None, Query(default=1, ge=1, description="Номер страницы")]
    per_page: Annotated[int | None, Query(default=15, ge=1, le=15, description="Количество отелей на странице")]

PaginationDep = Annotated[PaginationParams, Depends()]


class HotelParams(BaseModel):

    title: Annotated[str | None, Query(default=None, description="Название", example="Hotel Deluxe")]
    location: Annotated[str | None, Query(default=None, description="Адрес", example="г. Москва, ул. Пушкинская, д. 5")]

HotelDep = Annotated[HotelParams, Depends()]
