from enum import Enum

class UserRole(str, Enum):
    """
    Rôles possibles pour les utilisateurs de ParoGest.
    """
    PRIEST = "priest"
    VOLUNTEER = "volunteer"
    TREASURER = "treasurer"
    ADMIN = "admin"
    
    def __str__(self):
        return self.value


class ExpenseStatus(str, Enum):
    """
    Statuts possibles pour les dépenses.
    """
    DRAFT = "draft"
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"
    
    def __str__(self):
        return self.value


class ContactType(str, Enum):
    """
    Types de contacts possibles dans ParoGest.
    
    - SUPPLIER: Fournisseur (EDF, plombier, organiste...)
    - DONOR: Fidèle donateur
    - VOLUNTEER: Bénévole (comptage, secrétariat...)
    - PRIEST: Prêtre (curé, vicaire, diacre)
    - DIOCESE: Économat diocésain
    - OTHER: Autre type de contact
    """
    SUPPLIER = "supplier"
    DONOR = "donor"
    VOLUNTEER = "volunteer"
    PRIEST = "priest"
    DIOCESE = "diocese"
    OTHER = "other"
    
    def __str__(self):
        return self.value
    
    # AJOUT CRITIQUE : Force Pydantic à utiliser la valeur, pas le nom
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema
        return core_schema.no_info_after_validator_function(
            cls,
            core_schema.str_schema(),
        )