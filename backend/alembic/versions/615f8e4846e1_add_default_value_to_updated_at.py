"""Add default value to updated_at

Revision ID: 615f8e4846e1
Revises: 462fed58501a
Create Date: 2025-10-20 21:12:50.880298

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '615f8e4846e1'
down_revision: Union[str, None] = '462fed58501a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
