from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, DECIMAL, Date, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from decimal import Decimal
from app.database import Base
from app.enums import ExpenseStatus

class Expense(Base):
  """
  Modèle pour les dépenses.
  Une dépense représente un achat ou un remboursement de frais.
  """

  __tablename__ = "expenses"
  
  #Colone ID (clé primaire, auto-incrémentée)
  id = Column(Integer, primary_key=True, index=True)
  amount = Column(DECIMAL(10,2), nullable=False)
  description = Column(Text, nullable=False)
  expense_date = Column(Date, nullable=False, index=True)
  status = Column(
    SQLEnum(ExpenseStatus),
    nullable=False,
    default=(ExpenseStatus.DRAFT),
    index=True
  )
  # Relation (Foreign Keys)
  # Utilisateur qui a soumis la démense
  user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
  category_id = Column(Integer, ForeignKey('categories.id'), nullable=False, index=True)
  supplier_id = Column(Integer, ForeignKey('suppliers.id'), nullable=True, index=True)
  
  # Timestamps
  created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
  updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
  
  # Relation ORM (pour accéder facilement aux objets liés)
  user = relationship("User", foreign_keys=[user_id], backref="expenses")
  category = relationship("Category", backref="expenses")
  supplier = relationship("Supplier", backref="expenses")
  
  def __repr__(self):
    """
    Représentation du modèle (pour le débogage)
    """
    return f"<Expense(id={self.id}, amount={self.amount}€, status={self.status}, user_id={self.user_id})>"
  
  @property
  def display_amount(self) -> str:
    """
    Retourne le montant formaté pour l'affichage
    """
    return f"{self.amount:.2f}€"
  