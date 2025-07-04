from datetime import date, timedelta

from src.schemas.bookings import BookingAdd


async def test_add_booking(db):
    user = (await db.auth.get_all())[0]
    room = (await db.rooms.get_all())[0]
    booking_data = BookingAdd(
        user_id=user.id,
        room_id=room.id,
        date_from=date.today()+timedelta(days=1),
        date_to=date.today()+timedelta(days=10),
        price=room.discounted_price
    )
    
    await db.bookings.add(booking_data)
    await db.commit()
