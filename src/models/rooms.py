from typing import Optional

import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import CheckConstraint, Computed, ForeignKey

from src.db import Base

if typing.TYPE_CHECKING:
    from src.models.additionals import AdditionalsOrm


class RoomsOrm(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    title: Mapped[str]
    description: Mapped[Optional[str]]
    quantity: Mapped[int]

    price: Mapped[float]
    discount: Mapped[Optional[int]] = mapped_column(default=0)
    discounted_price: Mapped[float] = mapped_column(Computed("price * (100 - discount) / 100"))

    additionals: Mapped[list["AdditionalsOrm"]] = relationship(
        secondary="room_additionals",
        back_populates="rooms",
    )

    __table_args__ = (
        CheckConstraint("discount >= 0 AND discount <= 100", name="check_discount_range"),
        CheckConstraint("price >= 0", name="check_price_positive"),
    )
    