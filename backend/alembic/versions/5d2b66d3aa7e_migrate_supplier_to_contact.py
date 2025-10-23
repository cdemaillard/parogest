"""migrate_supplier_to_contact

Revision ID: 5d2b66d3aa7e
Revises: 547e783575ac
Create Date: 2025-10-23 18:28:07.538346

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '5d2b66d3aa7e'
down_revision: Union[str, None] = '547e783575ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Migrer le modèle Supplier vers Contact unifié.
    
    Étapes :
    1. Renommer la table suppliers → contacts
    2. Créer l'enum ContactType
    3. Ajouter toutes les nouvelles colonnes
    4. Migrer les données existantes (tous les suppliers → contact_type='supplier')
    5. Rendre contact_type NOT NULL
    """
    
    # 1. Renommer la table
    op.rename_table('suppliers', 'contacts')
    
    # 2. Créer l'enum ContactType
    contact_type_enum = postgresql.ENUM(
        'supplier', 'donor', 'volunteer', 'priest', 'diocese', 'other',
        name='contacttype',
        create_type=True
    )
    contact_type_enum.create(op.get_bind())
    
    # 3. Ajouter la colonne contact_type (nullable temporairement)
    op.add_column('contacts', sa.Column('contact_type', sa.Enum('supplier', 'donor', 'volunteer', 'priest', 'diocese', 'other', name='contacttype'), nullable=True))
    
    # 4. Migrer les données : tous les suppliers existants deviennent des contacts de type SUPPLIER
    op.execute("UPDATE contacts SET contact_type = 'supplier' WHERE contact_type IS NULL")
    
    # 5. Rendre contact_type NOT NULL maintenant que toutes les données sont migrées
    op.alter_column('contacts', 'contact_type', nullable=False)
    
    # 6. Ajouter index sur contact_type
    op.create_index(op.f('ix_contacts_contact_type'), 'contacts', ['contact_type'], unique=False)
    
    # 7. Ajouter toutes les nouvelles colonnes
    
    # Informations de base
    op.add_column('contacts', sa.Column('is_company', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('contacts', sa.Column('display_name', sa.String(length=200), nullable=True))
    
    # Coordonnées (mobile n'existait pas)
    op.add_column('contacts', sa.Column('mobile', sa.String(length=20), nullable=True))
    
    # Adresse postale détaillée (remplace l'ancien champ 'adress')
    op.add_column('contacts', sa.Column('street', sa.String(length=255), nullable=True))
    op.add_column('contacts', sa.Column('street2', sa.String(length=255), nullable=True))
    op.add_column('contacts', sa.Column('zip_code', sa.String(length=10), nullable=True))
    op.add_column('contacts', sa.Column('city', sa.String(length=100), nullable=True))
    op.add_column('contacts', sa.Column('country', sa.String(length=100), nullable=False, server_default='France'))
    
    # Index sur city
    op.create_index(op.f('ix_contacts_city'), 'contacts', ['city'], unique=False)
    
    # Informations légales
    op.add_column('contacts', sa.Column('vat_number', sa.String(length=50), nullable=True))
    
    # Ajouter index sur siret (s'il n'existe pas déjà)
    op.create_index(op.f('ix_contacts_siret'), 'contacts', ['siret'], unique=False)
    
    # Informations spécifiques DONATEUR
    op.add_column('contacts', sa.Column('is_donor', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('contacts', sa.Column('anonymize_donation', sa.Boolean(), nullable=False, server_default='false'))
    
    # Informations spécifiques PRÊTRE
    op.add_column('contacts', sa.Column('ministry_role', sa.String(length=100), nullable=True))
    op.add_column('contacts', sa.Column('ordination_date', sa.Date(), nullable=True))
    
    # Informations spécifiques BÉNÉVOLE
    op.add_column('contacts', sa.Column('volunteer_skills', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    
    # Coordonnées bancaires
    op.add_column('contacts', sa.Column('bank_name', sa.String(length=100), nullable=True))
    op.add_column('contacts', sa.Column('iban', sa.String(length=34), nullable=True))
    op.add_column('contacts', sa.Column('bic', sa.String(length=11), nullable=True))
    
    # Gestion
    op.add_column('contacts', sa.Column('active', sa.Boolean(), nullable=False, server_default='true'))
    op.add_column('contacts', sa.Column('notes', sa.Text(), nullable=True))
    
    # Index sur active
    op.create_index(op.f('ix_contacts_active'), 'contacts', ['active'], unique=False)
    
    # Ajouter index sur email (s'il n'existe pas déjà)
    op.create_index(op.f('ix_contacts_email'), 'contacts', ['email'], unique=False)
    
    # Renommer la contrainte unique sur email
    op.execute("ALTER TABLE contacts RENAME CONSTRAINT suppliers_email_key TO contacts_email_key")


def downgrade() -> None:
    """
    Revenir en arrière : contacts → suppliers.
    
    ATTENTION : Cette opération supprimera tous les contacts qui ne sont pas de type SUPPLIER.
    """
    
    # 1. Supprimer tous les contacts qui ne sont pas des suppliers
    op.execute("DELETE FROM contacts WHERE contact_type != 'supplier'")
    
    # 2. Supprimer les index ajoutés
    op.drop_index(op.f('ix_contacts_active'), table_name='contacts')
    op.drop_index(op.f('ix_contacts_city'), table_name='contacts')
    op.drop_index(op.f('ix_contacts_contact_type'), table_name='contacts')
    op.drop_index(op.f('ix_contacts_email'), table_name='contacts')
    op.drop_index(op.f('ix_contacts_siret'), table_name='contacts')
    
    # 3. Supprimer les colonnes ajoutées
    op.drop_column('contacts', 'notes')
    op.drop_column('contacts', 'active')
    op.drop_column('contacts', 'bic')
    op.drop_column('contacts', 'iban')
    op.drop_column('contacts', 'bank_name')
    op.drop_column('contacts', 'volunteer_skills')
    op.drop_column('contacts', 'ordination_date')
    op.drop_column('contacts', 'ministry_role')
    op.drop_column('contacts', 'anonymize_donation')
    op.drop_column('contacts', 'is_donor')
    op.drop_column('contacts', 'vat_number')
    op.drop_column('contacts', 'country')
    op.drop_column('contacts', 'city')
    op.drop_column('contacts', 'zip_code')
    op.drop_column('contacts', 'street2')
    op.drop_column('contacts', 'street')
    op.drop_column('contacts', 'mobile')
    op.drop_column('contacts', 'display_name')
    op.drop_column('contacts', 'is_company')
    op.drop_column('contacts', 'contact_type')
    
    # 4. Supprimer l'enum
    sa.Enum(name='contacttype').drop(op.get_bind(), checkfirst=True)
    
    # 5. Renommer la contrainte email
    op.execute("ALTER TABLE contacts RENAME CONSTRAINT contacts_email_key TO suppliers_email_key")
    
    # 6. Renommer la table
    op.rename_table('contacts', 'suppliers')