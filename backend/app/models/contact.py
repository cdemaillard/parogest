from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Date, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base
from app.enums import ContactType

class Contact(Base):
  """
  Modèle unifié pour tous les types de contacts (tiers).
  
  Peut représenter :
  - Un fournisseur (SUPPLIER)
  - Un donateur (DONOR)
  - Un bénévole (VOLUNTEER)
  - Un prêtre (PRIEST)
  - Le diocèse (DIOCESE)
  - Autre (OTHER)
  """
  __tablename__ = "contacts"
  
  # === Identifiant ===
  id = Column(Integer, primary_key=True, index=True)
  
  # === Type de contact (OBLIGATOIRE)
  contact_type = Column(SQLEnum(ContactType), nullable=False, index=True)
  
  # == Informations de base ===
  is_company = Column(Boolean, default=False, nullable=False)
  name = Column(String(200), nullable=False, index=True)
  display_name = Column(String(200), nullable=True)
  
  # === Coordonnées ===
  email = Column(String(250), unique=True, nullable=True, index=True)
  phone = Column(String(20), nullable=True)
  mobile = Column(String(20), nullable=True)
  
  # === Adresse postale ===
  street = Column(String(255), nullable=True)
  street2 = Column(String(255), nullable=True)
  zip_code = Column(String(10), nullable=True)
  city = Column(String(100), nullable=True, index=True)
  country = Column(String(100), default="France", nullable=False)
  
  # === Informations légale (fournisseur) ===
  siret = Column(String(14), nullable=True, index=True)
  vat_number = Column(String(50), nullable=True)
  
  # === Informations spécifiques (Donateur) ===
  is_donor = Column(Boolean, default=False, nullable=False)
  anonymize_donation = Column(Boolean, default=False, nullable=False)
  
  # === Informations spécifiques (Prêtre) ===
  ministry_role = Column(String(100), nullable=True)
  ordination_date = Column(Date, nullable=True)
  
  # === Informations spécifiques (Bénévole) ===
  volunteer_skills = Column(JSON, nullable=True)
  
  # === Coordonnées bancaires ===
  bank_name = Column(String(100), nullable=True)
  iban = Column(String(34), nullable=True)
  bic = Column(String(11), nullable=True)
  
  # === Gestion ===
  active = Column(Boolean, default=True, nullable=False, index=True)
  notes = Column(Text, nullable=True)
  
  # Timestaps automatiques
  created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
  updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
  
  def __repr__(self):
    """
    Représentation du modèle (pour le débug)
    """
    return f"<Contact(id={self.id}, name='{self.name}')>"