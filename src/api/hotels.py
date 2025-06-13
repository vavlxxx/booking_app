from fastapi import (
    APIRouter,
    Body,
    Path,
    Query,
)

from sqlalchemy import insert, select, func

from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPATCH
from src.helpers.examples import HOTEL_EXAMPLES
from src.api.dependencies import PaginationDep
from src.db import async_session_maker, engine

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

    async with async_session_maker() as session:
        
        limit = pagination.per_page
        offset = (pagination.page - 1) * limit
        query = select(HotelsOrm)
        
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
        
        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        # print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))
        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels
    


@router.post("/", summary="Создание отеля")
async def create_hotel(
    hotel_data: Hotel = Body(
        description="Данные об отеле", 
        openapi_examples=HOTEL_EXAMPLES
    )
):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        # print(add_hotel_statement.compile(bind=engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удаление отеля по ID")
def delete_hotel(hotel_id: int = Path(description="ID отеля")):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@router.put("/{hotel_id}", summary="Полное обновление данных об отеле по ID")
def update_hotel_put(
    hotel_id: int,
    hotel_data: Hotel,
):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
            return {"status": "OK"}

    return {"status": "NOT FOUND"}


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
