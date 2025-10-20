from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Supplier
from app.schemas import *

router = APIRouter(
  prefix="/api/suppliers",
  tags=["suppliers"]
)

# CREATE - Créer un fournisseur
@router.post("/", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
def create_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
  db_supplier = Supplier(**supplier.model_dump())
  db.add(db_supplier)
  db.commit()
  db.refresh(db_supplier)
  return db_supplier

# READ ALL - Lister tous les fournisseurs
@router.get("/", response_model=List[SupplierResponse])
def get_suppliers(skip: int=0, limit: int= 100, db: Session = Depends(get_db)):
  suppliers = db.query(Supplier).offset(skip).limit(limit).all()
  return suppliers

# READ ONE - Récupérer un forunisseur par ID
@router.get("/{supplier_id}", response_model=SupplierResponse)
def get_supplier(supplier_id: int, db: Session = Depends(get_db)):
  supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
  if not supplier:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"Supplier with id {supplier_id} not found"
    )
  return supplier

# UPDATE - Modifier un fournisseur
@router.put("/{supplier_id}", response_model=SupplierResponse)
def update_supplier(supplier_id: int, supplier_update: SupplierUpdate, db: Session = Depends(get_db)):
  db_supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
  if not db_supplier:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"Supplier with id {supplier_id} not found"
    )
  # Mettre à jour uniquement les champs fournis
  update_data = supplier_update.model_dump(exclude_unset=True)
  for key, value in update_data.items():
    setattr(db_supplier, key, value)
  
  db.commit()
  db.refresh(db_supplier)
  return db_supplier

# DELETE - Supprimer un fournisseur
@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
  db_supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
  if not db_supplier:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"Supplier with id {supplier_id} not found"
    )
  
  db.delete(db_supplier)
  db.commit()
  return None