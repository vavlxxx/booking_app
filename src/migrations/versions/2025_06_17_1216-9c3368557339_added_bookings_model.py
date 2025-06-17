"""added bookings model

Revision ID: 9c3368557339
Revises: a0b02917e75f
Create Date: 2025-06-17 12:16:18.064834

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9c3368557339"
down_revision: Union[str, None] = "a0b02917e75f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "bookings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("date_from", sa.Date(), nullable=False),
        sa.Column("date_to", sa.Date(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column(
            "total_price",
            sa.Float(),
            sa.Computed(
                "price * (date_to - date_from)",
            ),
            nullable=False,
        ),
        sa.CheckConstraint(
            "CURRENT_DATE < date_from AND CURRENT_DATE < date_to",
            name="check_date_future",
        ),
        sa.CheckConstraint("date_from < date_to", name="check_date_validity"),
        sa.CheckConstraint("price >= 0", name="check_price_positive"),
        sa.ForeignKeyConstraint(
            ["room_id"],
            ["rooms.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("bookings")
