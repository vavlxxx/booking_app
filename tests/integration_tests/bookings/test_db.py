from datetime import date, timedelta

from src.schemas.bookings import BookingAdd


async def test_booking_crud(db):
    user = (await db.auth.get_all())[0]
    room = (await db.rooms.get_all())[0]
    booking_data = BookingAdd(
        user_id=user.id,
        room_id=room.id,
        date_from=date.today() + timedelta(days=1),
        date_to=date.today() + timedelta(days=10),
        price=room.discounted_price,
    )

    booking = await db.bookings.add(booking_data)
    assert booking

    booking = await db.bookings.get_one_or_none(id=booking.id)
    assert booking
    assert booking.room_id == room.id
    assert booking.date_from == date.today() + timedelta(days=1)
    assert booking.date_to == date.today() + timedelta(days=10)
    assert booking.price == room.discounted_price

    booking.price = 0
    await db.bookings.edit(booking, id=booking.id)
    booking = await db.bookings.get_one_or_none(id=booking.id)
    assert booking.price == 0

    await db.bookings.delete(id=booking.id)
    booking = await db.bookings.get_one_or_none(id=booking.id)
    assert booking is None

    await db.rollback()
