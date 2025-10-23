from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from app.database import get_db
from app.models import Contact
from app.schemas import (
  ContactCreate,
  ContactUpdate,
  ContactResponse,
  PaginationParams,
  PaginatedResponse
)
from app.enums import ContactType
from app.exceptions import ContactNotFoundException, DuplicateEmailException

router = APIRouter(
  prefix="/api/contacts",
  tags=["contacts"]
)

# CREATE - Créer un fournisseur
@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
  """
  Créer un nouveau contact
  """
  try:
    # Verifier si doublon d'email
    if contact.email:
      existing = db.query(Contact).filter(Contact.email == contact.email).first()
      if existing:
        raise DuplicateEmailException(contact.email)
  
    db_contact = Contact(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact
  
  except IntegrityError as e:
    db.rollback()
    # Si c'est une erreur de duplicate email qui n'a pas été catchée
    if "contact_email_key" in str(e):
      raise DuplicateEmailException(contact.email if contact.email else "unknown")
    # Autre erreur d'intégrité
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail=f"Database integrity error: {str(e)}"
    )



# READ ALL - Lister tous les fournisseurs
@router.get("/", response_model=PaginatedResponse[ContactResponse])
def get_contacts(
  page: int = Query(1, ge=1, description="Page's number"),
  page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
  search: Optional[str] = Query(None, description="Rechercher par nom, email ou SIRET"),
  contact_type: Optional[ContactType] = Query(None, description="Filtrer par type de contact"),
  name: Optional[str] = Query(None, description="Filtrer par nom (contient)"),
  email: Optional[str] = Query(None, description="Filtrer par email (contient)"),
  siret: Optional[str] = Query(None, description="Filtrer par SIRET (exact)"),
  city: Optional[str] = Query(None, description="Filtrer par ville (contient)"),
  active: Optional[bool] = Query(None, description="Filtrer par status actif/archivé"),
  db: Session = Depends(get_db)
):
  
  """
  Lister tous les contacts avec pagination et filtres
  """
  # Paramètres de pagination
  pagination = PaginationParams(page=page, page_size=page_size)
  
  # Construire la requête de base
  query = db.query(Contact)
  
  # Appliquer les filtres
  if search:
    # Recherche globale (nom OU email OU siret)
    search_filter = f"%{search}%"
    query = query.filter(
      (Contact.name.ilike(search_filter)) |
      (Contact.email.ilike(search_filter)) |
      (Contact.siret.ilike(search_filter))
    )
  
  if name:
    query = query.filter(Contact.name.ilike(f"%{name}%"))
  
  if email:
    query = query.filter(Contact.email.ilike(f"%{email}%"))
  
  if siret:
    query = query.filter(Contact.siret == siret)
  
  if city:
    query = query.filter(Contact.city.ilike(f"%{city}%"))
  
  if active is not None:
    query = query.filter(Contact.active == active)
  
  # Compter le total après filtres
  total = query.count()
  
  # Récupérer les éélments paginés
  contacts = query\
    .offset(pagination.skip)\
    .limit(pagination.limit)\
    .all()
  
  # Créer la réponse paginée MANNUELLEMENT
  return PaginatedResponse.create(
    items=contacts,
    total=total,
    page=page,
    page_size=page_size,
  )

# READ ONE - Récupérer un forunisseur par ID
@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
  """
  Récupérer un contact spécifique par son ID
  """
  contact = db.query(Contact).filter(Contact.id == contact_id).first()
  if not contact:
    raise ContactNotFoundException(contact_id)
  return contact

# UPDATE - Modifier un fournisseur
@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact(
  contact_id: int,
  contact_update: ContactUpdate,
  db: Session = Depends(get_db)
):
  """
  Modifier un contact existant
  """
  try:
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
      raise ContactNotFoundException(contact_id)
    
    # Vérifier l'unicité de l'email si on le modifie
    update_data = contact_update.model_dump(exclude_unset=True)
    if "email" in update_data and update_data["email"]:
      existing = db.query(Contact).filter(
        Contact.email == update_data["email"],
        Contact.id != contact_id
      ).first()
      if existing:
        raise DuplicateEmailException(update_data["email"])
    
    # Appliquer les modifications
    for key, value in update_data.items():
      setattr(db_contact, key, value)
    
    db.commit()
    db.refresh(db_contact)
    return db_contact
  
  except IntegrityError as e:
    db.rollback()
    if "suppliers_email_key" in str(e):
      raise DuplicateEmailException(update_data.get("email", "unknown"))
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail=f"Database integrity error: {str(e)}"
    )

# DELETE - Supprimer un fournisseur
@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
  db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
  if not contact_id:
    raise ContactNotFoundException(contact_id)
  
  db.delete(db_contact)
  db.commit()
  return None