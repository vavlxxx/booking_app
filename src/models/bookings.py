from datetime import date

from sqlalchemy import CheckConstraint, ForeignKey, Computed
# from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import mapped_column, Mapped

from src.db import Base


class BookingsOrm(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    date_from: Mapped[date]
    date_to: Mapped[date]
    price: Mapped[float]
    total_price: Mapped[float] = mapped_column(Computed("price * (date_to - date_from)"))

    __table_args__ = (
        CheckConstraint("date_from < date_to", name="check_date_validity"),
        CheckConstraint("price >= 0", name="check_price_positive"),
        CheckConstraint("CURRENT_DATE < date_from AND CURRENT_DATE < date_to", name="check_date_future"),
    )

    # @hybrid_property
    # def total_cost(self) -> float:
    #     return self.price * (self.date_to - self.date_from).days
