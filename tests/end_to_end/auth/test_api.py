import pytest


@pytest.mark.parametrize(
    "email, password, first_name, last_name, birthday, gender, register_status", [
    ("johnson@techcorp.com", "DevPassword456", "Джон", "Джонсон", "1990-07-22", "М", 200),
    ("johnson@techcorp.com", "DevPassword456", "Джон", "Джонсон", "1990-07-22", "М", 409),
    ("12345", "DevPassword456", "Мария", "Джонсон", "1990-07-22", "Ж", 422),
])
async def test_auth_flow(email, password, first_name, last_name, birthday, gender, register_status, ac):
    response = await ac.post(
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

    response = await ac.post(
        url="/auth/login",
        json={
            "email": email,
            "password": password
        }
    )
    assert response.status_code == 200
    
    data = response.json()
    response_token = data.get("access_token")
    cookies_token = ac.cookies.get("access_token")
    assert response_token and cookies_token
    assert response_token == cookies_token

    response = await ac.get("/auth/profile")
    assert response.status_code == 200
    data = response.json()
    assert data and isinstance(data, dict)
    
    response = await ac.post("/auth/logout")
    assert response.status_code == 200
    cookies_token = ac.cookies.get("access_token")
    assert cookies_token is None
