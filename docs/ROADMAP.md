# 🗺️ Roadmap ParoGest

## 📍 État actuel (Version 0.2.0)

### ✅ Modèles implémentés
- **Supplier** (4 CRUD endpoints complets)
- **Category** (5 CRUD endpoints complets)
- **User** (5 CRUD endpoints complets)
- **Expense** (4 CRUD endpoints)

### ✅ Fonctionnalités opérationnelles
- Pagination sur toutes les listes
- Filtres de recherche multiples
- Validation SIRET (algorithme de Luhn)
- Hash de mots de passe sécurisé (bcrypt + SHA-256)
- Gestion d'erreurs custom
- Relations ORM fonctionnelles

---

## 🎯 Phase 1 : Refonte architecture (En cours)

### 🔄 Session prochaine : Migration Supplier → Contact

**Objectif** : Transformer le modèle `Supplier` en modèle `Contact` unifié.

**Tâches :**
1. ✅ Architecture validée (4 types de contact : SUPPLIER, DONOR, VOLUNTEER, PRIEST)
2. [ ] Créer migration Alembic
   - Renommer table `suppliers` → `contacts`
   - Ajouter colonne `contact_type` (enum)
   - Ajouter colonnes spécifiques :
     - `is_company` (boolean)
     - `display_name` (string)
     - `mobile` (string)
     - `street`, `street2`, `zip_code`, `city`, `country`
     - `vat_number` (string)
     - `is_donor`, `anonymize_donation` (boolean)
     - `ministry_role`, `ordination_date` (priest)
     - `volunteer_skills` (JSON)
     - `bank_name`, `iban`, `bic` (pour remboursements)
   - Migrer données existantes (tous → type SUPPLIER)
3. [ ] Mettre à jour modèle SQLAlchemy
   - Renommer `models/supplier.py` → `models/contact.py`
   - Ajouter enum `ContactType`
   - Ajouter tous les nouveaux champs
   - Mettre à jour relations
4. [ ] Adapter schémas Pydantic
   - Renommer `schemas/suppliers.py` → `schemas/contact.py`
   - `ContactBase`, `ContactCreate`, `ContactUpdate`, `ContactResponse`
   - Validation conditionnelle selon `contact_type`
5. [ ] Modifier router
   - Renommer `routes/suppliers.py` → `routes/contacts.py`
   - Routes : `/api/suppliers` → `/api/contacts`
   - Filtres : ajouter `contact_type`
6. [ ] Tests
   - Créer un fournisseur (EDF)
   - Créer un donateur (M. Dupont)
   - Créer un prêtre (Abbé Martin)
   - Créer un bénévole (Marie)
   - Tester les filtres par type

**Commit** : `refactor: migrate Supplier to Contact model`

**Durée estimée** : 2-3 heures

---

### Session 2 : Refactorer Expense → AccountMove + AccountMoveLine

**Objectif** : Transformer le modèle simple `Expense` en architecture comptable double entrée.

**Tâches :**
1. [ ] Créer modèle `AccountMove`
   - Enum `AccountMoveType` (ENTRY, IN_INVOICE, IN_REFUND, BANK_TRANSFER)
   - Enum `AccountMoveState` (DRAFT, POSTED, CANCELLED)
   - Champs : name, move_type, state, date, partner_id, ref, amount_total...
   - Relations : partner (Contact), lines (AccountMoveLine), account, counting_session
2. [ ] Créer modèle `AccountMoveLine`
   - Champs : move_id, account_code, account_name, name, debit, credit, sequence
   - Relation : counting_item_id (traçabilité)
3. [ ] Migration Alembic
   - Créer tables `account_moves` et `account_move_lines`
   - Migrer données `expenses` vers `account_moves` (type IN_INVOICE)
   - Supprimer table `expenses` (ou garder temporairement)
4. [ ] Schémas Pydantic
   - `AccountMoveBase`, `AccountMoveCreate`, `AccountMoveUpdate`, `AccountMoveResponse`
   - `AccountMoveLineBase`, etc.
   - Validation équilibre débit/crédit
