from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from typing import Optional
from datetime import date, datetime

from app.database import get_db
from app.models.expense import Expense
from app.models.user import User
from app.models.category import Category
from app.models.supplier import Supplier
from app.schemas import (
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseApproval,
    ExpenseResponse,
    ExpenseDetailResponse,
    PaginationParams,
    PaginatedResponse
)
from app.enums import ExpenseStatus

router = APIRouter(
    prefix="/api/expenses",
    tags=["Expenses"]
)

# CREATE - Créer une dépense
@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
  expense: ExpenseCreate,
  user_id: int = Query(..., description="ID de l'utilisateur qui soumet la dépense"),
  db: Session = Depends(get_db)
):
  """
  Crée une nouvelle dépense.
  Note: En production, le user_id sera extrait du token JWT.
  Pour l'instant, on le passe en query parameter pour tester.
  """
  
  try:
    #Vérif que l'user existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with id {user_id} not found"
      )
    
    # Vérifier que la cat. existe
    category = db.query(Category).filter(Category.id == expense.category_id).first()
    if not category:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Category with id {expense.category_id} not found"
      )
    
    # Vérifier que le fournisseur existe si fourni
    if expense.supplier_id:
      supplier = db.query(Supplier).filter(Supplier.id == expense.supplier_id).first()
      if not supplier:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Supplier with id {expense.supplier_id} not found"
      )
    
    # Créer la dépense
    expense_data = expense.model_dump()
    expense_data["user_id"] = user_id
    expense_data["status"] = ExpenseStatus.PENDING
    
    db_expense = Expense(**expense_data)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense
  
  except IntegrityError as e:
    db.rollback()
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Database integrity error: {str(e)}"
    )

# READ ALL - Lister toutes les dépenses
@router.get("/", response_model=PaginatedResponse[ExpenseDetailResponse])
def get_expenses(
  page: int = Query(1, ge=1, description="Page number"),
  page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
  user_id: Optional[int] = Query(None, description="Filtrer par utilisateur"),
  category_id: Optional[int] = Query(None, description="Filtrer par catégorie"),
  supplier_id: Optional[int] = Query(None, description="Filtrer par fournisseur"),
  status: Optional[ExpenseStatus] = Query(None, description="Filtrer par statut"),
  min_amount: Optional[float] = Query(None, description="Montant minimum"),
  max_amount: Optional[float] = Query(None, description="Montant maximum"),
  start_date: Optional[date] = Query(None, description="Date de début"),
  end_date: Optional[date] = Query(None, description="Date de fin"),
  db: Session = Depends(get_db)
):
  """
  Liste toutes les dépenses avec filtres et pagination.
  Retourne les informations détaillées (avec noms des objets liés).
  """
  
  # Paramètres de pagination
  pagination = PaginationParams(page=page, page_size=page_size)
  
  # Construire requete de base
  query = db.query(Expense).options(
    joinedload(Expense.user),
    joinedload(Expense.category),
    joinedload(Expense.supplier),
    joinedload(Expense.approved_by)
  )
  
  # Appliquer les filtres
  if user_id:
    query = query.filter(Expense.user_id == user_id)
  
  if category_id:
    query = query.filter(Expense.category_id == category_id)
  
  if supplier_id:
    query = query.filter(Expense.supplier_id == supplier_id)
  
  if status:
    query = query.filter(Expense.status == status)
  
  if min_amount:
    query = query.filter(Expense.amout >= min_amount)
    
  if max_amount:
    query = query.filter(Expense.amount <= max_amount)
  
  if start_date:
    query = query.filter(Expense.expense_date >= start_date)
  
  if end_date:
    query = query.filter(Expense.expense_date <= end_date)
  
  # Compter le total après filtres
  total = query.count()
  
  # Récupérer les éléments paginés
  expenses = query\
    .order_by(Expense.expense_date.desc())\
    .offset(pagination.skip)\
    .limit(pagination.limit)\
    .all()
    
  # Enrichir les données avec les noms
  enriched_expenses = []
  for expense in expenses:
    expense_dict = {
      "id": expense.id,
      "amount": expense.amount,
      "description": expense.description,
      "expense_date": expense.expense_date,
      "status": expense.status,
      "user_id": expense.user_id,
      "category_id": expense.category_id,
      "supplier_id": expense.supplier_id,
      "approved_by_id": expense.approved_by_id,
      "approved_at": expense.approved_at,
      "created_at": expense.created_at,
      "updated_at": expense.updated_at,
      # Informations enrichies
      "user_email": expense.user.email if expense.user else None,
      "user_name": expense.user.full_name if expense.user else None,
      "category_name": expense.category.name if expense.category else None,
      "category_code": expense.category.code if expense.category else None,
      "supplier_name": expense.supplier.name if expense.supplier else None,
      "approved_by_email": expense.approved_by.email if expense.approved_by else None,
      "approved_by_name": expense.approved_by.name if expense.approved_by else None,
    }
    enriched_expenses.append(expense_dict)
    
    # Créer la réponse paginée
    return PaginatedResponse.create(
      items=enriched_expenses,
      total=total,
      page=page,
      page_size=page_size
    )

