from datetime import date, timedelta

from httpx import AsyncClient


async def test_get_hotels(ac: AsyncClient):
    response = await ac.get(
        url="/hotels/",
        params={
            "date_from": (date.today()+timedelta(days=1)).strftime("%Y-%m-%d"), 
            "date_to": (date.today()+timedelta(days=10)).strftime("%Y-%m-%d")
        }
    )
    assert response.status_code == 200
    assert response.json() is not None
    assert isinstance(response.json(), list)
