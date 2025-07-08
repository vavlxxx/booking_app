# ruff: noqa: E402

from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda x: x).start()

import pytest
from httpx import AsyncClient, ASGITransport

from src.dependencies.db import get_db
from src.main import app
from src.db import Base, engine_null_pool, async_session_maker_null_pool
from src.models import * # noqa: F403
from src.config import get_settings
from src.utils.db_manager import DBManager
from src.utils.helpers import get_hotel_examples, get_room_examples


@pytest.fixture(scope="session", autouse=True)
def check_test_env():
    assert get_settings().DB_NAME == "test_booking"
    assert get_settings().MODE == "TEST"


async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture()
async def db():
    async for db in get_db_null_pool():
        yield db


# function (default), module, package, session
@pytest.fixture(scope="session", autouse=True)
async def async_main(check_test_env) -> None:
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        await db.hotels.add_bulk(get_hotel_examples())
        await db.rooms.add_bulk(get_room_examples())
        await db.commit()


@pytest.fixture(scope="session")
async def ac(async_main):
    app_ = ASGITransport(app=app)
    async with AsyncClient(transport=app_, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(async_main, ac):
    resp = await ac.post(
        "/auth/register",
        json={
            "email": "john.johnson@techcorp.com",
            "password": "DevPassword456",
            "first_name": "Джон",
            "last_name": "Джонсон",
            "birthday": "1990-07-22",
            "gender": "М",
        },
    )
    assert resp
    assert resp.status_code == 200
    assert isinstance(resp.json(), dict)


@pytest.fixture(scope="session")
async def authenticated_ac(register_user, ac):
    resp = await ac.post(
        "/auth/login",
        json={"email": "john.johnson@techcorp.com", "password": "DevPassword456"},
    )
    assert resp is not None
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)

    access_token = data.get("access_token")
    assert access_token is not None
    cookie_token = ac.cookies.get("access_token")
    assert cookie_token == access_token
    yield ac
