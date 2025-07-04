from src.db import async_session_maker_null_pool
from src.schemas.hotels import HotelAdd
from src.utils.db_manager import DBManager


# @pytest.mark.asyncio
async def test_add_hotel():
    hotel_data = {"title": "Hotel Extra", "location": "г. Москва, ул. Пушкинская, д. 5"}
    hotel_schema = HotelAdd(**hotel_data)
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        hotel = await db.hotels.add(hotel_schema)
        await db.commit()
        print(f"Hotel added: {hotel}")