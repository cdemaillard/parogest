"""Fix address typo

Revision ID: 0d097f6e8fef
Revises: ccab67ca40be
Create Date: 2025-10-20 19:55:27.192337

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d097f6e8fef'
down_revision: Union[str, None] = 'ccab67ca40be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Ajouter une valeur par défaut à updated_at
    op.execute("ALTER TABLE suppliers ALTER COLUMN updated_at SET DEFAULT now();")
    # Mettre à jour les lignes existantes avec NULL
    op.execute("UPDATE suppliers SET updated_at = now() WHERE updated_at IS NULL;")

def downgrade() -> None:
    op.execute("ALTER TABLE suppliers ALTER COLUMN updated_at DROP DEFAULT;")