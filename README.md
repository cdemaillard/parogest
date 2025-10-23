# ParoGest - Logiciel de comptabilité paroissiale

## 📖 À propos du projet

ParoGest est un **logiciel de comptabilité de trésorerie** dédié aux paroisses catholiques françaises. Il couvre le cycle complet de la gestion financière paroissiale :

- 💰 **Comptage des recettes** : Gestion des séances hebdomadaires de comptage (quêtes, troncs, casuels, offrandes)
- 🏦 **Dépôts bancaires** : Préparation et suivi des borderaux de dépôt (poches espèces, enveloppes chèques)
- 🔄 **Rapprochement bancaire** : Import et réconciliation automatique des relevés bancaires
- 📊 **Comptabilité** : Génération automatique des écritures comptables (débit/crédit)
- 📤 **Export diocésain** : Fichier Excel mensuel compatible avec le logiciel Quadratus de l'économat

### Particularités

- **Comptabilité de trésorerie** : Enregistrement uniquement des flux d'argent réels (pas de créances/dettes)
- **Substitution intelligente** : Remplacement automatique des lignes bancaires agrégées par les détails d'origine
- **Workflow paroissial** : Adapté aux pratiques réelles (comptage hebdomadaire, quêtes impérées, casuels)

---

## 🛠️ Stack technique

- **Backend** : Python 3.11 + FastAPI
- **Base de données** : PostgreSQL 15 (via Docker)
- **ORM** : SQLAlchemy 2.0
- **Migrations** : Alembic
- **Validation** : Pydantic v2
- **Sécurité** : bcrypt (hash mots de passe)
- **Environnement** : macOS, VS Code

---

## 📁 Structure du projet

```
parogest/
├── backend/
│   ├── app/
│   │   ├── models/           # Modèles SQLAlchemy (ORM)
│   │   │   ├── supplier.py   # ✅ Fournisseurs (à migrer → Contact)
│   │   │   ├── category.py   # ✅ Catégories comptables
│   │   │   ├── user.py       # ✅ Utilisateurs
│   │   │   └── expense.py    # ✅ Dépenses (à refactorer → AccountMove)
│   │   │
│   │   ├── schemas/          # Schémas Pydantic (validation)
│   │   │   ├── suppliers.py
│   │   │   ├── category.py
│   │   │   ├── users.py
│   │   │   └── expenses.py
│   │   │
│   │   ├── routes/           # Endpoints API
│   │   │   ├── suppliers.py  # CRUD complet ✅
│   │   │   ├── categories.py # CRUD complet ✅
│   │   │   ├── users.py      # CRUD complet ✅
│   │   │   └── expenses.py   # CRUD complet ✅
│   │   │
│   │   ├── main.py           # Point d'entrée FastAPI
│   │   ├── database.py       # Configuration PostgreSQL
│   │   ├── enums.py          # Énumérations (UserRole, ExpenseStatus...)
│   │   ├── exceptions.py     # Exceptions custom
│   │   ├── validators.py     # Validateurs (SIRET...)
│   │   └── utils.py          # Utilitaires (hash password...)
│   │
│   ├── alembic/              # Migrations de base de données
│   │   └── versions/         # Historique des migrations
│   │
│   ├── venv/                 # Environnement virtuel Python
│   └── requirements.txt      # Dépendances Python
│
├── docs/
│   ├── JOURNAL.md            # Journal de développement
│   ├── LEXIQUE.md            # Documentation complète (modèles, vocabulaire)
│   └── ROADMAP.md            # Plan de développement
│
├── docker-compose.yml        # Configuration PostgreSQL
├── README.md                 # Ce fichier
└── .gitignore
```

---

## 🚀 Installation et démarrage

### Prérequis

- Python 3.11+
- Docker & Docker Compose
- Git

### 1. Cloner le projet

```bash
git clone https://github.com/votre-username/parogest.git
cd parogest
```

### 2. Démarrer PostgreSQL

```bash
docker-compose up -d
```

Vérifier que le conteneur tourne :

```bash
docker ps
# → Vous devriez voir "parogest_db"
```

### 3. Configurer l'environnement Python

```bash
cd backend
python3.11 -m venv venv
source venv/bin/activate  # Sur macOS/Linux
# ou
venv\Scripts\activate     # Sur Windows
```

### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 5. Appliquer les migrations

```bash
alembic upgrade head
```

### 6. Lancer le serveur

```bash
uvicorn app.main:app --reload
```

Le serveur démarre sur http://localhost:8000

---

## 📚 Documentation API

Une fois le serveur lancé, accédez à :

- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

---

## ✅ État actuel du développement

### Modèles implémentés

| Modèle       | Statut     | Description                                 |
| ------------ | ---------- | ------------------------------------------- |
| **Supplier** | ✅ Complet | Fournisseurs (à migrer vers Contact)        |
| **Category** | ✅ Complet | Catégories comptables (plan comptable)      |
| **User**     | ✅ Complet | Utilisateurs avec rôles et authentification |
| **Expense**  | ✅ Complet | Dépenses (à refactorer vers AccountMove)    |

