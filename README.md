# Projet ParoGest - Contexte de développement

## À propos du projet

ParoGest est un logiciel de gestion des dépenses pour une association catholique française. Le système permet de :

- Scanner et extraire les informations des factures/reçus (OCR)
- Gérer un portail de soumission de notes de frais pour prêtres et bénévoles
- Regrouper les paiements par fournisseur
- Gérer différents modes de paiement (espèces, virements, chèques)
- Automatiser la numérotation des chèques avec gestion des chéquiers

## Stack technique choisie

- **Backend** : Python 3.11 + FastAPI
- **Base de données** : PostgreSQL (via Docker)
- **ORM** : SQLAlchemy
- **Migrations** : Alembic
- **Validation** : Pydantic
- **Environnement** : macOS, VS Code

## Structure du projet actuelle

```
pароgest/
├── backend/
│   ├── venv/                    # Environnement virtuel Python
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py             # Point d'entrée FastAPI
│   │   ├── database.py         # Configuration PostgreSQL
│   │   ├── models.py           # Modèles SQLAlchemy (ORM)
│   │   ├── schemas.py          # Schémas Pydantic (validation)
│   │   └── routers/
│   │       └── suppliers.py    # Endpoints CRUD fournisseurs
│   ├── alembic/                # Migrations DB
│   └── requirements.txt
├── docs/
│   └── JOURNAL.md              # Journal de développement
└── .gitignore
```

## Progression du développement

### ✅ Session 1 - Setup initial (terminée)

- Structure projet créée
- Environnement virtuel configuré
- Dépendances installées (FastAPI, SQLAlchemy, Alembic, etc.)
- Premiers endpoints de test (`/`, `/health`, `/hello/{name}`)
- Premier commit Git

### ✅ Session 2 - PostgreSQL + Premier modèle (terminée)

- PostgreSQL lancé via Docker
- SQLAlchemy configuré avec connexion DB
- Modèle `Supplier` (fournisseur) créé avec colonnes : id, name, siret, address, email, phone, created_at, updated_at
- Première migration Alembic appliquée
- Table `suppliers` créée dans PostgreSQL

### 🔄 Session 3 - CRUD Suppliers (en cours)

- Schémas Pydantic créés : `SupplierBase`, `SupplierCreate`, `SupplierUpdate`, `SupplierResponse`
- Router `/api/suppliers` configuré
- Endpoints implémentés :
  - ✅ POST `/api/suppliers` - Créer un fournisseur
  - ✅ GET `/api/suppliers` - Lister les fournisseurs
  - ⏳ GET `/api/suppliers/{id}` - Récupérer un fournisseur (à faire)
  - ⏳ PUT `/api/suppliers/{id}` - Modifier un fournisseur (à faire)
  - ⏳ DELETE `/api/suppliers/{id}` - Supprimer un fournisseur (à faire)

### 📋 Prochaines sessions prévues

- Session 4 : Modèle `Category` (catégories de dépenses)
- Session 5 : Modèle `User` (utilisateurs et rôles)
- Session 6 : Modèle `Expense` (dépenses - cœur du système)
- Session 7 : Modèle `Receipt` (reçus/factures + OCR)
- Sessions 8-9 : Modèles `Payment`, `Check`, `Checkbook`

## Architecture objet adoptée

Le projet suit une approche Domain-Driven Design (DDD) où chaque concept métier devient un objet Python avec :

- **Attributs** : données structurées
- **Méthodes** : comportements associés
- **Validation automatique** via Pydantic
- **Relations** gérées par SQLAlchemy

Objets métier principaux à développer :

- Supplier (fournisseur) ✅
- Category (catégorie)
- User (utilisateur)
- Expense (dépense)
- Receipt (reçu/facture)
- Payment (paiement)
- Checkbook (chéquier)
- Check (chèque)

## Style de travail du développeur

- Apprend Python après une pause, se réacclimate progressivement
- Aime comprendre les concepts en profondeur avant d'avancer
- Préfère les explications claires avec exemples concrets
- Apprécie les analogies pour mieux visualiser
- Travaille de manière méthodique avec commits réguliers
- Tient un journal de développement dans `docs/JOURNAL.md`

## Instructions pour Claude

- Toujours se référer à ce contexte sans demander de rappel
- Proposer de continuer là où on s'est arrêté
- Vérifier l'état des services (Docker, venv, serveur) avant de commencer
- Expliquer les nouveaux concepts si nécessaire
- Garder un ton pédagogique et encourageant
- Fournir le code complet, pas de raccourcis
- Suggérer des commits Git après chaque étape importante
