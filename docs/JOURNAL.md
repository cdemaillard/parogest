# Journal de développement ParoGest

## 2024-10-19 - Jour 1 ✅

### ✅ Réalisé

- Création repo GitHub "pароgest"
- Structure projet backend
- Environnement virtuel Python 3.11
- Installation dépendances (FastAPI, SQLAlchemy, etc.)
- Premier endpoint API fonctionnel (/ et /health)
- Tests Swagger réussis

### 📚 Appris

- Setup FastAPI de base
- Décorateurs @app.get()
- Documentation Swagger auto-générée
- Différence def vs async def (basique)
- SQLAlchemy = ORM
- Alembic = migrations DB

### 🤔 Questions restantes

- Approfondir async/await (plus tard)
- Comment marche SQLAlchemy concrètement (demain)

### 🎯 Prochaine session

- Setup PostgreSQL (local ou Docker)
- Configuration SQLAlchemy
- Premier modèle : Supplier

### ⏱️ Temps passé

~3h (dont interruptions questions/explications)

### 😊 Ressenti

Satisfait ! Premier serveur API qui tourne. Swagger impressionnant.

## 2024-10-20 - Jour 2 ✅

### ✅ Réalisé

- Setup PostgreSQL avec Docker
- Résolu conflit port 5432 (PostgreSQL local vs Docker)
- Configuration SQLAlchemy complète
- Création modèle Supplier
- Setup et config Alembic
- Première migration créée et appliquée
- Table suppliers créée en DB

### 📚 Appris

- Docker Compose pour PostgreSQL
- SQLAlchemy : engine, SessionLocal, Base
- Différence `yield` vs `return`
- Concept d'index sur colonnes
- Alembic autogenerate
- Résolution de conflits de ports

### 🤔 Questions résolues

- Pourquoi yield + finally (éviter connection leaks)
- Index = vitesse de recherche (pas ordre)
- server_default vs default (SQL vs Python)

### 🎯 Prochaine session

- Création endpoints CRUD pour Suppliers
- Tests avec Swagger

### ⏱️ Temps passé

~2h (dont debug PostgreSQL)

### 😊 Ressenti

Galère Docker mais résolu ! Modèle créé, migration appliquée. Prêt pour les endpoints !
