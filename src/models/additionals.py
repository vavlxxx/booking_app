import typing

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.db import Base

if typing.TYPE_CHECKING:
    from src.models.rooms import RoomsOrm


class AdditionalsOrm(Base):
    __tablename__ = "additionals"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column(nullable=True)

    rooms: Mapped[list["RoomsOrm"]] = relationship( # type: ignore
        secondary="room_additionals",
        back_populates="additionals",
    )


class RoomsAdditionalsOrm(Base):
    __tablename__ = "room_additionals"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    additional_id: Mapped[int] = mapped_column(ForeignKey("additionals.id"))
