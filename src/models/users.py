from datetime import date

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Computed, String, Date, CheckConstraint, func

from src.db import Base


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(192))
    hashed_password: Mapped[str] = mapped_column(String(256))

    last_name: Mapped[str] = mapped_column(String(128))
    first_name: Mapped[str] = mapped_column(String(128))
    birthday: Mapped[date] = mapped_column(Date())
    gender: Mapped[str] = mapped_column(String(7))

    __table_args__ = (
        CheckConstraint("birthday <= CURRENT_DATE", name="check_birthday_validity"),
        CheckConstraint("gender IN ('M', 'F')", name="check_gender_validity"),
    )
