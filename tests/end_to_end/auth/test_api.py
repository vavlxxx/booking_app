import pytest

from httpx import AsyncClient, ASGITransport

from src.main import app


@pytest.fixture
async def _ac(ac: AsyncClient):
    app_ = ASGITransport(app=app)
    async with AsyncClient(transport=app_, base_url="http://test") as ac:
        yield ac


@pytest.mark.parametrize(
    "email, password, first_name, last_name, birthday, gender, register_status", [
    ("johnson@techcorp.com", "DevPassword456", "Джон", "Джонсон", "1990-07-22", "М", 200),
    ("johnson@techcorp.com", "DevPassword456", "Джон", "Джонсон", "1990-07-22", "М", 400),
    ("maria@techcorp.com", "DevPassword456", "Мария", "Джонсон", "1990-07-22", "Ж", 200),
])
async def test_auth_flow(email, password, first_name, last_name, birthday, gender, register_status, _ac):
    response = await _ac.post(
        url="/auth/register",
        json={
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "birthday": birthday,
            "gender": gender
        }
    )
    assert response.status_code == register_status
    if response.status_code != 200:
        return

    response = await _ac.post(
        url="/auth/login",
        json={
            "email": email,
            "password": password
        }
    )
    assert response.status_code == 200
    
    data = response.json()
    response_token = data.get("access_token")
    cookies_token = _ac.cookies.get("access_token")
    assert response_token and cookies_token
    assert response_token == cookies_token

    response = await _ac.get("/auth/profile")
    assert response.status_code == 200
    data = response.json()
    assert data and isinstance(data, dict)
    
    assert data["email"] == email 
    assert data["first_name"] == first_name 
    assert data["last_name"] == last_name 
    assert data["gender"] == gender 
    assert data["birthday"] == birthday

    response = await _ac.delete("/auth/logout")
    assert response.status_code == 200
    cookies_token = _ac.cookies.get("access_token")
    assert cookies_token is None
