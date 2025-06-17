from fastapi import (
    APIRouter,
    Body,
    Path,
)

from src.schemas.hotels import HotelAdd, HotelNullable
from src.helpers.hotels import HOTEL_EXAMPLES
from src.api.dependencies import (
    PaginationDep, 
    HoteParamslDep, 
    DBDep
)


router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get("/", summary="Получить список отелей")
async def get_hotels(
    pagination: PaginationDep, 
    hotel_filter_data: HoteParamslDep,
    db: DBDep
):
    hotels = await db.hotels.get_all_filtered(
        location=hotel_filter_data.location,
        title=hotel_filter_data.title,
        limit=pagination.per_page,
        offset=(pagination.page - 1) * pagination.per_page,
    )    
    return hotels


@router.get("/{hotel_id}", summary="Получить отель")
async def get_hotel(
    db: DBDep,
    hotel_id: int = Path(description="ID отеля", example=1)
):
    hotel = await db.hotels.check_existence(id=hotel_id)
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
    hotel_id: int = Path(description="ID отеля", example=1)
):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}", summary="Полностью обновить данные отеля")
async def update_hotel_put(
    db: DBDep,
    hotel_id: int = Path(description="ID отеля", example=1),
    hotel_data: HotelAdd = Body(
        description="Данные об отеле", 
        openapi_examples=HOTEL_EXAMPLES
    )
):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частично обновить данные отеля")
async def update_hotel_patch(
    db: DBDep,
    hotel_id: int = Path(description="ID отеля", example=1),
    hotel_data: HotelNullable = Body(
        description="Данные об отеле", 
        openapi_examples=HOTEL_EXAMPLES
    ),
):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}
