from typing import Annotated

from fastapi import Depends, Query

from src.schemas.base import BasePydanticModel


class HotelParams(BasePydanticModel):
    title: str | None
    location: str | None


def get_hotel_params(
    title: Annotated[str | None, Query(description="Название")] = None,
    location: Annotated[str | None, Query(description="Адрес")] = None,
) -> HotelParams:
    return HotelParams(title=title, location=location)


HoteParamsDep = Annotated[HotelParams, Depends(get_hotel_params)]


class PaginationParams(BasePydanticModel):
    page: Annotated[int, Query(1, ge=1)]
    per_page: Annotated[int, Query(None, ge=1, le=15)]

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.per_page


def get_pagination_params(
    page: Annotated[int, Query(ge=1, description="Номер страницы")] = 1,
    per_page: Annotated[int, Query(ge=1, le=15, description="Количество отелей на странице")] = 15,
) -> PaginationParams:
    return PaginationParams(page=page, per_page=per_page)


PaginationDep = Annotated[PaginationParams, Depends(get_pagination_params)]
