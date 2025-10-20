from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from app.database import get_db
from app.models import Supplier
from app.schemas import (
  SupplierCreate,
  SupplierUpdate,
  SupplierResponse,
  PaginationParams,
  PaginatedResponse
)
from app.exceptions import *

router = APIRouter(
  prefix="/api/suppliers",
  tags=["suppliers"]
)

# CREATE - Créer un fournisseur
@router.post("/", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
def create_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
  try:
    
    # Verifier si doublon
    if supplier.email:
      existing = db.query(Supplier).filter(Supplier.email == supplier.email).first()
      if existing:
        raise DuplicateEmailException(supplier.email)
  
    db_supplier = Supplier(**supplier.model_dump())
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier
  except IntegrityError as e:
    db.rollback()
    # Si c'est une erreur de duplicate email qui n'a pas été catchée
    if "supplier_email_key" in str(e):
      raise DuplicateEmailException(supplier.email if supplier.email else "unknown")
    # Autre erreur d'intégrité
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail=f"Database integrity error: {str(e)}"
    )



# READ ALL - Lister tous les fournisseurs
@router.get("/", response_model=PaginatedResponse[SupplierResponse])
def get_suppliers(
  page: int = Query(1, ge=1, description="Page's number"),
  page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
  db: Session = Depends(get_db)
):
  
  # Paramètres de pagination
  pagination = PaginationParams(page=page, page_size=page_size)
  
  # Compter le total
  total = db.query(Supplier).count()
  
  # Récupérer les éélments paginés
  suppliers = db.query(Supplier)\
    .offset(pagination.skip)\
    .limit(pagination.limit)\
    .all()
  
  # Créer la réponse paginée MANNUELLEMENT
  return PaginatedResponse.create(
    items=suppliers,
    total=total,
    page=page,
    page_size=page_size,
  )

# READ ONE - Récupérer un forunisseur par ID
@router.get("/{supplier_id}", response_model=SupplierResponse)
def get_supplier(supplier_id: int, db: Session = Depends(get_db)):
  supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
  if not supplier:
    raise SupplierNotFoundException(supplier_id)
  return supplier

# UPDATE - Modifier un fournisseur
@router.put("/{supplier_id}", response_model=SupplierResponse)
def update_supplier(supplier_id: int, supplier_update: SupplierUpdate, db: Session = Depends(get_db)):
  try:
    db_supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not db_supplier:
      raise SupplierNotFoundException(supplier_id)
    
    # Vérifier l'unicité de l'email si on le modifie
    update_data = supplier_update.model_dump(exclude_unset=True)
    if "email" in update_data and update_data["email"]:
      existing = db.query(Supplier).filter(
        Supplier.email == update_data["email"],
        Supplier.id != supplier_id
      ).first()
      if existing:
        raise DuplicateEmailException(update_data["email"])
    
    # Appliquer les modifications
    for key, value in update_data.items():
      setattr(db_supplier, key, value)
    
    db.commit()
    db.refresh(db_supplier)
    return db_supplier
  except IntegrityError as e:
    db.rollback()
    if "suppliers_email_key" in str(e):
      raise DuplicateEmailException(update_data.get("email", "unknown"))
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail=f"Database integrity error: {str(e)}"
    )

# DELETE - Supprimer un fournisseur
@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
  db_supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
  if not db_supplier:
    raise SupplierNotFoundException(supplier_id)
  
  db.delete(db_supplier)
  db.commit()
  return None