5. [ ] Router `/api/account-moves`
   - CRUD complet
   - Validation automatique équilibre
6. [ ] Tests
   - Créer facture fournisseur (2 lignes : débit charge, crédit banque)
   - Vérifier refus si déséquilibré

**Commit** : `refactor: replace Expense with AccountMove + AccountMoveLine`

**Durée estimée** : 4-5 heures

---

### Session 3 : Créer modèle Account

**Objectif** : Gérer les comptes bancaires et caisses.

**Tâches :**
1. [ ] Créer modèle `Account`
   - Enum `AccountType` (BANK, CASH, SAVINGS)
   - Champs : name, account_type, bank_name, iban, opening_balance, current_balance, currency, active
2. [ ] Migration Alembic
3. [ ] Schémas Pydantic
4. [ ] Router `/api/accounts`
   - CRUD complet
   - Calcul automatique `current_balance` (via sum des AccountMove)
5. [ ] Seed data (comptes initiaux)
   - Compte courant Crédit Agricole
   - Caisse espèces presbytère
6. [ ] Tests

**Commit** : `feat: add Account model for bank accounts and cash`

**Durée estimée** : 2 heures

---

### Session 4 : Enrichir Category avec plan comptable diocésain

**Objectif** : Adapter le modèle Category existant au plan comptable paroissial.

**Tâches :**
1. [ ] Ajouter enum `CategoryType` (INCOME, EXPENSE)
2. [ ] Migration Alembic (ajout colonne `category_type`)
3. [ ] Seed data (plan comptable complet)
   - Produits (70xxx) : quêtes, casuels, offrandes, dons
   - Charges (60xxx, 62xxx) : électricité, chauffage, déplacements...
4. [ ] Adapter router (filtre par type)
5. [ ] Mapper collection_type → accounting_code
   - `QUETE_DOMINICALE` → `70100`
   - `CASUEL_OBSEQUE` → `70300`
   - etc.

**Commit** : `feat: enrich Category with parish accounting plan`

**Durée estimée** : 1-2 heures

---

## 🎯 Phase 2 : Workflow comptage (Sessions 5-9)

### Session 5 : Créer modèle CountingSession

**Objectif** : Gérer les séances hebdomadaires de comptage.

**Tâches :**
1. [ ] Créer modèle `CountingSession`
   - Enum `CountingSessionStatus` (DRAFT, COMPLETED, CLOSED)
   - Champs : date, status, counted_by, notes, totaux...
   - Relations : items, deposits, account_move
2. [ ] Migration Alembic
3. [ ] Schémas Pydantic
4. [ ] Router `/api/counting-sessions`
   - POST : créer session
   - GET : lister sessions
   - GET /{id} : détails session
   - PUT /{id}/complete : marquer terminée
   - PUT /{id}/close : clôturer (génère AccountMove)
5. [ ] Service `CountingService`
   - Logique de clôture
   - Génération AccountMove type ENTRY
6. [ ] Tests

**Commit** : `feat: add CountingSession model`

**Durée estimée** : 3 heures

---

### Session 6 : Créer modèle CountingItem

**Objectif** : Gérer les items comptés (sacs de collecte).

**Tâches :**
1. [ ] Créer modèle `CountingItem`
   - Enum `CollectionType` (QUETE_DOMINICALE, TRONC, CASUEL...)
   - Champs : location, event_date, event_label, détails JSON, totaux...
   - Champ `is_impereed` + `impereed_destination`
2. [ ] Migration Alembic
3. [ ] Schémas Pydantic
   - Validation JSON `coins_detail`, `bills_detail`, `checks_detail`
4. [ ] Router `/api/counting-items`
   - POST : créer item (dans une session)
   - GET : lister items d'une session
   - PUT /{id} : modifier item
   - DELETE /{id} : supprimer item
5. [ ] Tests
   - Créer quête dominicale avec détail pièces
   - Créer casuel avec chèque
   - Créer quête impérée

**Commit** : `feat: add CountingItem model`

**Durée estimée** : 3-4 heures

