from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.enums import UserRole

# Schema de base
class UserBase(BaseModel):
  email: EmailStr = Field(..., description="Email de l'utilisateur")
  first_name: str = Field(..., min_length=1, max_length=100, description="Prénom")
  last_name: str = Field(..., min_length=1, max_length=100, description="Nom de famille")
  phone: Optional[str] = Field(None, max_length=20, description="Numéro de téléphone")
  role: UserRole = Field(default=UserRole.VOLUNTEER, description="Rôle de l'utilisateur")
  is_active: bool = Field(default=True, description="Statut d'activation du compte")
  
# Schema pour la création
class UserCreate(UserBase):
  password: str = Field(..., min_length=8, description="Mot de passe (min 8 caractères)")
  # Note : on reçoit le password en clair, mais il sera hasher avant l'enregistrement

# Sechma pour la modification
class UserUpdate(BaseModel):
  email: Optional[EmailStr] = None
  first_name: Optional[str] = Field(None, min_length=1, max_length=100)
  last_name: Optional[str] = Field(None, min_length=1, max_length=100)
  phone: Optional[str] = Field(None, max_length=20)
  role: Optional[UserRole] = None
  is_active: Optional[bool] = None
  password: Optional[str] = Field(default=None, min_length=8, description="Nouveau mot de passe (min 8 caractères) (optionnel)")

# Schema pour la réponse (SANS le mot de passe !)
class UserResponse(BaseModel):
  id: int
  email: str
  first_name: str
  last_name: str
  phone: Optional[str] = None
  role: UserRole
  is_active: bool
  created_at: datetime
  updated_at: datetime
  
  class Config:
    from_attributes = True
  
  @property
  def full_name(self) -> str:
    """Retourne le nom complet"""
    return f"{self.first_name} {self.last_name}"