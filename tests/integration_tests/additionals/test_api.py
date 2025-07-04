from httpx import AsyncClient


async def test_add_additionals(ac: AsyncClient):
    title = "Бесплатный Wi-Fi"
    descr = "Высокоскоростной беспроводный интернет во всех номерах"
    response = await ac.post(
        url=f"/additionals/",
        json={
            "name": title,
            "description": descr
        }
    )
    data = response.json()
    assert response.status_code == 200
    assert data is not None
    assert isinstance(data, dict)
    assert data["data"]["name"] == title
    assert data["data"]["description"] == descr
    
    

async def test_get_additionals(ac: AsyncClient):
    response = await ac.get(url=f"/additionals/")
    data = response.json()
    assert response.status_code == 200
    assert data is not None
    assert isinstance(data, list)