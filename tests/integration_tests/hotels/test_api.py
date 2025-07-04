from httpx import AsyncClient

from src.utils.db_manager import DBManager


async def test_get_hotels(ac: AsyncClient, db: DBManager):
    response = await ac.get(
        url=f"/hotels/",
        params={"date_from": "2023-01-01", "date_to": "2023-01-10"}
    )
    assert response.status_code == 200
    assert response.json() is not None
