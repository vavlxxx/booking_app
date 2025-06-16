from typing import Annotated
from fastapi import Depends, HTTPException, Path, Query, Request

from services.auth import AuthService
from src.schemas.base import BasePydanticModel
from src.utils.db_manager import DBManager
from src.db import async_session_maker


class PaginationParams(BasePydanticModel):

    page: Annotated[int | None, Query(default=1, ge=1, description="Номер страницы")]
    per_page: Annotated[int | None, Query(default=15, ge=1, le=15, description="Количество отелей на странице")]

PaginationDep = Annotated[PaginationParams, Depends()]


class HotelParams(BasePydanticModel):

    title: Annotated[str | None, Query(default=None, description="Название", example="Hotel Deluxe")]
    location: Annotated[str | None, Query(default=None, description="Адрес", example="г. Москва, ул. Пушкинская, д. 5")]

HotelDep = Annotated[HotelParams, Depends()]


class RoomWithIds(BasePydanticModel):
    id: Annotated[int, Path(description="ID номера", example=1)]
    hotel_id: Annotated[int, Path(description="ID отеля", example=1)]

RoomWithIdsDep = Annotated[RoomWithIds, Depends()]


def get_token(request: Request) -> str | None:
    access_token = request.cookies.get("access_token", None)
    if access_token is None:
        raise HTTPException(status_code=401, detail="Не аутентифицирован. Пожалуйста предоставьте токен доступа")
    return access_token


def get_current_user(access_token: str = Depends(get_token)):
    data = AuthService.decode_access_token(access_token)
    return data.get("user_id")
    
UserIdDep = Annotated[int, Depends(get_current_user)]


def get_db_manager():
    return DBManager(session_factory=async_session_maker)


async def get_db():
    async with get_db_manager() as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
