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