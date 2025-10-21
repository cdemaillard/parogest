from enum import Enum

class UserRole(str, Enum):
  """
  Roles possibles pour les utilisateurs de ParoGest.
  """
  
  PRIEST = "priest",
  VOLUNTEER =  "volunteer"
  TREASURER =  "treasurer"
  ADMIN = "admin"
  
  def __str__(self):
    return self.value

class ExpenseStatus(str, Enum):
  """
  Status possibles pour les dépenses
  """
  DRAFT = "draft"
  PENDING = "pending"
  PAID = "paid"
  CANCELLED = "cancelled"
  
  def __str__(self):
    return self.value