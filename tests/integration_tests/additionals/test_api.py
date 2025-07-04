from httpx import AsyncClient

from src.utils.db_manager import DBManager


async def test_add_additionals(ac: AsyncClient, db: DBManager):
    response = await ac.post(
        url=f"/additionals/",
        json={
            "name": "Бесплатный Wi-Fi",
            "description": "Высокоскоростной беспроводной интернет во всех номерах"
        }
    )
    assert response.status_code == 200
    

async def test_get_additionals(ac: AsyncClient, db: DBManager):
    response = await ac.get(url=f"/additionals/")
    assert response.status_code == 200
    assert response.json() is not None