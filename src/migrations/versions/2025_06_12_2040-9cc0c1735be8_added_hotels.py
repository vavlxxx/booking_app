"""added hotels

Revision ID: 9cc0c1735be8
Revises:
Create Date: 2025-06-12 20:40:40.409744

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "9cc0c1735be8"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "hotels",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("location", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("hotels")
