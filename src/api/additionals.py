import json

from fastapi import APIRouter, Body

from src.schemas.additionals import AdditionalsRequest
from src.helpers.additionals import ADDITIONALS_EXAMPLES
from src.dependencies.db import DBDep
from src.bootstrap import redis_manager


router = APIRouter(
    prefix="/additionals",
    tags=["Удобства для номеров"],
)


@router.get("/", summary="Получить список всех удобств")
async def get_additionals(
    db: DBDep
):
    additionals_from_redis = await redis_manager.get("additionals")
    if not additionals_from_redis:
        additionals = await db.additionals.get_all()
        additionals_dict: list[dict] = [a.model_dump() for a in additionals]
        additionals_json = json.dumps(additionals_dict)
        await redis_manager.set("additionals", additionals_json, 60)
        return additionals

    additionals_dicts = json.loads(additionals_from_redis)
    return additionals_dicts


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
