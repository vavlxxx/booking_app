"""added extra fields

Revision ID: a0b02917e75f
Revises: 0514c8fa3815
Create Date: 2025-06-14 18:18:43.059700

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a0b02917e75f"
down_revision: Union[str, None] = "0514c8fa3815"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("hotels", sa.Column("description", sa.String(), nullable=True))
    op.add_column("rooms", sa.Column("discount", sa.Integer(), nullable=True))
    op.add_column(
        "rooms",
        sa.Column(
            "discounted_price",
            sa.Float(),
            sa.Computed(
                "price * (100 - discount) / 100",
            ),
            nullable=False,
        ),
    )
    op.add_column(
        "users", sa.Column("last_name", sa.String(length=128), nullable=False)
    )
    op.add_column(
        "users", sa.Column("first_name", sa.String(length=128), nullable=False)
    )
    op.add_column("users", sa.Column("birthday", sa.Date(), nullable=False))
    op.add_column("users", sa.Column("gender", sa.String(), nullable=False))

    op.create_unique_constraint("email_uniqueness", "users", ("email",))

    op.create_check_constraint(
        "check_discount_range", "rooms", "discount >= 0 AND discount <= 100"
    )
    op.create_check_constraint("check_price_positive", "rooms", "price >= 0")
    op.create_check_constraint(
        "check_birthday_validity", "users", "birthday <= CURRENT_DATE"
    )
    op.create_check_constraint("check_gender_validity", "users", "gender IN ('М', 'Ж')")


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
    op.drop_constraint("check_gender_validity", "users", type_="check")
    op.drop_constraint("check_birthday_validity", "users", type_="check")
    op.drop_constraint("check_price_positive", "rooms", type_="check")
    op.drop_constraint("check_discount_range", "rooms", type_="check")

    op.drop_column("users", "gender")
    op.drop_column("users", "birthday")
    op.drop_column("users", "first_name")
    op.drop_column("users", "last_name")
    op.drop_column("rooms", "discounted_price")
    op.drop_column("rooms", "discount")
    op.drop_column("hotels", "description")
