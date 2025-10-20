import re

def validate_siret(siret: str) -> bool:
  """
  Valide un numéro de SIRET français.
  Args:
    siret: Le numéro de SIRET à valider
  
  Returns:
    True si valide, False sinon
  """
  if not siret:
    return True
  
  if not re.match(r'^\d{14}$', siret):
    return False
  
  #Algorithme de Luhn pour vérifier la validité
  total = 0
  for i, digit in enumerate(siret):
    n = int(digit)
    # Les chiffres en position impaire (index pair) sont doublés
    # On compte de droite à gauche, donc on inverse
    if (len(siret) - i) % 2 == 0:
      n *= 2
      # Si le résultat est > 9, on soustrait 9
      if n > 9:
        n -= 9
    total += n
    
    # Le total doit être un multiple de 10
  return total % 10 == 0

def format_siret(siret: str) -> str:
  """ 
  Formate un SIRET pour le rendre plus lisible
  Args:
    siret: numéro à formater
    
  Returns:
    SIRET formaté (XXX XXX XXX XXXXX)
  """
  
  if not siret or len(siret) != 14:
    return siret
  
  return f"{siret[:3]} {siret[3:6]} {siret[6:9]} {siret[9:]}"