from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from app.database import get_db
from app.models import Category
from app.schemas import (
  CategoryCreate,
  CategoryUpdate,
  CategoryResponse,
  PaginationParams,
  PaginatedResponse
)

router = APIRouter(
  prefix="/api/categories",
  tags=["Categories"]
)

#CREATE - Créer une catégorie
@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
  try:
    # Vérifier doublon de nom
    existing_name = db.query(Category).filter(Category.name == category.name).first()
    if existing_name:
      raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"A category with name '{category.name}' already exist"
      )
    # Vérifier si doublon de code PCG (si fourni)
    if category.code:
      existing_code = db.query(Category).filter(Category.code == category.code).first()
      if existing_code:
        raise HTTPException(
          status_code=status.HTTP_409_CONFLICT,
          detail=f"This PCG code is already affected to '{existing_code.name}' category"
        )
    db_category = Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category
  except IntegrityError as e:
    db.rollback()
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail=f"Database integrity error: {str(e)}"
    )


# READ ALL - Lister toutes les catégories
@router.get("/", response_model=PaginatedResponse[CategoryResponse])
def get_categories(
  page: int = Query(1, ge=1, description="Page number"),
  page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
  search: Optional[str] = Query(None, description="Rechercher par nom, code ou description"),
  name: Optional[str] = Query(None, description="Rechercher par nom (contient)"),
  code: Optional[str] = Query(None, description="Rechercher par code (exact)"),
  is_active: Optional[bool] = Query(None, description="Filtrer par état d'activation"),
  db: Session = Depends(get_db)
):
  # Paramètre de pagination
  pagination = PaginationParams(page=page, page_size=page_size)
  
  # Construire la requête de base,
  query = db.query(Category)
  
  # Appliquer les filtres
  if search:
    # Recherche globale (nom OU code OU description)
    search_filter = f"%{search}%"
    query = query.filter(
      (Category.name.ilike(search_filter)) |
      (Category.code.ilike(search_filter)) |
      (Category.description.ilike(search_filter))
    )
  
  if name:
    query = query.filter(Category.name.ilike(f"‰{name}‰"))
  if code:
    query = query.filter(Category.code == code)
  if is_active is not None:
    query = query.filter(Category.is_active == is_active)
  
  # Compter le total après filtres
  total = query.count()
  
  # Récupérer les éléments paginés
  categories = query \
    .offset(pagination.skip)\
    .limit(pagination.limit)\
    .all()
  
  # Créer la réponse paginée
  return PaginatedResponse.create(
    items=categories,
    total=total,
    page=page,
    page_size=page_size
  )

#READ ONE - Récupérer une catgorie par ID
@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
  category = db.query(Category).filter(Category.id == category_id).first()
  if not category:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"Category with id {category_id} not found"
    )
  return category

# UPDATE - Modifier un catégorie
@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
  category_id: int,
  category_update: CategoryUpdate,
  db: Session = Depends(get_db)
):
  try:
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Category with id {category_id} not found"
      )
    
    # Récupérer les données à mettre à jour
    update_data = category_update.model_dump(exclude_unset=True)
    
    # Vérifier l'unicité du nom si modifié
    if "name" in update_data:
      existing = db.query(Category).filter(
        Category.name == update_data["name"],
        Category.id != category_id
      ).first()
      if existing:
        raise HTTPException(
          status_code=status.HTTP_409_CONFLICT,
          detail=f"A category with name '{update_data['name']}' already exist"
        )
    
    # Vérifier l'unicité du code si modifié
    if "code" in update_data and update_data["code"]:
      existing = db.query(Category).filter(
        Category.code == update_data["code"],
        Category.id != category_id
      ).first()
      if existing:
        raise HTTPException(
          status_code=status.HTTP_409_CONFLICT,
          detail=f"The PCG code '{update_data['code']}' is already affected to the category '{existing.name}'"
        )
    
    # Appliquer les modifications
    for key, value in update_data.items():
      setattr(db_category, key, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category
    
  except IntegrityError as e:
    db.rollback()
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail=f"Database integrity error: {str(e)}"
    )

# DELETE - Supprimer une catégorie
@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
  db_category = db.query(Category).filter(Category.id == category_id).first()
  if not db_category:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"Category wi id {category_id} not found"
    )
  
  db.delete(db_category)
  db.commit()
  return None