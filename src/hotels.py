from fastapi import (
    APIRouter, 
    Body, 
    Path, 
    Depends,
)

from schemas.hotels import Hotel, HotelPATCH, HotelQueryParams
from helpers.examples import HOTEL_EXAMPLES

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)

hotels = [
    {"id": 1, "title": "Sochi", "name": "Hotel Sochi"},
    {"id": 2, "title": "Dubai", "name": "Hotel Dubai"},
    {"id": 3, "title": "New York", "name": "Hotel New York"},
    {"id": 4, "title": "Paris", "name": "Hotel Paris"},
    {"id": 5, "title": "London", "name": "Hotel London"},
    {"id": 6, "title": "Moscow", "name": "Hotel Moscow"},
    {"id": 7, "title": "Tokyo", "name": "Hotel Tokyo"},
    {"id": 8, "title": "Beijing", "name": "Hotel Beijing"},
    {"id": 9, "title": "Sydney", "name": "Hotel Sydney"},
    {"id": 10, "title": "Rio de Janeiro", "name": "Hotel Rio de Janeiro"},
]


@router.get("/", summary="Получение списка отелей")
def get_hotels(params: HotelQueryParams = Depends()):  

    hotels_ = []
    start = (params.page-1)*params.per_page
    
    for hotel in hotels[start:start+params.per_page]:
        if params.id_ and hotel["id"] == params.id_:
            continue
        if params.title and hotel["title"] != params.title:
            continue
        hotels_.append(hotel)
    return hotels_


@router.post("/", summary="Создание отеля")
def create_hotel(
    hotel_data: Hotel = Body(
        description="Данные об отеле", 
        openapi_examples=HOTEL_EXAMPLES
        )
    ):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
    })
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
            hotel["title"] = hotel_data.title if hotel_data.title is not None else hotel["title"]
            hotel["name"] = hotel_data.name if hotel_data.name is not None else hotel["name"]
            return {"status": "OK"}
        
    return {"status": "NOT FOUND"}
