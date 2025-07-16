from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.types import ASGIApp


class LimitUploadSize(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, max_upload_size: int) -> None:
        super().__init__(app)
        self.max_upload_size = max_upload_size

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> JSONResponse:
        if request.method == 'POST':
            if 'content-length' not in request.headers:
                return JSONResponse(
                    status_code=status.HTTP_411_LENGTH_REQUIRED,
                    content={
                        "detail": "Content-Length header is required"
                    }
                )
            
            content_length = int(request.headers['content-length'])
            if content_length > self.max_upload_size:
                max_size_mb = self.max_upload_size / 1024 / 1024
                actual_size_mb = content_length / 1024 / 1024
                return JSONResponse(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    content={
                        "detail": f"Размер файла превышает допустимый лимит. Максимум: {max_size_mb:.1f}MB, Размер файла: {actual_size_mb:.1f}MB"
                    }
                )
        
        return await call_next(request)
