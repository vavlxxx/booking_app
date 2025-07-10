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
from src.services.hotels import HotelsService

from src.utils.exceptions import (
    DatesMissMatchException,
    DatesMissMatchHTTPException,
    ObjectNotFoundException,
    HotelNotFoundException,
    HotelNotFoundHTTPException,
    InvalidDataHTTPException,
    InvalidDataException,
    NotEmptyHotelException,
    NotEmptyHotelHTTPException
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
        hotels = await HotelsService(db).get_hotels(pagination, hotel_filter_data, dates)
    except DatesMissMatchException:
        raise DatesMissMatchHTTPException
    except InvalidDataException:
        raise InvalidDataHTTPException
    return {
        "status": "OK",
        "page": pagination.page,
        "offset": pagination.offset,
        "detail": "Отели были успешно получены", 
        "data": hotels
    }


@router.get("/{hotel_id}", summary="Получить отель")
async def get_hotel(
    db: DBDep,
    hotel_id: int = Path(description="ID отеля")
):  
    try:
        hotel = await HotelsService(db).get_hotel(hotel_id=hotel_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except NotEmptyHotelException:
        raise NotEmptyHotelHTTPException
    except InvalidDataException:
        raise InvalidDataHTTPException
    return {"status": "OK", "detail": "Отель был успешно получен", "data": hotel}


@router.post("/", summary="Добавить отель")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        description="Данные об отеле", 
        openapi_examples=HOTEL_EXAMPLES
    )
):
    hotel = await HotelsService(db).add_hotel(hotel_data) # type: ignore
    return {"status": "OK", "detail": "Отель был успешно добавлен", "data": hotel}


@router.delete("/{hotel_id}", summary="Удалить отель")
async def delete_hotel(
    db: DBDep,
    hotel_id: int = Path(description="ID отеля")
):  
    try:
        await HotelsService(db).delete_hotel(hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    except InvalidDataException:
        raise InvalidDataHTTPException
    except NotEmptyHotelException:
        raise HTTPException(status_code=422, detail="Нельзя удалить отель с номерами")
    
    return {"status": "OK", "detail": "Отель был успешно удалён"}


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
        await HotelsService(db).edit_hotel(hotel_id=hotel_id, hotel_data=hotel_data) # type: ignore
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    except InvalidDataException:
        raise InvalidDataHTTPException
    return {"status": "OK", "detail": "Отель был успешно полностью обновлен"}


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
        await HotelsService(db).edit_hotel(hotel_id=hotel_id, hotel_data=hotel_data) # type: ignore
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    except InvalidDataException:
        raise InvalidDataHTTPException
    return {"status": "OK", "detail": "Отель был успешно частично обновлен"}
