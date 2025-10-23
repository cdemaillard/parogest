from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, Dict, Any
from datetime import datetime, date
from app.exceptions import InvalidSiretException
from app.validators import validate_siret
from app.enums import ContactType

# === Schéma de base (champs communs) ===

class ContactBase(BaseModel):
  """
  Schéma de base pour un contact.
  Contient les champs communs à tous les types de contacts.
  """
  contact_type: ContactType
  is_company: bool = True
  name: str = Field(..., min_length=1, max_length=200, description="Nom complet du contact")
  display_name: Optional[str] = Field(None, max_length=200, description="Nom d'affichage (ex: 'Abbé Martin')")
  
  
  # Coordonnées
  email: Optional[EmailStr] = Field(None, description="Email du contact")
  phone: Optional[str] = Field(None, max_length=20, description="Téléphone fixe")
  mobile: Optional[str] = Field(None, max_length=20, description="Téléphone mobile")
  
  # Adresse postale
  street: Optional[str] = Field(None, max_length=255, description="Rue (ligne 1)")
  street2: Optional[str] = Field(None, max_length=255, description="Complément d'adresse (ligne 2)")
  zip_code: Optional[str] = Field(None, max_length=10, description="Code postal")
  city: Optional[str] = Field(None, max_length=100, description="Ville")
  country: str = Field(default="France", max_length=100, description="Pays")
  
   # Informations légales (fournisseurs)
  siret: Optional[str] = Field(None, min_length=14, max_length=14, description="Numéro SIRET (14 chiffres)")
  vat_number: Optional[str] = Field(None, max_length=50, description="Numéro TVA intracommunautaire")
  
   # Informations spécifiques DONATEUR
  is_donor: bool = Field(default=False, description="Est un donateur régulier")
  anonymize_donation: bool = Field(default=False, description="Anonymiser les dons")
  
  # Informations spécifiques PRÊTRE
  ministry_role: Optional[str] = Field(None, max_length=100, description="Fonction ecclésiastique (Curé, Vicaire, Diacre)")
  ordination_date: Optional[date] = Field(None, description="Date d'ordination")
  
  # Informations spécifiques BÉNÉVOLE
  volunteer_skills: Optional[Dict[str, Any]] = Field(None, description="Compétences bénévole (JSON)")
  
  # Coordonnées bancaires (pour remboursements)
  bank_name: Optional[str] = Field(None, max_length=100, description="Nom de la banque")
  iban: Optional[str] = Field(None, max_length=34, description="IBAN (max 34 caractères)")
  bic: Optional[str] = Field(None, max_length=11, description="BIC/SWIFT (8 ou 11 caractères)")
  
  # Gestion
  active: bool = Field(default=True, description="Contact actif/archivé")
  notes: Optional[str] = Field(None, description="Remarques libres")
  
  @field_validator('siret')
  @classmethod
  def validate_siret_format(cls, v):
    if v and not validate_siret(v):
      raise ValueError('Invalide SIRET number. Must be 14 digits and pass Luhn algorithm')
    return v
  
# Schema pour la création
class ContactCreate(ContactBase):
  """
  Schéma pour créer un nouveau contact.
  Hérite de ContactBase avec tous les champs.
  """
  pass

# Schema pour la modification

class ContactUpdate(BaseModel):
  """
  Schéma pour modifier un contact existant.
  Tous les champs sont optionnels.
  """
  contact_type: Optional[ContactType] = None
  is_company: Optional[bool] = None
  name: Optional[str] = Field(None, min_length=1, max_length=200)
  display_name: Optional[str] = Field(None, max_length=200)
  
  # Coordonnées
  email: Optional[EmailStr] = None
  phone: Optional[str] = Field(None, max_length=20)
  mobile: Optional[str] = Field(None, max_length=20)
  
  # Adresse postale
  street: Optional[str] = Field(None, max_length=255)
  street2: Optional[str] = Field(None, max_length=255)
  zip_code: Optional[str] = Field(None, max_length=10)
  city: Optional[str] = Field(None, max_length=100)
  country: Optional[str] = Field(None, max_length=100)
  
  # Informations légales
  siret: Optional[str] = Field(None, min_length=14, max_length=14)
  vat_number: Optional[str] = Field(None, max_length=50)
  
  # Informations spécifiques DONATEUR
  is_donor: Optional[bool] = None
  anonymize_donation: Optional[bool] = None
  
  # Informations spécifiques PRÊTRE
  ministry_role: Optional[str] = Field(None, max_length=100)
  ordination_date: Optional[date] = None
  
  # Informations spécifiques BÉNÉVOLE
  volunteer_skills: Optional[Dict[str, Any]] = None
  
  # Coordonnées bancaires
  bank_name: Optional[str] = Field(None, max_length=100)
  iban: Optional[str] = Field(None, max_length=34)
  bic: Optional[str] = Field(None, max_length=11)
  
  # Gestion
  active: Optional[bool] = None
  notes: Optional[str] = None
  
  @field_validator('siret')
  @classmethod
  def validate_siret_format(cls, v):
    if v and not validate_siret(v):
      raise ValueError('Invalide SIRET number. Must be 14 digits and pass Luhn algorithm')
    return v

# === Schéma pour la réponse ===
class ContactResponse(BaseModel):
  """
  Schéma pour la réponse API.
  Contient tous les champs y compris les timestamps.
  """
  id: int
  contact_type: ContactType
  is_company: bool
  name: str
  display_name: Optional[str] = None
  
  # Coordonnées
  email: Optional[str] = None
  phone: Optional[str] = None
  mobile: Optional[str] = None
  
  # Adresse postale
  street: Optional[str] = None
  street2: Optional[str] = None
  zip_code: Optional[str] = None
  city: Optional[str] = None
  country: str
  
  # Informations légales
  siret: Optional[str] = None
  vat_number: Optional[str] = None
  
  # Informations spécifiques DONATEUR
  is_donor: bool
  anonymize_donation: bool
  
  # Informations spécifiques PRÊTRE
  ministry_role: Optional[str] = None
  ordination_date: Optional[date] = None
  
  # Informations spécifiques BÉNÉVOLE
  volunteer_skills: Optional[Dict[str, Any]] = None
  
  # Coordonnées bancaires
  bank_name: Optional[str] = None
  iban: Optional[str] = None
  bic: Optional[str] = None
  
  # Gestion
  active: bool
  notes: Optional[str] = None
  
  # Timestamps
  created_at: datetime
  updated_at: datetime
  
  class Config:
      from_attributes = True