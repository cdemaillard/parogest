from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

#URL de connexion PostgreSQL
SQLALCHEMY_DATABASE_URL = os.getenv(
  "DATABASE_URL",
  "postgresql://parogest_user:parogest_dev_password@localhost:5432/parogest_dev"
)

#Création du moteur SQLACHEMY
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#Session pour interagir avec la DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles
Base = declarative_base()

# Fonction helper pour obtenir une session db

def get_db():
  """
  Génère une session de base de données.
  À utiliser comme dépendance FastAPI
  """
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()