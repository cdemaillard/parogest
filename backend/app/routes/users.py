from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional

from app.database import get_db
from app.models.user import User
from app.schemas import (
    UserCreate,
    UserUpdate,
    UserResponse,
    PaginationParams,
    PaginatedResponse
)
from app.utils import hash_password
from app.enums import UserRole

router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
  try:
    # Check si l'email existe déjà
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
      raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"A user with email '{user.email}' already exists"
      )
    
    # Créer le dictionnaire avec les données de l'utilisateur
    user_data = user.model_dump(exclude={"password"})
    
    # Hasher le mot de passe
    user_data["hashed_password"] = hash_password(user.password)
    
    # Créer l'utilisateur
    db_user = User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
  
  except IntegrityError as e:
    db.rollback()
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail=f"Database integrity error: {str(e)}"
    )

# READ ALL - Lister tous les utilisateurs
@router.get("/", response_model=PaginatedResponse[UserResponse])
def get_users(
  page: int = Query(1, ge=1, description="Page's number"),
  page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
  search: Optional[str] = Query(None, description="Rechercher par nom, prénom ou email"),
  email: Optional[str] = Query(None, description="Filtrer par email (contient)"),
  role: Optional[UserRole] = Query(None, description="Filtrer par rôle"),
  is_active: Optional[bool] = Query(None, description="Fitlrer par status actif"),
  db: Session = Depends(get_db)
  ):
  
  # Params pagination
  pagination = PaginationParams(page=page, page_size=page_size)
  
  # Construction de la requête
  query = db.query(User)
  
  # Appliquer filtres
  if search:
    #Recherche globale (prnom OU nom OU email)
    search_filter = f"%{search}%"
    query = query.filter(
      (User.first_name.ilike(search_filter)) |
      (User.last_name.ilike(search_filter)) |
      (User.email.ilike(search_filter))
    )
  
  if email:
    query = query.filter(User.email.ilike(f"%{email}‰"))
  
  if role:
        query = query.filter(User.role == role)
    
  if is_active is not None:
      query = query.filter(User.is_active == is_active)
      
  # Compter le total après filtres
  total = query.count()
  
  # Récupérer les éléments paginés
  users = query\
    .offset(pagination.skip)\
    .limit(pagination.limit)\
    .all()
  # Créer la réponse paginé
  return PaginatedResponse.create(
    items=users,
    total=total,
    page=page,
    page_size=page_size
  )

#READ ONE - Récupérer une catgorie par ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
  user = db.query(User).filter(User.id == user_id).first()
  if not user:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"User with id {user_id} not found"
    )
  return user

# UPDATE - Modifier un catégorie
@router.put("/{user_id}", response_model=UserResponse)
def update_user(
  user_id: int,
  user_update: UserUpdate,
  db: Session = Depends(get_db)
):
  try:
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with id {user_id} not found"
      )
    
    # Récupérer les données à mettre à jour
    update_data = user_update.model_dump(exclude_unset=True)
    
    # Vérifier l'unicité de l'email si modifié
    if "email" in update_data:
      existing = db.query(User).filter(
        User.email == update_data["email"],
        User.id != user_id
      ).first()
      if existing:
        raise HTTPException(
          status_code=status.HTTP_409_CONFLICT,
          detail=f"A user with email '{update_data['email']}' already exist"
        )
    
    # Si nouveau mot de passe, le hahser
    if "password" in update_data:
      update_data["hashed_password"] = hash_password(update_data["password"])
      del update_data["password"] # Suppression du MdP en clair (sécurité)
    
    # Appliquer les modifications
    for key, value in update_data.items():
      setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user
    
  except IntegrityError as e:
    db.rollback()
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail=f"Database integrity error: {str(e)}"
    )

# DELETE - Supprimer un utilisateur
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
  db_user = db.query(User).filter(User.id == user_id).first()
  if not db_user:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"User with id {user_id} not found"
    )
  db.delete(db_user)
  db.commit()
  return None