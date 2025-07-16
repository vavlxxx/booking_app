"""make user fields optional

Revision ID: cc5ac0bc9202
Revises: b07259507a12
Create Date: 2025-07-15 15:02:10.646961

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cc5ac0bc9202"
down_revision: Union[str, None] = "b07259507a12"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("users", "last_name", existing_type=sa.VARCHAR(length=128), nullable=True)
    op.alter_column("users", "first_name", existing_type=sa.VARCHAR(length=128), nullable=True)
    op.alter_column("users", "birthday", existing_type=sa.DATE(), nullable=True)
    op.alter_column("users", "gender", existing_type=sa.VARCHAR(), nullable=True)


def downgrade() -> None:
    op.alter_column("users", "gender", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("users", "birthday", existing_type=sa.DATE(), nullable=False)
    op.alter_column("users", "first_name", existing_type=sa.VARCHAR(length=128), nullable=False)
    op.alter_column("users", "last_name", existing_type=sa.VARCHAR(length=128), nullable=False)
