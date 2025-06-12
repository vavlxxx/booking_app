from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from src.db import Base


class RoomsOrm(Base):
    __tablename__ = "rooms"

    id_: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id_"))
    title: Mapped[str]
    description: Mapped[Optional[str]]
    price: Mapped[int]
    quantity: Mapped[int]
