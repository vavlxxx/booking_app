"""added additionals and many-to-many rooms_with_additionals

Revision ID: d876bc95ec32
Revises: e11758781b0f
Create Date: 2025-06-18 12:16:00.449133

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d876bc95ec32"
down_revision: Union[str, None] = "e11758781b0f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "additionals",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "room_additionals",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("additional_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["additional_id"],
            ["additionals.id"],
        ),
        sa.ForeignKeyConstraint(
            ["room_id"],
            ["rooms.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("room_additionals")
    op.drop_table("additionals")
