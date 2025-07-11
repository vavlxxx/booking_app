from httpx import AsyncClient

from src.helpers.additionals import ADDITIONALS_EXAMPLES


async def test_get_additionals(ac: AsyncClient):
    response = await ac.get(url="/additionals/")
    data = response.json()["data"]
    assert response.status_code == 200
    assert data is not None
    assert isinstance(data, list)
    assert len(data) == len(ADDITIONALS_EXAMPLES)
