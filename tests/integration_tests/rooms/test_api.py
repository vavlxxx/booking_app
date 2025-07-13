from src.helpers.additionals import ADDITIONALS_EXAMPLES
from src.utils.helpers import get_random_ids


async def test_change_additionals_in_room(
    ac,
    db,
):
    rooms = await db.rooms.get_all()
    room_id, hotel_id = rooms[0].id, rooms[0].hotel_id
    
    response = await ac.get(
        url=f"hotels/{hotel_id}/rooms/{room_id}"
    )
    assert response.status_code == 200
    
    data = response.json()["data"]
    assert data is not None
    assert isinstance(data, dict)
    assert "additionals" in data
    
    additionals_ids_before_change = []
    for additional in data["additionals"]:
        additionals_ids_before_change.append(additional["id"])

    new_additionals_ids = get_random_ids(len(ADDITIONALS_EXAMPLES), exclude=additionals_ids_before_change)
    response = await ac.patch(
        url=f"hotels/{hotel_id}/rooms/{room_id}", 
        json={"additionals_ids": new_additionals_ids})
    assert response.status_code == 200
    
    response = await ac.get(
        url=f"hotels/{hotel_id}/rooms/{room_id}"
    )
    assert response.status_code == 200

    data = response.json()["data"]
    assert data is not None
    assert isinstance(data, dict)
    assert "additionals" in data

    additionals_ids_after_change = []
    for additional in data["additionals"]:
        additionals_ids_after_change.append(additional["id"])

    assert sorted(additionals_ids_after_change) != sorted(additionals_ids_before_change)
    assert sorted(additionals_ids_after_change) == sorted(new_additionals_ids)
