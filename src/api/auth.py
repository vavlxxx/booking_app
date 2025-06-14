from fastapi import APIRouter, Body

from src.db import async_session_maker
from src.schemas.auth import UserAuthentication, UserAdd
from src.repos.auth import AuthRepository
from src.helpers.examples import USER_EXAMPLES

router = APIRouter(prefix="/auth", tags=["Авторизация и Аутентификация"])


@router.post("/register", summary="Зарегистрироваться")
async def register_user(user_data: UserAuthentication = Body(
    description="Данные о пользователе",
    openapi_examples=USER_EXAMPLES
)):

    new_user_data: UserAdd = user_data.hash_password()
    async with async_session_maker() as session:
        user = await AuthRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "OK", "data": user}
