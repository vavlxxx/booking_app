"""added users

Revision ID: 0514c8fa3815
Revises: bb5818568d87
Create Date: 2025-06-14 11:38:41.319152

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0514c8fa3815"
down_revision: Union[str, None] = "bb5818568d87"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=192), nullable=False),
        sa.Column("hashed_password", sa.String(length=256), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("users")