### Endpoints API disponibles

```
POST   /api/suppliers           # Créer un fournisseur
GET    /api/suppliers           # Lister les fournisseurs (pagination + filtres)
GET    /api/suppliers/{id}      # Récupérer un fournisseur
PUT    /api/suppliers/{id}      # Modifier un fournisseur
DELETE /api/suppliers/{id}      # Supprimer un fournisseur

POST   /api/categories          # Créer une catégorie
GET    /api/categories          # Lister les catégories (pagination + filtres)
GET    /api/categories/{id}     # Récupérer une catégorie
PUT    /api/categories/{id}     # Modifier une catégorie
DELETE /api/categories/{id}     # Supprimer une catégorie

POST   /api/users               # Créer un utilisateur
GET    /api/users               # Lister les utilisateurs (pagination + filtres)
GET    /api/users/{id}          # Récupérer un utilisateur
PUT    /api/users/{id}          # Modifier un utilisateur
DELETE /api/users/{id}          # Supprimer un utilisateur

POST   /api/expenses            # Créer une dépense
GET    /api/expenses            # Lister les dépenses (pagination + filtres)
GET    /api/expenses/{id}       # Récupérer une dépense
PUT    /api/expenses/{id}       # Modifier une dépense
```

### Fonctionnalités implémentées

- ✅ **Pagination** sur toutes les listes (page, page_size, total_pages)
- ✅ **Filtres de recherche** multiples par endpoint
- ✅ **Validation SIRET** avec algorithme de Luhn
- ✅ **Hash de mots de passe** sécurisé (bcrypt + SHA-256)
- ✅ **Gestion d'erreurs** custom (SupplierNotFoundException, DuplicateEmailException...)
- ✅ **Relations ORM** (Expense → User, Category, Supplier)
- ✅ **Réponses enrichies** (ExpenseDetailResponse avec noms des objets liés)

---

## 🔄 Prochaines étapes (Roadmap)

### Phase 1 : Refonte architecture (En cours)

#### Session prochaine : Migration Supplier → Contact

- [ ] Créer migration Alembic (renommer table + ajouter colonnes)
- [ ] Mettre à jour modèle SQLAlchemy avec `contact_type`
- [ ] Adapter schémas Pydantic
- [ ] Modifier router `/api/suppliers` → `/api/contacts`
- [ ] Tester avec différents types (fournisseur, donateur, prêtre, bénévole)

#### Sessions suivantes

- [ ] Refactorer Expense → AccountMove + AccountMoveLine
- [ ] Créer modèle Account (comptes bancaires/caisses)
- [ ] Mettre à jour Category avec plan comptable diocésain

### Phase 2 : Workflow comptage

- [ ] Modèle CountingSession (séances hebdomadaires)
- [ ] Modèle CountingItem (items comptés)
- [ ] Modèle BankDeposit (borderaux de dépôt)
- [ ] Interface de saisie comptage
- [ ] Interface de répartition en dépôts
- [ ] Génération automatique AccountMove à la clôture

### Phase 3 : Rapprochement bancaire

- [ ] Modèle BankTransaction
- [ ] Import relevés bancaires (parsing Excel)
- [ ] Algorithme de rapprochement automatique
- [ ] Gestion des écarts
- [ ] Dashboard de réconciliation

### Phase 4 : Export et reporting

- [ ] Générateur export Quadratus (substitution intelligente)
- [ ] Gestion quêtes impérées (reversement diocèse)
- [ ] Rapports analytiques
- [ ] Dashboard trésorerie

### Phase 5 (Optionnel) : Modules avancés

- [ ] Module Sacrements (baptêmes, mariages, obsèques)
- [ ] Liaison casuels ↔ sacrements
- [ ] Répartition automatique intelligente (poids des poches)
- [ ] Scan et archivage duplicatas PDF
- [ ] Notifications automatiques

---

## 📖 Documentation complète

Consultez le fichier [LEXIQUE.md](docs/LEXIQUE.md) pour :

- Description détaillée de tous les modèles
- Glossaire du vocabulaire métier paroissial
- Architecture et relations entre objets
- Workflows détaillés (comptage → export)

---

## 🤝 Contribution

Projet en développement actif. Contributions bienvenues après validation de l'architecture.

---

## 📝 Journal de développement

Voir [docs/JOURNAL.md](docs/JOURNAL.md) pour l'historique détaillé des sessions de développement.

---

## 📄 Licence

À définir

---

## 👤 Auteur

Projet développé pour une paroisse catholique française.

---

**Version actuelle** : 0.2.0 (Phase 1 - Refonte architecture)  
**Dernière mise à jour** : 24 octobre 2024
