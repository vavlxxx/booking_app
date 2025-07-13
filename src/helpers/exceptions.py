from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException, RequestValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "ERROR",
            "detail": exc.errors(),
        },
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    status = getattr(exc, 'status', 'ERROR')
    
    response_content = {
        "detail": exc.detail,
        "status": status
    }
    
    return JSONResponse(
        status_code=exc.status_code,
        content=response_content,
        headers=exc.headers
    )
