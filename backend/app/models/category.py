from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base

class Category(Base):
  """
  Modèle pour les catégories de dépenses.
  Permet de classifier les dépenses sur le Plan Comptable Général.
  """
  
  __tablename__ = "categories"
  
  # Colonne ID (clé primaire, auto-incrémenté)
  id = Column(Integer, primary_key=True, index=True)
  
  # Nom de la catégorie (obligatoire)
  name = Column(String(100), nullable=False, unique=True, index=True)
  
  # Code comptable PCG (optionnel)
  code = Column(String(10), nullable=True, unique=True, index=True)
  
  # Description (optionnelle)
  description = Column(Text, nullable=True)
  
  # Activation
  is_active = Column(Boolean, default=True, nullable=False)
  
  # Timestaps automatiquesoui
  created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
  updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

def __repr__(self):
  """
  Représentation du modèle pour le débogage
  """
  return f"<Category(id={self.id}, name='{self.name}', code='{self.code}')>"