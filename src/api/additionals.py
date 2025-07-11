from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.services.additionals import AdditionalsService
from src.schemas.additionals import AdditionalsRequest
from src.helpers.additionals import ADDITIONALS_EXAMPLES
from src.dependencies.db import DBDep


router = APIRouter(
    prefix="/additionals",
    tags=["Удобства для номеров"],
)


@router.get("/", summary="Получить список всех удобств")
@cache(expire=120)
async def get_additionals(
    db: DBDep
):  
    additionals = await AdditionalsService(db).get_additionals()
    return {
        "status": "OK",
        "detail": "Удобства были успешно получены",
        "data": additionals
    }


@router.post("/", summary="Добавить новое удобство")
async def create_additional(
    db: DBDep,
    additional_data: AdditionalsRequest = Body(
        description="Название удобства", 
        openapi_examples=ADDITIONALS_EXAMPLES
    )
):
    additional = await AdditionalsService(db).add_additional(additional_data)
    return {
        "status": "OK", 
        "detail": "Удобство было успешно добавлено",
        "data": additional
    }
