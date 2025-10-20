"""Add default value to updated_at

Revision ID: 462fed58501a
Revises: d8dbc93c10c5
Create Date: 2025-10-20 21:12:09.314387

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '462fed58501a'
down_revision: Union[str, None] = 'd8dbc93c10c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
