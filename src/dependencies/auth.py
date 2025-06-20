from typing import Annotated

from fastapi import Depends, HTTPException, Request

from src.services.auth import AuthService


def get_token(request: Request) -> str | None:
    access_token = request.cookies.get("access_token", None)
    if access_token is None:
        raise HTTPException(status_code=401, detail="Пользователь не аутентифицирован. Пожалуйста, пройдите аутентификацию")
    return access_token


def get_current_user(access_token: str = Depends(get_token)):
    data = AuthService.decode_access_token(access_token)
    return data.get("user_id")
    
UserIdDep = Annotated[int, Depends(get_current_user)]
