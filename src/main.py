import uvicorn
from fastapi import FastAPI

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as router_hotels
from src.helpers.docs import router as router_docs

app = FastAPI(docs_url=None, redoc_url=None)
app.include_router(router_hotels)
app.include_router(router_docs)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
