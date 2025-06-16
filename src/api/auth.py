from fastapi import APIRouter, Body, HTTPException, Response

from src.db import async_session_maker
from src.schemas.auth import UserRegister, UserRegisterRequest, UserLoginRequest
from src.repos.auth import AuthRepository
from src.helpers.auth import USER_REGISTER_EXAMPLES, USER_LOGIN_EXAMPLES
from src.services.auth import AuthService
from src.api.dependencies import UserIdDep

router = APIRouter(prefix="/auth", tags=["Авторизация и Аутентификация"])


@router.post("/register", summary="Зарегистрироваться")
async def register_user(
    user_data: UserRegisterRequest = Body(
        description="Данные о пользователе",
        openapi_examples=USER_REGISTER_EXAMPLES
)):
    hashed_password = AuthService().get_hashed_password(user_data.password)
    new_user_data = UserRegister(**user_data.model_dump(exclude={"password"}), hashed_password=hashed_password)
    async with async_session_maker() as session:
        user = await AuthRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "OK", "data": user}


@router.post("/login", summary="Авторизоваться")
async def login_user(
    response: Response = Response(status_code=200),
    user_data: UserLoginRequest = Body(
        description="Лоигин и пароль",
        openapi_examples=USER_LOGIN_EXAMPLES
    ),
):  
    async with async_session_maker() as session:
        user = await AuthRepository(session).get_user_with_passwd(email=user_data.email)
        password_is_valid =  AuthService().verify_password(user_data.password, user.hashed_password)

        if user is None or not password_is_valid:
            raise HTTPException(status_code=401, detail="Неверные логин или пароль")
        
        access_token = AuthService.create_access_token({"user_id": user.id})
        response.set_cookie(key="access_token", value=access_token)
        return {"status": "OK", "access_token": access_token}


@router.get("/profile", summary="Получить профиль")
async def only_auth(
        user_id: UserIdDep
):

    async with async_session_maker() as session:
        user = await AuthRepository(session).get_one_or_none(id=user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        return user


@router.delete("/logout", summary="Выйти из аккаунта")
async def logout_user(response: Response = Response(status_code=200)):
    response.delete_cookie(key="access_token")
    return {"status": "OK"}