---

### Session 7 : Interface de saisie comptage

**Objectif** : Créer endpoints pour le workflow de saisie.

**Tâches :**
1. [ ] Endpoint POST `/api/counting-sessions/{id}/items`
   - Créer item dans session en cours
   - Validation : session doit être DRAFT
   - Mise à jour automatique totaux session
2. [ ] Endpoint GET `/api/counting-sessions/{id}/summary`
   - Récap détaillé : totaux par type, par compte comptable
   - Liste des items avec montants
3. [ ] Logique métier
   - Calcul automatique totaux (coins, bills, checks)
   - Suggestion code comptable selon collection_type
   - Validation : montants cohérents
4. [ ] Tests postman/curl

**Commit** : `feat: add counting input workflow endpoints`

**Durée estimée** : 2 heures

---

### Session 8 : Créer modèle BankDeposit

**Objectif** : Gérer les borderaux de dépôt bancaire.

**Tâches :**
1. [ ] Créer modèle `BankDeposit`
   - Enum `DepositType` (COINS, BILLS, CHECKS)
   - Champs : deposit_number, deposit_date, planned_amount, credited_amount...
   - Gestion écarts : has_discrepancy, discrepancy_amount, discrepancy_notes
2. [ ] Table de liaison many-to-many
   - `counting_item_deposits` (item_id, deposit_id)
3. [ ] Migration Alembic
4. [ ] Schémas Pydantic
5. [ ] Router `/api/bank-deposits`
   - POST : créer dépôt
   - GET : lister dépôts
   - PUT /{id} : mettre à jour (montant crédité, date crédit)
6. [ ] Tests

**Commit** : `feat: add BankDeposit model`

**Durée estimée** : 2-3 heures

---

### Session 9 : Interface de répartition en dépôts

**Objectif** : Permettre la répartition des items en dépôts bancaires.

**Tâches :**
1. [ ] Endpoint POST `/api/counting-sessions/{id}/deposits`
   - Créer dépôt lié à la session
   - Paramètres : type, montant, items_ids[]
2. [ ] Endpoint POST `/api/bank-deposits/{id}/add-items`
   - Ajouter items à un dépôt existant
3. [ ] Endpoint GET `/api/counting-sessions/{id}/deposits-summary`
   - Totaux à répartir (coins, bills, checks)
   - Totaux déjà répartis
   - Reste à répartir
4. [ ] Logique validation
   - Total réparti = Total compté
   - Un item peut être dans plusieurs dépôts (cas division)
   - Génération automatique numéro bordereau
5. [ ] Tests
   - Scénario 1 : Regrouper 3 petits sacs → 1 dépôt
   - Scénario 2 : Diviser 1 gros sac → 2 dépôts (euros/centimes)

**Commit** : `feat: add deposit allocation workflow`

**Durée estimée** : 3 heures

---

### Session 10 : Clôture session et génération AccountMove

**Objectif** : Finaliser le workflow de comptage.

**Tâches :**
1. [ ] Endpoint PUT `/api/counting-sessions/{id}/close`
   - Validation : session COMPLETED, dépôts créés, répartition complète
   - Génération AccountMove type ENTRY
     - 1 ligne débit Caisse (total)
     - N lignes crédit Produits (une par item)
   - Mise à jour session.account_move_id
   - Status → CLOSED
2. [ ] Service `AccountingService.generate_move_from_session()`
   - Création AccountMove
   - Création AccountMoveLine par CountingItem
   - Validation équilibre débit/crédit
   - Atomicité (transaction)
3. [ ] Email automatique
   - Envoi récap au trésorier
   - PDF borderaux à imprimer
4. [ ] Tests
   - Clôturer session complète
   - Vérifier AccountMove créé
   - Vérifier équilibre
   - Tester rollback si erreur

**Commit** : `feat: implement session closure and AccountMove generation`

**Durée estimée** : 4 heures

---

## 🎯 Phase 3 : Rapprochement bancaire (Sessions 11-13)

### Session 11 : Créer modèle BankTransaction + Import relevés

