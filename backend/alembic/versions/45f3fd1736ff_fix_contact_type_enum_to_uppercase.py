"""fix_contact_type_enum_to_uppercase

Revision ID: 45f3fd1736ff
Revises: 5d2b66d3aa7e
Create Date: 2025-10-23 23:00:52.052131

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '45f3fd1736ff'
down_revision: Union[str, None] = '5d2b66d3aa7e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Passer l'enum ContactType de minuscule à MAJUSCULES.
    Ceci suit la convention Python standard pour les noms d'enum.
    """
    
    op.execute("ALTER TYPE contacttype RENAME TO contacttype_old")
    
    op.execute("""
               CREATE TYPE contacttype AS ENUM (
                   'SUPPLIER', 'DONOR', 'VOLUNTEER', 'PRIEST', 'DIOCESE', 'OTHER'
               )
        """)
    
    op.execute("""
               ALTER TABLE contacts
               ALTER COLUMN contact_type TYPE contacttype
               USING UPPER(contact_type::text)::contacttype
               """)
    
    op.execute("DROP TYPE contacttype_old")


def downgrade() -> None:
    """
    Revenir aux minuscules (au cas où)
    """

    # 1. Renommer l'enum actuel
    op.execute("ALTER TYPE contacttype RENAME TO contacttype_old")

    # 2. Re-créer l'ancien enum en minuscules
    op.execute("""
        CREATE TYPE contacttype AS ENUM (
            'supplier', 'donor', 'volunteer', 'priest', 'diocese', 'other'
        )
    """)

    # 3. Convertir les données (MAJUSCULES → minuscules)
    op.execute("""
        ALTER TABLE contacts 
        ALTER COLUMN contact_type TYPE contacttype 
        USING LOWER(contact_type::text)::contacttype
    """)

    # 4. Supprimer l'ancien enum
    op.execute("DROP TYPE contacttype_old")
