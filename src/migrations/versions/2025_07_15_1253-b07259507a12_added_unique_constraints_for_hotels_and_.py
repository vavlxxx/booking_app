"""added unique constraints for hotels and rooms

Revision ID: b07259507a12
Revises: 5176364dea3c
Create Date: 2025-07-15 12:53:58.750563

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "b07259507a12"
down_revision: Union[str, None] = "5176364dea3c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint("hotels_title_key", "hotels", ["title"])
    op.create_unique_constraint("rooms_title_hotel_key", "rooms", ["title", "hotel_id"])
    op.create_check_constraint("check_quantity_is_ge_one", "rooms", "quantity >= 1")


def downgrade() -> None:
    op.drop_constraint("rooms_title_hotel_key", "rooms", type_="unique")
    op.drop_constraint("hotels_title_key", "hotels", type_="unique")
    op.drop_constraint("check_quantity_is_ge_one", "rooms", type_="check")
