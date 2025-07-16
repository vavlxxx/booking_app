from datetime import date

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, CheckConstraint

from src.db import Base


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(192), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(256))

    last_name: Mapped[str | None] = mapped_column(String(128))
    first_name: Mapped[str | None] = mapped_column(String(128))
    birthday: Mapped[date | None]
    gender: Mapped[str | None]

    __table_args__ = (
        CheckConstraint("birthday <= CURRENT_DATE", name="check_birthday_validity"),
        CheckConstraint("gender IN ('М', 'Ж')", name="check_gender_validity"),
    )