# READ ONE - Récupérer une dépense par ID
@router.get("/{expense_id}", response_model=ExpenseDetailResponse)
def get_expense(expense_id: int, db: Session = Depends(get_db)):
  """
  Récupère une dépense avec totues les informations détaillées
  """
  expense = db.query(Expense).options(
    joinedload(Expense.user),
    joinedload(Expense.category),
    joinedload(Expense.supplier),
    joinedload(Expense.approved_by)
  ).filter(Expense.id == expense_id).first()
  
  if not expense:
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with id {expense_id} not found"
        )
    
  # Enrichir les données
  expense_dict = {
    "id": expense.id,
    "amount": expense.amount,
    "description": expense.description,
    "expense_date": expense.expense_date,
    "status": expense.status,
    "user_id": expense.user_id,
    "category_id": expense.category_id,
    "supplier_id": expense.supplier_id,
    "approved_by_id": expense.approved_by_id,
    "approved_at": expense.approved_at,
    "created_at": expense.created_at,
    "updated_at": expense.updated_at,
    # Informations enrichies
    "user_email": expense.user.email if expense.user else None,
    "user_name": expense.user.full_name if expense.user else None,
    "category_name": expense.category.name if expense.category else None,
    "category_code": expense.category.code if expense.category else None,
    "supplier_name": expense.supplier.name if expense.supplier else None,
    "approved_by_email": expense.approved_by.email if expense.approved_by else None,
    "approved_by_name": expense.approved_by.name if expense.approved_by else None,
  }
  
  return expense_dict

# UPDATE - Modifier une dépense
@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
  expense_id: int,
  expense_update: ExpenseUpdate,
  db: Session = Depends(get_db)
):
  """
  Modifie une dépense existante.
  Seules les dépenses en statut PENDING peuvent être modifiées
  """
  try:
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not db_expense:
      raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail=f"Expense with id {expense_id} not found"
      )
    
    # Check status
    if not db_expense.status != ExpenseStatus.PENDING:
      raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail=f"Only PENDING expenses can be modified"
      )
    
    # Récupérer les données à mettre à jour
    update_data = expense_update.model_dump(exclude_unset=True)
    
    # Vérifier que la cat. existe
    if "category_id" in update_data:
      category = db.query(Category).filter(Category.id == update_data["category_id"]).first()
      if not category:
        raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail=f"Category with id {update_data["category_id"]} not found"
        )
    
    # Vérifier que le fournisseur existe si fourni
    if "supplier_id" in update_data and update_data["supplier_id"]:
      supplier = db.query(Supplier).filter(Supplier.id == update_data["supplier_id"]).first()
      if not supplier:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Supplier with id {update_data["supplier_id"]} not found"
      )
    
    # Appliquer les modifications
    for key, value in update_data.items():
      setattr(db_expense, key, value)
    
    db.commit()
    db.refresh(db_expense)
    return db_expense
  
  except IntegrityError as e:
    db.rollback()
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Database integrity error: {str(e)}"
    )

# APPROVE/