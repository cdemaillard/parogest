from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
from app.exceptions import InvalidSiretException
from app.validators import validate_siret

# Schema de base (champs communs)

class SupplierBase(BaseModel):
  name: str = Field(..., min_length=1, max_length=200)
  email: Optional[EmailStr] = None
  phone: Optional[str] = Field(None, max_length=20)
  adress: Optional[str] = None
  siret: Optional[str] = Field(None, min_length=14, max_length=14)
  
  @field_validator('siret')
  @classmethod
  def validate_siret_format(cls, v):
    if v and not validate_siret(v):
      raise ValueError('Invalide SIRET number. Must be 14 digits and pass Luhn algorithm')
    return v
  
# Schema pour la création
class SupplierCreate(SupplierBase):
  pass

# Schema pour la modification

class SupplierUpdate(BaseModel):
  name: Optional[str] = Field(None, min_length=1, max_length=200)
  email: Optional[EmailStr] = None
  phone: Optional[str] = Field(None, max_length=20)
  adress: Optional[str] = None
  siret: Optional[str] = Field(None, max_length=14)
  
  @field_validator('siret')
  @classmethod
  def validate_siret_format(cls, v):
    if v and not validate_siret(v):
      raise ValueError('Invalide SIRET number. Must be 14 digits and pass Luhn algorithm')
    return v

# Schema pour la réponse
class SupplierResponse(BaseModel):
  id: int
  name: str
  email: Optional[str] = None
  phone: Optional[str] = None
  adress: Optional[str] = None
  siret: Optional[str] = None
  created_at: datetime
  updated_at: datetime
  
  class Config:
    from_attributes = True