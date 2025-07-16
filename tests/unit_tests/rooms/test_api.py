import pytest

from httpx import AsyncClient

@pytest.mark.parametrize(
        "title, description, quantity, price, discount, additionals_ids, expected_status",[
        ("", "", -5, -3500, -10, [100], 422),
        ("some room", "", -5, -3500, -10, [100], 422),
        ("some room", "some description", -5, -3500, -10, [100], 422),
        ("some room", "some description", 5, -3500, -10, [100], 422),
        ("some room", "some description", 5, 3500, -10, [100], 422),
        ("some room", "some description", 5, 3500, 10, [100], 404),
        ("some room", "some description", 5, 3500, 10, [1], 200),
        ("some room", "some description", 5, 3500, 10, [1], 409),
])
async def test_create_rooms(
    title, 
    description, 
    quantity, 
    price, 
    discount, 
    additionals_ids, 
    expected_status,
    ac: AsyncClient
):
    hotel_id = 1
    result = await ac.post(
        url=f"/hotels/{hotel_id}/rooms", 
        json={
            "title": title,
            "description": description,
            "quantity": quantity,
            "price": price,
            "discount": discount,
            "additionals_ids": additionals_ids
        }
    )
    assert result.status_code == expected_status


@pytest.fixture(scope="module")
async def test_create_temp_room(db_module, ac):
    result = await ac.post(
        url="/hotels/1/rooms",
        json={
            "title": "PATCH TEST ROOM",
            "description": "PATCH TEST ROOM",
            "quantity": 5,
            "price": 3500,
            "discount": 10,
            "additionals_ids": [1,2,3]
        }
    )
    assert result.status_code == 200
    data = result.json()
    assert data is not None and isinstance(data, dict)
    return data["data"]["id"]

@pytest.mark.parametrize(
    "title, description, quantity, price, discount, additionals_ids, expected_status,", [
    ("", "", -5, -3500, -10, [100], 422),
    ("some room", "", -5, -3500, -10, [100], 422),
    ("some room", "some description", -5, -3500, -10, [100], 422),
    ("some room", "some description", 5, -3500, -10, [100], 422),
    ("some room", "some description", 5, 3500, -10, [100], 422),
    ("KOMNATKA", "some description", 5, 3500, 10, [100], 404),
    ("KOMNATKA", "some description", 5, 3500, 10, [1], 200),
])
async def test_patch_rooms(
    title, 
    description, 
    quantity, 
    price, 
    discount, 
    additionals_ids, 
    expected_status,
    ac: AsyncClient,
    test_create_temp_room
):  
    hotel_id = 1
    result = await ac.patch(
        url=f"/hotels/{hotel_id}/rooms/{test_create_temp_room}", 
        json={
            "title": title,
            "description": description,
            "quantity": quantity,
            "price": price,
            "discount": discount,
            "additionals_ids": additionals_ids
        }
    )
    assert result.status_code == expected_status