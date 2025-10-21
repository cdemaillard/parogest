from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date, datetime
from decimal import Decimal
from app.enums import ExpenseStatus

#Schema de base
class ExpenseBase(BaseModel):
  amount: Decimal = Field(..., gt=0, description="Montant en euros (ex: 19.99)")
  description: str = Field(..., min_length=1, max_length=500, description="Description de la dépense")
  expense_date: date = Field(..., description="Date de la dépense")
  category_id: int = Field(..., gt=0, description="ID de la catégorie")
  supplier_id: int = Field(None, gt=0, description="ID du fournisseur (optionnel)" )
  
  @field_validator('amount')
  @classmethod
  def validate_amount(cls, v):
    """Valide que le montant a maximum 2 décimales"""
    if v.as_tuple().exponent < -2:
      raise ValueError('Amount must at most 2 decimal places')
    return v
  
# Schema pour la création
class ExpenseCreate(ExpenseBase):
  """
  Schema pour créer une dépense.
  Le user°id est automatiquement rempli par l'utilisateur connecté (cf : JWT)
  Le status par défaut est automatiquement PENDING.
  """
  pass

#Schema pour la modification
class ExpenseUpdate(BaseModel):
  amount: Optional[Decimal] = Field(None, gt=0)
  description: Optional[str] = Field(None, min_length=1, max_length=500)
  expense_date: Optional[date] = None
  category_id: Optional[int] = Field(None, gt=0)
  supplier_id: Optional[int] = Field(None, gt=0)
  status: Optional[ExpenseStatus] = None
  
  @field_validator('amount')
  @classmethod
  def validate_amount(cls, v):
    """Valide que le montant a maximum 2 décimales"""
    if v.as_tuple().exponent < -2:
      raise ValueError('Amount must at most 2 decimal places')
    return v

# Schema de réponse (avec infos complètes)
class ExpenseResponse(BaseModel):
  id: int
  amount: Decimal
  description: str
  expense_date: date
  status: ExpenseStatus
  
  # IDs des relations
  user_id: int
  category_id: int
  supplier_id: Optional[int] = None
  
  # Timestamps
  created_at: datetime
  updated_at: datetime
  
  class Config:
    from_attributes = True

# Schema pour la réponse détaillée (avec les noms des objets liés)
class ExpenseDetailResponse(ExpenseResponse):
  """
  Scehma enrichi avec les infos complètes des objets liés.
  Utilisé pour afficher une dépense avec tous les détails
  """
  # Information de l'utilisateur qui a soumis
  user_email: Optional[str] = None
  user_name: Optional[str] = None

  # Informations de la catégorie
  category_name: Optional[str] = None
  category_code: Optional[str] = None
  
  # Informations du fournisseur
  supplier_name: Optional[str] = None