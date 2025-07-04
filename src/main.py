
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.api.hotels import router as router_hotels
from src.api.auth import router as router_auth
from src.api.rooms import router as router_rooms
from src.api.bookings import router as router_bookings
from src.api.additionals import router as router_additionals
from src.api.images import router as router_images
from src.helpers.docs import router as router_docs
from src.bootstrap import redis_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application is starting...")
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    yield 
    await redis_manager.close()
    print("Application is shutting down...")

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    lifespan=lifespan
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
