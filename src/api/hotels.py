from fastapi_cache.decorator import cache
from fastapi import (
    APIRouter,
    Body,
    HTTPException,
    Path,
)

from src.schemas.hotels import HotelAdd, HotelNullable
from src.helpers.hotels import HOTEL_EXAMPLES
from src.dependencies.hotels import HoteParamsDep, PaginationDep
from src.dependencies.db import DBDep
from src.dependencies.rooms import DateDep
from src.utils.exceptions import (
    DatesMissMatchException,
    ObjectNotFoundException
)


router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get("/", summary="Получить список отелей со свободными номерами за указанный период")
@cache(expire=120)
async def get_hotels(
    pagination: PaginationDep, 
    hotel_filter_data: HoteParamsDep,
    dates: DateDep,
    db: DBDep
):  
    try:
        hotels = await db.hotels.get_all_filtered_by_time(
            location=hotel_filter_data.location,
            title=hotel_filter_data.title,
            limit=pagination.per_page,
            offset=pagination.offset,
            date_from=dates.date_from,
            date_to=dates.date_to
        )
    except DatesMissMatchException as ex:
        raise HTTPException(status_code=422, detail=ex.detail)
    return hotels


@router.get("/{hotel_id}", summary="Получить отель")
async def get_hotel(
    db: DBDep,
    hotel_id: int = Path(description="ID отеля")
):  
    try:
        hotel = await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Отель не найден")
    return hotel


@router.post("/", summary="Добавить отель")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        description="Данные об отеле", 
        openapi_examples=HOTEL_EXAMPLES
    )
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "OK", "data": hotel}


@router.delete("/{hotel_id}", summary="Удалить отель")
async def delete_hotel(
    db: DBDep,
    hotel_id: int = Path(description="ID отеля")
):  
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Отель не найден")

    rooms = await db.rooms.get_all_filtered(hotel_id=hotel_id)
    if rooms is not None and len(rooms) > 0:
        raise HTTPException(status_code=403, detail="Нельзя удалить отель, который содержит номера")

    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}", summary="Полностью обновить данные отеля")
async def update_hotel_put(
    db: DBDep,
    hotel_id: int = Path(description="ID отеля"),
    hotel_data: HotelAdd = Body(
        description="Данные об отеле", 
        openapi_examples=HOTEL_EXAMPLES
    )
):  
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Отель не найден")

    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частично обновить данные отеля")
async def update_hotel_patch(
    db: DBDep,
    hotel_id: int = Path(description="ID отеля"),
    hotel_data: HotelNullable = Body(
        description="Данные об отеле", 
        openapi_examples=HOTEL_EXAMPLES
    ),
):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Отель не найден")

    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}
