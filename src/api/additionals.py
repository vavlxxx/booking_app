from fastapi import APIRouter, Body

from src.schemas.additionals import AdditionalsRequest
from src.helpers.additionals import ADDITIONALS_EXAMPLES

from src.dependencies.db import DBDep


router = APIRouter(
    prefix="/additionals",
    tags=["Удобства для номеров"],
)


@router.get("/", summary="Получить список всех удобств")
async def get_additionals(
    db: DBDep
):
    additionals = await db.additionals.get_all()
    return additionals


@router.post("/", summary="Добавить новое удобство")
async def create_additional(
    db: DBDep,
    additional_data: AdditionalsRequest = Body(
        description="Название удобства", 
        openapi_examples=ADDITIONALS_EXAMPLES
    )
):
    additional = await db.additionals.add(additional_data)
    await db.commit()
    return {"status": "OK", "data": additional}
