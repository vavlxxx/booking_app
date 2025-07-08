from fastapi import APIRouter, Body, HTTPException, Response

from src.services.auth import AuthService

from src.dependencies.db import DBDep
from src.dependencies.auth import UserIdDep
from src.utils.exceptions import (
    ObjectNotFoundException,
    ObjectAlreadyExistsException
)

from src.schemas.auth import (
     UserFullInfo,
     UserRegister, 
     UserRegisterRequest, 
     UserLoginRequest
)
from src.helpers.auth import (
    USER_REGISTER_EXAMPLES, 
    USER_LOGIN_EXAMPLES
)

router = APIRouter(prefix="/auth", tags=["Авторизация и Аутентификация"])


@router.post("/register", summary="Зарегистрироваться")
async def register_user(
    db: DBDep,
    user_data: UserRegisterRequest = Body(
        description="Данные о пользователе",
        openapi_examples=USER_REGISTER_EXAMPLES
)):
    hashed_password = AuthService().hash_password(user_data.password)
    data = user_data.model_dump(exclude={"password"})
    new_user_data = UserRegister(**data, hashed_password=hashed_password)
    
    try:
        user = await db.auth.add(new_user_data)
    except ObjectAlreadyExistsException:
        raise HTTPException(status_code=404, detail="Пользователь с таким email уже существует")
    await db.commit()

    return {"status": "OK", "data": user}


@router.post("/login", summary="Пройти аутентификацию")
async def login_user(
    db: DBDep,
    response: Response = Response(status_code=200),
    user_data: UserLoginRequest = Body(
        description="Лоигин и пароль",
        openapi_examples=USER_LOGIN_EXAMPLES
    ),
):  
    try:
        user: UserFullInfo = await db.auth.get_user_with_passwd(email=user_data.email)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    password_is_valid =  AuthService().verify_password(user_data.password, user.hashed_password)

    if user is None or not password_is_valid:
        raise HTTPException(status_code=401, detail="Неверные логин или пароль")
        
    access_token = AuthService.create_access_token({"user_id": user.id})
    response.set_cookie(key="access_token", value=access_token)
    return {"status": "OK", "access_token": access_token}


@router.get("/profile", summary="Получить профиль аутентифицированного пользователя")
async def only_auth(
        user_id: UserIdDep,
        db: DBDep
):      
        try:
            user = await db.auth.get_one(id=user_id)
        except ObjectNotFoundException:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        return user


@router.delete("/logout", summary="Выйти из аккаунта")
async def logout_user(
    user_id: UserIdDep,
    response: Response = Response(status_code=200)
):
    response.delete_cookie(key="access_token")
    return {"status": "OK"}