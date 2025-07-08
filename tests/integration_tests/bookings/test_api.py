from datetime import date, timedelta

import pytest

from httpx import AsyncClient

from tests.conftest import get_db_null_pool


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code", [
    (1, (date.today()+timedelta(days=1)).strftime("%Y-%m-%d"), (date.today()+timedelta(days=10)).strftime("%Y-%m-%d"), 200),
    (1, (date.today()+timedelta(days=1)).strftime("%Y-%m-%d"), (date.today()+timedelta(days=10)).strftime("%Y-%m-%d"), 200),
    (1, (date.today()+timedelta(days=1)).strftime("%Y-%m-%d"), (date.today()+timedelta(days=10)).strftime("%Y-%m-%d"), 200),
    (1, (date.today()+timedelta(days=1)).strftime("%Y-%m-%d"), (date.today()+timedelta(days=10)).strftime("%Y-%m-%d"), 200),
    (1, (date.today()+timedelta(days=1)).strftime("%Y-%m-%d"), (date.today()+timedelta(days=10)).strftime("%Y-%m-%d"), 200),
    (1, (date.today()+timedelta(days=1)).strftime("%Y-%m-%d"), (date.today()+timedelta(days=10)).strftime("%Y-%m-%d"), 400),
])
async def test_create_booking(
    room_id, 
    date_from, 
    date_to, 
    status_code,
    authenticated_ac: AsyncClient
):
    response = await authenticated_ac.post(
        url="/bookings/",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to
        }
    )

    assert response is not None
    assert response.status_code == status_code
    if response.status_code != 200:
        return
    
    data = response.json()
    assert data is not None
    assert isinstance(response.json(), dict)

    assert data["room_id"] == room_id
    assert data["date_from"] == date_from
    assert data["date_to"] == date_to


@pytest.fixture(scope="session")
async def delete_all_bookings() -> None:
    async for _db in get_db_null_pool():
        await _db.bookings.delete()
        await _db.commit()
    


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code_for_post, status_code_for_get, count", [
    (1, (date.today()+timedelta(days=1)).strftime("%Y-%m-%d"), (date.today()+timedelta(days=10)).strftime("%Y-%m-%d"), 200, 200, 1),
    (1, (date.today()+timedelta(days=1)).strftime("%Y-%m-%d"), (date.today()+timedelta(days=10)).strftime("%Y-%m-%d"), 200, 200, 2),
    (1, (date.today()+timedelta(days=1)).strftime("%Y-%m-%d"), (date.today()+timedelta(days=10)).strftime("%Y-%m-%d"), 200, 200, 3),
    (1, (date.today()+timedelta(days=1)).strftime("%Y-%m-%d"), (date.today()+timedelta(days=10)).strftime("%Y-%m-%d"), 200, 200, 4),
    (1, (date.today()+timedelta(days=1)).strftime("%Y-%m-%d"), (date.today()+timedelta(days=10)).strftime("%Y-%m-%d"), 200, 200, 5),
    (1, (date.today()+timedelta(days=1)).strftime("%Y-%m-%d"), (date.today()+timedelta(days=10)).strftime("%Y-%m-%d"), 400, 200, 5),
])
async def test_add_and_get_bookings(
    room_id, 
    date_from, 
    date_to, 
    status_code_for_post,
    status_code_for_get,
    count,
    authenticated_ac: AsyncClient,
    delete_all_bookings,
):
    response = await authenticated_ac.post(
        url="/bookings/",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to
        }
    )

    assert response is not None
    assert response.status_code == status_code_for_post

    if response.status_code == 200:
        data = response.json()
        assert data is not None
        assert isinstance(response.json(), dict)

        assert data["room_id"] == room_id
        assert data["date_from"] == date_from
        assert data["date_to"] == date_to

    response = await authenticated_ac.get(url="/bookings/me")
    assert response.status_code == status_code_for_get

    if response.status_code == 200:
        data = response.json()
        assert data is not None
        assert isinstance(data, list)
        assert len(data) == count
    