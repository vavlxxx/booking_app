from datetime import date
from sqlalchemy import func, select

from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm


def rooms_data_to_booking(
        date_from: date, 
        date_to: date, 
        hotel_id: int | None = None
):
        
    rooms_count = (
        select(BookingsOrm.room_id, func.count(BookingsOrm.room_id).label("booked_rooms"))
        .select_from(BookingsOrm)
        .filter(
            BookingsOrm.date_from <= date_to, 
            BookingsOrm.date_to >= date_from
        )
        .group_by(BookingsOrm.room_id)
        .cte(name="rooms_count")
    )

    rooms_left = (
        select(
            RoomsOrm.id, 
            RoomsOrm.hotel_id,
            RoomsOrm.title,
            RoomsOrm.description,
            RoomsOrm.price,
            RoomsOrm.quantity,
            (RoomsOrm.quantity - func.coalesce(rooms_count.c.booked_rooms, 0)).label("empty"),
            RoomsOrm.discount,
            RoomsOrm.discounted_price,
        )
        .select_from(RoomsOrm)
        .outerjoin(rooms_count, RoomsOrm.id == rooms_count.c.room_id)
        .cte(name="rooms_left")
    )

    rooms_ids_by_hotel = (
        select(RoomsOrm.id)
        .select_from(RoomsOrm)
    )

    if hotel_id is not None:
        rooms_ids_by_hotel = (
            rooms_ids_by_hotel
            .filter_by(hotel_id=hotel_id)
        )

    rooms_ids_by_hotel = (
        rooms_ids_by_hotel
        .subquery(name="rooms_ids_by_hotel")
    )

    empty_rooms_data_to_get = (
        select(rooms_left)
        .select_from(rooms_left)
        .filter(
            rooms_left.c.empty > 0,
            (rooms_left.c.id).in_(select(rooms_ids_by_hotel))
        )
    )

    return empty_rooms_data_to_get
