from fastapi import HTTPException, status

class SupplierNotFoundException(HTTPException):
  def __init__(self, supplier_id: int):
    super().__init__(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"Supplier with id {supplier_id} not found"
    )

class DuplicateEmailException(HTTPException):
  def __init__(self, email: str):
    super().__init__(
      status_code=status.HTTP_409_CONFLICT,
      detail=f"A supplier with email '{email} already exists"
    )

class InvalidSiretException(HTTPException):
  def __init__(self, siret: str):
    super().__init__(
      status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
      detail=f"Invalid SIRET number: '{siret}'. Must be 14 digits."
    )