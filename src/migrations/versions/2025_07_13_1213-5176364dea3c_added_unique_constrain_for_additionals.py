"""added unique constrain for additionals

Revision ID: 5176364dea3c
Revises: d233d034600a
Create Date: 2025-07-13 12:13:22.968024

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "5176364dea3c"
down_revision: Union[str, None] = "d233d034600a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "additionals", ["name"])


def downgrade() -> None:
    op.drop_constraint(None, "additionals", type_="unique")