**Objectif** : Importer et parser les relevés bancaires.

**Tâches :**
1. [ ] Créer modèle `BankTransaction`
   - Enum `TransactionType` (DEPOSIT, WITHDRAWAL, TRANSFER, FEE, DIRECT_DEBIT, CHECK)
   - Champs : account_id, transaction_date, value_date, label, amount, type...
   - Relation : bank_deposit_id, account_move_id
2. [ ] Migration Alembic
3. [ ] Schémas Pydantic
4. [ ] Service `BankImportService`
   - Parser Excel Crédit Agricole
   - Détecter colonnes (date, libellé, débit, crédit)
   - Créer BankTransaction
5. [ ] Endpoint POST `/api/bank-transactions/import`
   - Upload fichier Excel
   - Parsing automatique
   - Retour : nombre lignes importées, erreurs éventuelles
6. [ ] Tests
   - Import relevé test
   - Vérifier création transactions

**Commit** : `feat: add BankTransaction model and import`

**Durée estimée** : 4 heures

---

### Session 12 : Algorithme de rapprochement automatique

**Objectif** : Matcher automatiquement transactions bancaires et dépôts.

**Tâches :**
1. [ ] Service `ReconciliationService`
   - Méthode `match_deposits()`
   - Critères matching :
     - Montant exact
     - Date proche (±3 jours)
     - Libellé contient numéro bordereau
2. [ ] Endpoint POST `/api/reconciliation/auto-match`
   - Lance algorithme
   - Retour : nombre matches, non rapprochés
3. [ ] Détection écarts
   - Comparaison planned_amount vs credited_amount
   - Création alerte si différence
4. [ ] Endpoint GET `/api/reconciliation/status`
   - Dashboard rapprochement
   - Transactions en attente
   - Écarts détectés
5. [ ] Tests
   - Cas normal : match parfait
   - Cas écart : 280€ → 80€ (erreur banque)
   - Cas aucun match

**Commit** : `feat: implement automatic bank reconciliation`

**Durée estimée** : 5 heures

---

### Session 13 : Gestion des écarts et corrections

**Objectif** : Permettre les corrections manuelles et automatiques.

**Tâches :**
1. [ ] Endpoint POST `/api/reconciliation/manual-match`
   - Rapprocher manuellement transaction ↔ dépôt
   - Création AccountMove correction si écart
2. [ ] Service `DiscrepancyService`
   - Création AccountMoveLine "Écart de caisse" (658000)
   - Gestion correction automatique lors régularisation
3. [ ] Endpoint PUT `/api/bank-deposits/{id}/resolve-discrepancy`
   - Marquer écart résolu
   - Annoter explication
4. [ ] Dashboard écarts
   - GET `/api/reconciliation/discrepancies`
   - Liste écarts non résolus
   - Historique résolutions
5. [ ] Tests

**Commit** : `feat: add discrepancy management`

**Durée estimée** : 3 heures

---

## 🎯 Phase 4 : Export et reporting (Sessions 14-16)

### Session 14 : Générateur export Quadratus

**Objectif** : Créer le fichier Excel mensuel pour l'économat.

**Tâches :**
1. [ ] Service `QuadratusExportService`
   - Méthode `generate_monthly_export(month, year)`
   - Récupère tous les AccountMove du mois
   - **SUBSTITUTION INTELLIGENTE** :
     - Détecte AccountMove type ENTRY liés à CountingSession
     - Remplace ligne globale par détail CountingItem
   - Génère fichier Excel
     - Colonnes : Date, Compte, Libellé, Débit, Crédit
     - 1 ligne par AccountMoveLine
     - Vérification équilibre final
2. [ ] Modèle `QuadratusExport` (historique)
   - Champs : month, year, file_path, status, totaux
3. [ ] Endpoint POST `/api/exports/quadratus`
   - Paramètres : month, year
   - Génération fichier
   - Retour : lien téléchargement
4. [ ] Endpoint GET `/api/exports/quadratus`
   - Liste exports historiques
