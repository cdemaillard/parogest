from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime

# Schema de base (champs communs)
class CategoryBase(BaseModel):
  name: str = Field(..., min_length=1, max_length=100, description="Nom de la catégorie")
  code: Optional[str] = Field(None, max_length=10, description="Code comptable PCG")
  description: Optional[str] = Field(None, description="Description de la catégorie")
  is_active: bool = Field(True, description="Etat d'activation de la catégorie")
  
# Schema de création
class CategoryCreate(CategoryBase):
  pass

# Schema pour la modification
class CategoryUpdate(BaseModel):
  name: Optional[str] = Field(None, min_length=1, max_length=100)
  code: Optional[str] = Field(None, max_length=10)
  description: Optional[str] = None
  is_active: Optional[bool] = None

# Schema pour la réponse
class CategoryResponse(BaseModel):
  id: int
  name: str
  code: Optional[str] = None
  description: Optional[str] = None
  is_active: bool
  created_at: datetime
  updated_at: datetime
  
  class Config:
    from_attributes = True