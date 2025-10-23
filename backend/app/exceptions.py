from fastapi import HTTPException, status

# === Exceptions CONTACT (nouveau) ===
class ContactNotFoundException(HTTPException):
  def __init__(self, contact_id: int):
    super().__init__(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Contact with id {contact_id} not found"
    )


# === Exceptions communes ===
class DuplicateEmailException(HTTPException):
  """
  Exception levée quand un email existe déjà dans la base.
  Utilisable pour Supplier et Contact.
  """
  def __init__(self, email: str):
    super().__init__(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"A contact with email '{email}' already exists"
    )


class InvalidSiretException(HTTPException):
  """
  Exception levée quand un SIRET est invalide.
  Utilisable pour Supplier et Contact.
  """
  def __init__(self, siret: str):
    super().__init__(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=f"Invalid SIRET number: '{siret}'. Must be 14 digits."
    )