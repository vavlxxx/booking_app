from datetime import date, timedelta

from httpx import AsyncClient

from src.utils.db_manager import DBManager


async def test_create_booking(authenticated_ac: AsyncClient, db: DBManager):
    room = (await db.rooms.get_all())[0]
    date_from = (date.today()+timedelta(days=1)).strftime("%Y-%m-%d")
    date_to = (date.today()+timedelta(days=10)).strftime("%Y-%m-%d")
    response = await authenticated_ac.post(
        url=f"/bookings/",
        json={
            "room_id": room.id,
            "date_from": date_from,
            "date_to": date_to
        }
    )

    assert response is not None
    data = response.json()
    assert response.status_code == 200
    assert data is not None
    assert isinstance(response.json(), dict)

    assert data["room_id"] == room.id
    assert data["date_from"] == date_from
    assert data["date_to"] == date_to
