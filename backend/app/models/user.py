from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum as SQLEnum
from sqlalchemy.sql import func
from app.database import Base
from app.enums import UserRole

class User(Base):
  """
    Modèle pour les utilisateurs de ParoGest.
    Gère les prêtres, bénévoles, trésoriers et administrateurs.
  """
  __tablename__ = "users"
  
  id = Column(Integer, primary_key=True, index=True)
  email = Column(String(255), unique=True, nullable=False, index=True)
  hashed_password = Column(String(255), nullable=False)
  #Info perso
  first_name = Column(String(255), nullable=False)
  last_name = Column(String(255), nullable=False)
  phone = Column(String(255), nullable=True)
  
  role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.VOLUNTEER)
  
  is_active = Column(Boolean, nullable=False, default=True)
  
  created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
  updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

  def __repr__(self):
    """
      Représentation du modèle (pour le débogage)
    """
    return f"<User(id={self.id}, email='{self.email}', role={self.role})>"
  
  @property
  def full_name(self):
    """Retourne le nom complet de l'utilisateur"""
    return f"{self.first_name} {self.last_name}"