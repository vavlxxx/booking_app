from fastapi import APIRouter, Body

from src.api.dependencies import DBDep
from src.schemas.additionals import AdditionalRequest
from src.helpers.additionals import ADDITIONALS_EXAMPLES


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
    additional_data: AdditionalRequest = Body(
        description="Название удобства", 
        openapi_examples=ADDITIONALS_EXAMPLES
    )
):
    additional = await db.additionals.add(additional_data)
    await db.commit()
    return {"status": "OK", "data": additional}
