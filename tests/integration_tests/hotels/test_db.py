from src.db import async_session_maker_null_pool
from src.schemas.hotels import HotelAdd
from src.utils.db_manager import DBManager


# @pytest.mark.asyncio
async def test_add_hotel(db):
    hotel_data = {
        "title": "Hotel EXTRA",
        "location": "г. Москва, ул. Пушкинская, д. 5",
        "description": "Описание отеля",
    }
    hotel_schema = HotelAdd(**hotel_data)
    hotel = await db.hotels.add(hotel_schema)
    await db.commit()
    print(f"Hotel added: {hotel}")
