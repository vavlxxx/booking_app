"""added created_at field to BookingsOrm model

Revision ID: e11758781b0f
Revises: 9c3368557339
Create Date: 2025-06-17 16:30:55.230318

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e11758781b0f"
down_revision: Union[str, None] = "9c3368557339"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "bookings",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("bookings", "created_at")
