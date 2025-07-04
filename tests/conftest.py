import pytest

from httpx import AsyncClient, ASGITransport

from src.main import app
from src.db import Base, engine_null_pool
from src.models import *
from src.config import get_settings


@pytest.fixture(scope="session", autouse=True)
def check_test_env():
    assert get_settings().DB_NAME == "test_booking"
    assert get_settings().MODE == "TEST"


# function, module, package, session 
@pytest.fixture(scope="session", autouse=True)
async def async_main(check_test_env) -> None:
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def register_user(async_main):
    app_ = ASGITransport(app=app)
    async with AsyncClient(transport=app_, base_url="http://test") as client:
        resp = await client.post(
            "/auth/register", 
            json={
                "email": "john.johnson@techcorp.com",
                "password": "DevPassword456",
                "first_name": "Джон",
                "last_name": "Джонсон",
                "birthday": "1990-07-22",
                "gender": "М"
            }
        )
        
        assert resp
        assert resp.status_code == 200
        
        