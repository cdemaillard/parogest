from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# Schema de base (champs communs)

class SupplierBase(BaseModel):
  name: str = Field(..., min_length=1, max_length=200)
  email: Optional[EmailStr] = None
  phone: Optional[str] = Field(None, max_length=20)
  adress: Optional[str] = None
  siret: Optional[str] = Field(None, max_length=14)
  
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

# Schema pour la réponse
class SupplierResponse(SupplierBase):
  id: int
  created_at: datetime
  updated_at: datetime
  
  class Config:
    from_attributes = True