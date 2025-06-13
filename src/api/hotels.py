from fastapi import (
    APIRouter,
    Body,
    Path,
    Query,
)

from sqlalchemy import insert

from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPATCH
from src.helpers.examples import HOTEL_EXAMPLES
from src.api.dependencies import PaginationDep
from src.db import async_session_maker
from src.repos.hotels import HotelsRepository

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)

hotels = []


@router.get("/", summary="Получение списка отелей")
async def get_hotels(
    pagination: PaginationDep,
    location: str | None = Query(default=None, description="Адрес"),
    title: str | None = Query(default=None, description="Название"),
):
    limit = pagination.per_page
    offset = (pagination.page - 1) * limit
    
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=limit,
            offset=offset,
        )


@router.post("/", summary="Создание отеля")
async def create_hotel(
    hotel_data: Hotel = Body(
        description="Данные об отеле", 
        openapi_examples=HOTEL_EXAMPLES
    )
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "OK", "data": hotel}


@router.delete("/{hotel_id}", summary="Удаление отеля по ID")
async def delete_hotel(hotel_id: int = Path(description="ID отеля")):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}", summary="Полное обновление данных об отеле по ID")
async def update_hotel_put(
    hotel_id: int,
    hotel_data: Hotel = Body(
        description="Данные об отеле", 
        openapi_examples=HOTEL_EXAMPLES
    )
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частичное обновление данных об отеле по ID")
def update_hotel_patch(
    hotel_id: int,
    hotel_data: HotelPATCH,
):
    if hotel_data.title is None and hotel_data.name is None:
        return {"status": "ERROR"}

    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = (
                hotel_data.title if hotel_data.title is not None else hotel["title"]
            )
            hotel["name"] = (
                hotel_data.name if hotel_data.name is not None else hotel["name"]
            )
            return {"status": "OK"}

    return {"status": "NOT FOUND"}
