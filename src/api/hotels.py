from fastapi import (
    APIRouter,
    Body,
    HTTPException,
    Path,
)

from src.schemas.hotels import HotelAdd, HotelNullable
from src.helpers.hotels import HOTEL_EXAMPLES
from src.api.dependencies import PaginationDep, HotelDep
from src.db import async_session_maker
from src.repos.hotels import HotelsRepository

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get("/", summary="Получить список отелей")
async def get_hotels(pagination: PaginationDep, hotel_data: HotelDep):
    limit = pagination.per_page
    offset = (pagination.page - 1) * limit
    
    async with async_session_maker() as session:
        hotels = await HotelsRepository(session).get_all(
            location=hotel_data.location,
            title=hotel_data.title,
            limit=limit,
            offset=offset,
        )    
    return hotels


@router.get("/{hotel_id}", summary="Получить отель")
async def get_hotel(hotel_id: int = Path(description="ID отеля", example=1)):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).get_one_or_none(id=hotel_id)
    return hotel


@router.post("/", summary="Добавить отель")
async def create_hotel(
    hotel_data: HotelAdd = Body(
        description="Данные об отеле", 
        openapi_examples=HOTEL_EXAMPLES
    )
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "OK", "data": hotel}


@router.delete("/{hotel_id}", summary="Удалить отель")
async def delete_hotel(hotel_id: int = Path(description="ID отеля", example=1)):
    async with async_session_maker() as session:       
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()

    return {"status": "OK"}


@router.put("/{hotel_id}", summary="Полностью обновить данные отеля")
async def update_hotel_put(
    hotel_id: int = Path(description="ID отеля", example=1),
    hotel_data: HotelAdd = Body(
        description="Данные об отеле", 
        openapi_examples=HOTEL_EXAMPLES
    )
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частично обновить данные отеля")
async def update_hotel_patch(
    hotel_id: int = Path(description="ID отеля", example=1),
    hotel_data: HotelNullable = Body(
        description="Данные об отеле", 
        openapi_examples=HOTEL_EXAMPLES
    ),
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {"status": "OK"}
