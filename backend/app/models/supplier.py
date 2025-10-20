from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Supplier(Base):
  """
  Modèle pour les fournisseur.
  Un fournisseur est une entreprise ou personne qui vend des biens/services
  """
  __tablename__ = "suppliers"
  
  # Colonne ID (clé primaire, auto-incrémenté)
  id = Column(Integer, primary_key=True, index=True)
  
  # Nom du fournisseur (obligatoire)
  name = Column(String(200), nullable=False, index=True)
  
  # Informations de contact
  email = Column(String(250), unique=True, nullable=True)
  phone = Column(String(20), nullable=True)
  
  # Adresse
  adress = Column(Text, nullable=True)
  
  # Timestaps automatiques
  created_at = Column(DateTime(timezone=True), server_default=func.now())
  updated_at = Column(DateTime(timezone=True), onupdate=func.now())
  
  def __repr__(self):
    """
    Représentation du modèle (pour le débug)
    """
    return f"<Supplier(id={self.id}, name='{self.name}')>"