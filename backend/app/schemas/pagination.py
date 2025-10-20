from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel

T = TypeVar('T')

class PaginationParams(BaseModel):
  """Paramètres de pagination"""
  page: int = 1
  page_size: int = 20
  
  @property
  def skip(self) -> int:
    """Calcule le nombre d'éléments à sauter"""
    return (self.page - 1) * self.page_size
  
  @property
  def limit(self) -> int:
    """Alias pour page_size"""
    return self.page_size

class PaginatedResponse(BaseModel, Generic[T]):
  """Réponse paginée générique"""
  items: List[T]
  total: int
  page: int
  page_size: int
  total_pages: int
  has_next: bool
  has_previous: bool
  
  @classmethod
  def create(cls, items: List[T], total: int, page: int, page_size: int):
    """Crée une réponse paginé"""
    total_pages = (total + page_size -1) // page_size # Arrondi supérieur
    
    return cls(
      items = items,
      total = total,
      page = page,
      page_size = page_size,
      total_pages = total_pages,
      has_next = page < total_pages,
      has_previous = page > 1
    )