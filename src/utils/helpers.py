from collections import defaultdict
import random

from src.schemas.base import BasePydanticModel

from src.helpers.hotels import HOTEL_EXAMPLES
from src.helpers.rooms import ROOM_EXAMPLES
from src.helpers.additionals import ADDITIONALS_EXAMPLES

from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.schemas.additionals import AdditionalsRequest


def get_hotel_examples() -> tuple[BasePydanticModel]:
    result = []
    for _, example in HOTEL_EXAMPLES.items():
        data = example.get("value", {})
        instance = HotelAdd(**data) # type: ignore
        result.append(instance)
    return tuple(result)


def get_random_ids(max_id: int, min=1, max=4):
    random_ids = []
    quantity = int(random.randint(1, 4))
    while len(random_ids) < quantity:
        rand_id = random.randint(1, max_id)
        if rand_id not in random_ids:
            random_ids.append(rand_id)
    return random_ids


def get_room_examples() -> tuple[RoomAdd]:
    result = []
    for _, example in ROOM_EXAMPLES.items():
        data = example.get("value", {})
        for hotel_id in get_random_ids(len(HOTEL_EXAMPLES)):
            instance = RoomAdd(**data, hotel_id=hotel_id) # type: ignore
            result.append(instance)
    return tuple(result)


def get_additionals_examples() -> tuple[AdditionalsRequest]:
    result = []
    for _, example in ADDITIONALS_EXAMPLES.items():
        data = example.get("value", {})
        instance = AdditionalsRequest(**data) # type: ignore
        result.append(instance)
    return tuple(result)


def get_rooms_additionals_examples(rooms_quantity: int) -> tuple[tuple[int, list[int]], ...]:
    result = defaultdict(list)
    for additional_id in range(1, len(ADDITIONALS_EXAMPLES) + 1):
        for room_id in get_random_ids(rooms_quantity):
            result[room_id].append(additional_id)
    return tuple(result.items())
