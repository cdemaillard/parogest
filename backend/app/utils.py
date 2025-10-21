import bcrypt
import hashlib

def _pre_hash_password(password: str) -> bytes:
  """
  Pré-hashe un mot de passe avec SHA-256.
  Contourne la limite de 72 octets de bcrypt.
   
  Args:
    password: Mot de passe en clair (longueur illimitée)
    
  Returns:
    Hash SHA-256 en bytes (32 octets)
  """
  return hashlib.sha256(password.encode('utf-8')).digest()

def hash_password(password: str) -> str:
  """
  Hashe un mot de passe (longueur illimitée).
  Double hashing : SHA-256 + bcrypt.
    
  Args:
      password: Mot de passe en clair
  
  Returns:
      Mot de passe hashé (string)
  """
  
  # Pré-hasher
  pre_hashed = _pre_hash_password(password)
  
  # Générer un salt et hasher avec bcrypt
  salt = bcrypt.gensalt(rounds=12)
  hashed = bcrypt.hashpw(pre_hashed, salt)
  
  return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
  """
  Vérifie un mot de passe.

  Args:
      plain_password: Mot de passe en clair
      hashed_password: Mot de passe hashé

  Returns:
      True si le mot de passe correspond
  """
  # Pre-hashing
  pre_hashed = _pre_hash_password(plain_password)
  
  return bcrypt.checkpw(pre_hashed, hashed_password.encode('utf-8'))