"""added desc to Additionals

Revision ID: d233d034600a
Revises: d876bc95ec32
Create Date: 2025-06-18 12:30:44.729550

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d233d034600a"
down_revision: Union[str, None] = "d876bc95ec32"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("additionals", sa.Column("description", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("additionals", "description")
