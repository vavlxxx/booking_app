from fastapi import APIRouter, Body, Response

from src.services.auth import AuthService

from src.dependencies.db import DBDep
from src.dependencies.auth import UserIdDep
from src.utils.exceptions import (
    IncorrentLoginDataException,
    IncorrentLoginDataHTTPException,
    UserNotFoundException,
    UserNotFoundHTTPException,
    UserAlreadyExistsException,
    UserAlreadyExistsHTTPException,
)

from src.schemas.auth import UserRegisterRequest, UserLoginRequest, UserUpdateRequest
from src.helpers.auth import USER_REGISTER_EXAMPLES, USER_LOGIN_EXAMPLES

router = APIRouter(prefix="/auth", tags=["Авторизация и Аутентификация"])


@router.post("/register", summary="Зарегистрироваться 💻")
async def register_user(
    db: DBDep,
    user_data: UserRegisterRequest = Body(
        description="Данные о пользователе", openapi_examples=USER_LOGIN_EXAMPLES
    ),
):
    try:
        await AuthService(db).add_user(user_data)
    except UserAlreadyExistsException as exc:
        raise UserAlreadyExistsHTTPException from exc

    return {"status": "OK"}


@router.post("/login", summary="Пройти аутентификацию 💻")
async def login_user(
    db: DBDep,
    response: Response = Response(status_code=200),
    user_data: UserLoginRequest = Body(
        description="Лоигин и пароль", openapi_examples=USER_LOGIN_EXAMPLES
    ),
):
    try:
        access_token = await AuthService(db).login_user(response=response, user_data=user_data)
    except IncorrentLoginDataException as exc:
        raise IncorrentLoginDataHTTPException from exc

    return {"status": "OK", "access_token": access_token}


@router.patch("/edit", summary="Обновить данные профиля аутентифицированного пользователя 💻")
async def edit_user(
    user_id: UserIdDep,
    db: DBDep,
    user_data: UserUpdateRequest = Body(
        description="Данные о пользователе", openapi_examples=USER_REGISTER_EXAMPLES
    ),
):
    try:
        await AuthService(db).edit_user(user_data, user_id=user_id)
    except UserNotFoundException as exc:
        raise UserNotFoundHTTPException from exc
    return {"status": "OK"}


@router.get("/profile", summary="Получить профиль аутентифицированного пользователя 💻")
async def only_auth(user_id: UserIdDep, db: DBDep):
    try:
        user = await AuthService(db).get_user(user_id=user_id)
    except UserNotFoundException as exc:
        raise UserNotFoundHTTPException from exc
    return user


@router.post("/logout", summary="Выйти из аккаунта 💻")
async def logout_user(_: UserIdDep, response: Response = Response(status_code=200)):
    response.delete_cookie(key="access_token")
    return {"status": "OK"}
