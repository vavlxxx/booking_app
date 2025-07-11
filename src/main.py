
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import logging
from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi_cache import FastAPICache
# from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.backends.redis import RedisBackend


from src.api.hotels import router as router_hotels
from src.api.auth import router as router_auth
from src.api.rooms import router as router_rooms
from src.api.bookings import router as router_bookings
from src.api.additionals import router as router_additionals
from src.api.images import router as router_images

# from src.config import get_settings
from src.helpers.docs import router as router_docs
from src.bootstrap import redis_manager


logging.basicConfig(level=logging.INFO)



@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Application is starting...")
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager._redis), prefix="fastapi-cache")
    logging.info("FastAPICache initialized...")
    yield 
    await redis_manager.close()
    logging.info("Application is shutting down...")

# if get_settings().MODE == "TEST":
#     FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")


app = FastAPI(
    docs_url=None,
    redoc_url=None,
    lifespan=lifespan
)

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
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


app.include_router(router_docs)
app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_additionals)
app.include_router(router_images)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