5. [ ] Tests
   - Générer export mois test
   - Vérifier substitution
   - Vérifier équilibre

**Commit** : `feat: implement Quadratus export with intelligent substitution`

**Durée estimée** : 5-6 heures

---

### Session 15 : Gestion quêtes impérées

**Objectif** : Isoler et suivre les quêtes à reverser.

**Tâches :**
1. [ ] Filtre CountingItem `is_impereed=True`
2. [ ] Endpoint GET `/api/counting-items/impereed`
   - Liste quêtes impérées non reversées
   - Totaux par destination
3. [ ] Service `ImpériedService`
   - Création AccountMove reversement
   - Débit Charge reversement (65xxx)
   - Crédit Banque
4. [ ] Endpoint POST `/api/counting-items/{id}/reverse`
   - Marquer reversé
   - Générer AccountMove reversement
5. [ ] Dashboard quêtes impérées
   - En attente de reversement
   - Historique reversements
6. [ ] Rappel automatique (optionnel)
   - Email si reversement non fait après 30 jours
7. [ ] Section dédiée export Quadratus

**Commit** : `feat: add impereed collections management`

**Durée estimée** : 3 heures

---

### Session 16 : Dashboard trésorerie et rapports

**Objectif** : Interfaces de visualisation.

**Tâches :**
1. [ ] Endpoint GET `/api/dashboard/treasury`
   - Soldes actuels comptes
   - Évolution sur 12 mois
   - Totaux recettes/dépenses mois en cours
2. [ ] Endpoint GET `/api/reports/monthly-summary`
   - Récap mensuel détaillé
   - Graphiques (à prévoir pour frontend)
3. [ ] Endpoint GET `/api/reports/by-category`
   - Répartition dépenses/recettes par catégorie
   - Comparaison N vs N-1
4. [ ] Export PDF rapports (optionnel)

**Commit** : `feat: add treasury dashboard and reports`

**Durée estimée** : 4 heures

---

## 🎯 Phase 5 : Modules avancés (Optionnel - Sessions 17+)

### Session 17 : Module Sacrements

**Objectif** : Suivi baptêmes, mariages, obsèques avec casuels.

**Tâches :**
1. [ ] Créer modèle `Sacrament`
   - Enum `SacramentType` (BAPTISM, MARRIAGE, FUNERAL)
   - Champs : date, location, person_name, priest_id, family_contact_id
   - Gestion casuel : expected, received, paid, payment_date
   - Relations : counting_item_id, account_move_id
2. [ ] Migration Alembic
3. [ ] Schémas Pydantic
4. [ ] Router `/api/sacraments`
   - CRUD complet
   - Filtres : type, paid/unpaid, date range
5. [ ] Liaison avec CountingItem
   - Sélecteur lors saisie comptage
   - Mise à jour automatique sacrament.casuel_paid
6. [ ] Dashboard "Casuels en attente"
7. [ ] Tests

**Commit** : `feat: add Sacrament module`

**Durée estimée** : 5 heures

---

### Session 18 : Répartition automatique intelligente

**Objectif** : Suggérer répartition optimale en dépôts.

**Tâches :**
1. [ ] Service `DepositAllocationService`
   - Calcul poids pièces (constantes par valeur)
   - Règle : max 3kg par poche
   - Division automatique euros/centimes si nécessaire
2. [ ] Endpoint GET `/api/counting-sessions/{id}/suggest-allocation`
   - Retourne proposition répartition
   - Utilisateur peut accepter ou modifier
3. [ ] Tests

**Commit** : `feat: add intelligent deposit allocation`

**Durée estimée** : 3 heures

---

### Session 19 : Scan et archivage duplicatas

**Objectif** : Gestion documentaire.

**Tâches :**
1. [ ] Upload PDF duplicata bordereau
   - Endpoint POST `/api/bank-deposits/{id}/upload-slip`
   - Stockage fichier
   - Mise à jour BankDeposit.physical_slip_scanned
2. [ ] Archivage automatique
   - Structure : /archives/{year}/{month}/
