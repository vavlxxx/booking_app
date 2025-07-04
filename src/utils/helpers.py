import random

from src.schemas.base import BasePydanticModel

from src.helpers.hotels import HOTEL_EXAMPLES
from src.helpers.rooms import ROOM_EXAMPLES

from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd


def get_hotel_examples() -> tuple[BasePydanticModel]:
    result = []
    for _, example in HOTEL_EXAMPLES.items():
        data = example.get("value")
        instance = HotelAdd(**data)
        result.append(instance)
    return result


def _get_random_hotel_ids():
    hotel_ids = []
    hotels_quantity = int(random.randint(1, 4))
    while len(hotel_ids) < hotels_quantity:
        rand_id = random.randint(1, len(HOTEL_EXAMPLES))
        if rand_id not in hotel_ids:
            hotel_ids.append(rand_id)
    return hotel_ids


def get_room_examples():
    result = []
    for _, example in ROOM_EXAMPLES.items():
        data = example.get("value")
        for hotel_id in _get_random_hotel_ids():
            instance = RoomAdd(**data, hotel_id=hotel_id)
            result.append(instance)
    return result