3. [ ] Endpoint GET `/api/archives/{year}/{month}`
   - Liste documents du mois
4. [ ] Génération PDF rapports session

**Commit** : `feat: add document archiving`

**Durée estimée** : 3 heures

---

## 📊 Récapitulatif estimations

| Phase | Sessions | Heures estimées | Description |
|-------|----------|-----------------|-------------|
| **Phase 1** | 4 | 12-15h | Refonte architecture (Contact, AccountMove, Account, Category) |
| **Phase 2** | 5 | 15-18h | Workflow comptage complet |
| **Phase 3** | 3 | 12-15h | Rapprochement bancaire |
| **Phase 4** | 3 | 12-15h | Export Quadratus et reporting |
| **Phase 5** | 3+ | 11h+ | Modules optionnels avancés |
| **TOTAL** | 18+ | **62-74h** | MVP complet (hors frontend) |

---

## 🎯 Jalons (Milestones)

### ✅ Milestone 0 : Setup initial (Terminé)
- PostgreSQL + Docker
- FastAPI configuré
- Premiers modèles (Supplier, Category, User, Expense)
- Migrations Alembic

### 🔄 Milestone 1 : Architecture comptable (Phase 1)
**Objectif** : Base solide pour la comptabilité de trésorerie  
**Livrable** : Contact, AccountMove, Account, Category enrichi  
**ETA** : Session prochaine + 3 sessions

### 🎯 Milestone 2 : Workflow comptage (Phase 2)
**Objectif** : Gérer cycle complet comptage → clôture  
**Livrable** : CountingSession, CountingItem, BankDeposit + génération AccountMove  
**ETA** : 5 sessions après Milestone 1

### 🎯 Milestone 3 : Rapprochement bancaire (Phase 3)
**Objectif** : Import et réconciliation automatique  
**Livrable** : BankTransaction, algorithmes matching, gestion écarts  
**ETA** : 3 sessions après Milestone 2

### 🎯 Milestone 4 : Export Quadratus (Phase 4)
**Objectif** : Livrable pour l'économat diocésain  
**Livrable** : Export Excel mensuel avec substitution intelligente  
**ETA** : 3 sessions après Milestone 3

### 🌟 Milestone 5 : MVP Production-Ready
**Objectif** : Version stable utilisable en production  
**Livrable** : MVP complet avec workflow bout-en-bout  
**ETA** : Fin Phase 4

---

## 📅 Planning prévisionnel

**Hypothèse** : 1 session = 2-3 heures de travail effectif

| Période | Milestone | Sessions | Livrable clé |
|---------|-----------|----------|--------------|
| **Semaines 1-2** | Milestone 1 | 1-4 | Architecture comptable |
| **Semaines 3-5** | Milestone 2 | 5-10 | Workflow comptage |
| **Semaines 6-7** | Milestone 3 | 11-13 | Rapprochement bancaire |
| **Semaines 8-9** | Milestone 4 | 14-16 | Export Quadratus |
| **Semaine 10** | Milestone 5 | 17 | MVP Production-Ready |

**Note** : Planning indicatif, ajustable selon disponibilités et imprévus.

---

## 🔮 Vision long terme (Post-MVP)

### Frontend (Phase 6)
- Interface web moderne (React/Vue.js)
- Dashboard temps réel
- Formulaires de saisie comptage
- Interface répartition drag & drop
- Visualisations graphiques

### Authentification & sécurité (Phase 7)
- JWT tokens
- Rôles et permissions (PRIEST, VOLUNTEER, TREASURER, ADMIN)
- Logs d'audit
- Backup automatique

### Intégrations (Phase 8)
- API bancaire (import automatique relevés)
- OCR factures (extraction automatique données)
- Envoi email automatique (SMTP)
- Stockage cloud (Google Drive, Dropbox)

### Mobile (Phase 9)
- Application mobile (Flutter/React Native)
- Saisie comptage sur tablette
- Notifications push

---

**Version roadmap** : 1.0  
**Dernière mise à jour** : 24 octobre 2024  
**Prochaine session** : Migration Supplier → Contact
