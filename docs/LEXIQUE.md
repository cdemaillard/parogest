# 📚 Lexique complet du projet ParoGest

## 🎯 Vue d'ensemble

ParoGest est un logiciel de **comptabilité de trésorerie** dédié aux paroisses catholiques françaises. Il couvre le cycle complet : comptage des espèces → dépôt bancaire → rapprochement → export comptable diocésain.

---

## 🏗️ Modèles de données (Objets métier)

### 📁 **1. GESTION DES TIERS**

#### **Contact**
*Ancien nom : Supplier (en cours de migration)*

Représente toute personne physique ou morale en relation avec la paroisse.

**Champs principaux :**
- `id` : Identifiant unique
- `contact_type` : Type de contact (enum)
  - `SUPPLIER` : Fournisseur (EDF, plombier, organiste...)
  - `DONOR` : Fidèle donateur
  - `VOLUNTEER` : Bénévole (comptage, secrétariat...)
  - `PRIEST` : Prêtre (curé, vicaire, diacre)
  - `DIOCESE` : Économat diocésain
  - `OTHER` : Autre
- `is_company` : Personne morale (True) ou physique (False)
- `name` : Nom complet
- `display_name` : Nom d'affichage ("Abbé Martin" au lieu de "Martin Jean")
- `email`, `phone`, `mobile` : Coordonnées
- `street`, `street2`, `zip_code`, `city`, `country` : Adresse postale
- `siret`, `vat_number` : Informations légales (fournisseurs)
- `is_donor` : Est un donateur régulier
- `anonymize_donation` : Don anonyme (True/False)
- `ministry_role` : Fonction ecclésiastique ("Curé", "Vicaire", "Diacre")
- `ordination_date` : Date d'ordination (pour prêtres)
- `volunteer_skills` : Compétences bénévole (JSON : `{"comptage": true, "secrétariat": true}`)
- `bank_name`, `iban`, `bic` : Coordonnées bancaires (pour remboursements)
- `active` : Contact actif/archivé
- `created_at`, `updated_at` : Métadonnées

**Relations :**
- `account_moves` : Liste des mouvements comptables liés
- `counting_items` : Items comptés par ce bénévole (si VOLUNTEER)

**Cas d'usage :**
- Fournisseurs : émission factures, paiements
- Donateurs : traçabilité dons
- Prêtres/bénévoles : remboursement notes de frais, suivi comptages

**Note** : Les reçus fiscaux pour les dons formalisés (denier de l'Église) sont gérés par le diocèse, pas par la paroisse.

---

### 💰 **2. COMPTABILITÉ DE TRÉSORERIE**

#### **Account**
Représente un compte bancaire ou une caisse physique.

**Champs principaux :**
- `id` : Identifiant unique
- `name` : Libellé ("Compte courant Crédit Agricole", "Caisse espèces presbytère")
- `account_type` : Type de compte (enum)
  - `BANK` : Compte bancaire
  - `CASH` : Caisse espèces
  - `SAVINGS` : Compte épargne
- `bank_name` : Nom de la banque (si type BANK)
- `iban` : IBAN (si type BANK)
- `opening_balance` : Solde d'ouverture (au 1er janvier)
- `current_balance` : Solde actuel (calculé dynamiquement)
- `currency` : Devise (défaut "EUR")
- `active` : Compte actif/clôturé

**Relations :**
- `account_moves` : Mouvements comptables passant par ce compte
- `bank_transactions` : Transactions du relevé bancaire

**Cas d'usage :**
- Suivi soldes en temps réel
- Rapprochement bancaire
- Tableau de bord trésorerie

---

#### **Category**
Plan comptable simplifié adapté aux paroisses (fourni par le diocèse).

**Champs principaux :**
- `id` : Identifiant unique
- `code` : Code comptable ("70100", "60610", "62510"...)
- `name` : Libellé ("Quêtes ordinaires", "Électricité", "Frais déplacement")
- `category_type` : Type (enum)
  - `INCOME` : Produit/recette
  - `EXPENSE` : Charge/dépense
- `parent_id` : Catégorie parente (pour hiérarchie)
- `active` : Catégorie active

**Relations :**
- `account_move_lines` : Lignes comptables utilisant cette catégorie
- `subcategories` : Sous-catégories (ex: 606 → 60610, 60620...)

**Exemples de codes :**
- `70100` : Quêtes ordinaires (dominicales + semaine)
- `70120` : Quêtes de casuels (obsèques, mariages, baptêmes)
- `70130` : Troncs
- `70200` : Offrandes de messes
- `70300` : Casuels (baptêmes, mariages, obsèques)
- `60610` : Électricité
- `60620` : Chauffage
- `62510` : Frais de déplacement

---

#### **AccountMove**
Mouvement comptable (écriture). C'est le **document comptable central**.

**Champs principaux :**
- `id` : Identifiant unique
- `name` : Numéro de pièce (auto-généré : "COMPT-20241018", "FACT-2024-042")
- `move_type` : Type de mouvement (enum)
  - `ENTRY` : Pièce comptable générique (utilisé pour comptages)
  - `IN_INVOICE` : Facture fournisseur
  - `IN_REFUND` : Avoir fournisseur (remboursement)
  - `BANK_TRANSFER` : Virement interne (caisse → banque)
- `state` : État (enum)
  - `DRAFT` : Brouillon
  - `POSTED` : Comptabilisé (validé)
  - `CANCELLED` : Annulé
- `date` : Date comptable
- `partner_id` : Contact lié (fournisseur, donateur, prêtre)
- `ref` : Référence externe (n° facture fournisseur, n° chèque...)
- `amount_total` : Montant total (calculé depuis les lignes)
- `payment_method` : Mode de paiement ("cash", "check", "transfer", "card")
- `account_id` : Compte bancaire/caisse utilisé
- `counting_session_id` : Session de comptage (si type ENTRY pour recettes)
- `is_reconciled` : Rapproché avec relevé bancaire
- `notes` : Commentaires libres

**Relations :**
- `lines` : Lignes comptables (débit/crédit) - **1 à N**
- `partner` : Contact lié
- `account` : Compte bancaire/caisse
- `counting_session` : Session de comptage d'origine
- `bank_transaction` : Transaction bancaire rapprochée

**Principe comptable :**
Chaque AccountMove contient au minimum 2 lignes (débit/crédit) dont le total doit s'équilibrer (∑ débits = ∑ crédits).

**Exemple - Comptage :**
```
AccountMove "COMPT-20241018" (type=ENTRY)
├─ Line 1: Débit Caisse (53000) +2.437,35€
├─ Line 2: Crédit Quêtes ordinaires (70100) -1.450€
├─ Line 3: Crédit Casuels (70300) -320€
└─ Line 4: Crédit Troncs (70130) -287,35€
```

**Exemple - Facture fournisseur :**
```
AccountMove "FACT-2024-042" (type=IN_INVOICE)
├─ Line 1: Débit Électricité (60610) +245,80€
└─ Line 2: Crédit Banque (51200) -245,80€
```

---

#### **AccountMoveLine**
Ligne d'écriture comptable (débit ou crédit).

**Champs principaux :**
- `id` : Identifiant unique
- `move_id` : AccountMove parent
- `account_code` : Code du compte comptable ("70100", "53000"...)
- `account_name` : Libellé du compte (cache, pour performance)
- `name` : Libellé de la ligne ("Quête dominicale St-Pierre")
- `debit` : Montant au débit (0 si crédit)
- `credit` : Montant au crédit (0 si débit)
- `sequence` : Ordre d'affichage
- `counting_item_id` : Lien vers l'item de comptage d'origine (traçabilité)

**Relations :**
- `move` : AccountMove parent
- `counting_item` : Item de comptage source (si applicable)

**Règle d'or :**
Dans un AccountMove, ∑ débits = ∑ crédits (équilibre obligatoire)

---

### 📊 **3. WORKFLOW COMPTAGE**

#### **CountingSession**
Séance hebdomadaire de comptage des espèces (typiquement jeudi ou vendredi).

**Champs principaux :**
- `id` : Identifiant unique
- `date` : Date de la séance
- `status` : État (enum)
  - `DRAFT` : En cours de saisie
  - `COMPLETED` : Comptage terminé (pas encore clôturée)
  - `CLOSED` : Clôturée (écritures comptables générées)
- `counted_by` : Participants ("Marie Dubois + Jeanne Martin")
- `notes` : Remarques éventuelles
- `total_coins` : Total pièces compté
- `total_bills` : Total billets compté
- `total_checks` : Total chèques compté
- `total_amount` : Montant global de la session
- `created_at`, `updated_at` : Métadonnées

**Relations :**
- `items` : Liste des items comptés (quêtes, troncs, casuels...) - **1 à N**
- `deposits` : Borderaux de dépôt préparés - **1 à N**
- `account_move` : Écriture comptable générée à la clôture - **1 à 1**

**Workflow :**
1. Création session (DRAFT)
2. Comptage des items un par un
3. Validation → COMPLETED
4. Répartition en dépôts bancaires
5. Clôture → CLOSED (génération AccountMove type ENTRY)

---

#### **CountingItem**
Un élément compté lors d'une session (= un "sac" physique ou une enveloppe).

**Champs principaux :**
- `id` : Identifiant unique
- `counting_session_id` : Session parente
- `collection_type` : Type de collecte (enum)
  - `QUETE_DOMINICALE` : Quête messe dominicale
  - `QUETE_SEMAINE` : Quête messe de semaine
  - `QUETE_CASUEL` : Quête lors casuel (obsèque, mariage, baptême)
  - `TRONC` : Tronc d'église
  - `OFFRANDE_MESSE` : Offrande/intention de messe
  - `CASUEL_BAPTEME` : Casuel de baptême
  - `CASUEL_MARIAGE` : Casuel de mariage
  - `CASUEL_OBSEQUE` : Casuel d'obsèque
  - `DON_ORDINAIRE` : Don ponctuel
  - `DON_CHEQUE` : Don par chèque nominatif
- `location` : Lieu de collecte ("Église St-Pierre", "Chapelle ND Lourdes")
- `event_date` : Date de l'événement (pas du comptage !)
- `event_label` : Description ("Messe 10h30", "Obsèques M. Dupont")
- `coins_detail` : Détail pièces (JSON : `{"2€": 45, "1€": 23, "0.50€": 12}`)
- `bills_detail` : Détail billets (JSON : `{"50€": 2, "20€": 5}`)
- `checks_detail` : Détail chèques (JSON : `[{"number": "1234567", "amount": 50, "bank": "BNP"}]`)
- `coins_total` : Total pièces
- `bills_total` : Total billets
- `checks_total` : Total chèques
- `total_amount` : Montant global de l'item
- `is_impereed` : Quête impérée (à reverser au diocèse/œuvre)
- `impereed_destination` : Destination du reversement ("Diocèse", "Œuvre d'Orient", "Séminaire")
- `accounting_code` : Code comptable suggéré (70100, 70120...)

**Relations :**
- `counting_session` : Session parente
- `deposits` : Borderaux dans lesquels cet item est réparti (many-to-many)
- `account_move_line` : Ligne comptable générée à la clôture

**Cas d'usage :**
- Saisie détaillée lors du comptage
- Traçabilité événementielle (quel événement a rapporté combien)
- Génération automatique des lignes comptables

---

#### **BankDeposit**
Bordereau de dépôt bancaire (poche espèces ou enveloppe chèques).

**Champs principaux :**
- `id` : Identifiant unique
- `counting_session_id` : Session d'origine
- `deposit_number` : Numéro bordereau (manuscrit sur la poche : "20241018-001")
- `deposit_date` : Date de dépôt physique à la banque
- `deposit_type` : Type (enum)
  - `COINS` : Poche pièces
  - `BILLS` : Poche billets
  - `CHECKS` : Enveloppe chèques
- `planned_amount` : Montant inscrit sur le bordereau
- `credited_amount` : Montant réellement crédité par la banque (peut différer)
- `bank_credit_date` : Date crédit effectif sur le compte
- `has_discrepancy` : Écart détecté entre prévu/réel
- `discrepancy_amount` : Montant de l'écart
- `discrepancy_notes` : Explication ("Erreur lecture banque : 280€ → 80€")
- `physical_slip_scanned` : Chemin PDF du duplicata scanné

**Relations :**
- `counting_session` : Session d'origine
- `items` : Items comptés inclus dans ce dépôt (many-to-many via table de liaison)
- `bank_transaction` : Transaction bancaire correspondante (après crédit)

**Workflow :**
1. Création lors de la répartition (après comptage)
2. Remplissage bordereau papier (duplicata carbone)
3. Dépôt physique à la banque
4. Attente crédit (1-3 jours)
5. Rapprochement avec BankTransaction

---

### 🏦 **4. RAPPROCHEMENT BANCAIRE**

#### **BankTransaction**
Ligne du relevé bancaire importé.

**Champs principaux :**
- `id` : Identifiant unique
- `account_id` : Compte bancaire
- `transaction_date` : Date opération
- `value_date` : Date valeur
- `label` : Libellé banque ("DEPOT ESPECES 20241018-001", "VIR EDF")
- `amount` : Montant (positif=crédit, négatif=débit)
- `transaction_type` : Type (enum)
  - `DEPOSIT` : Dépôt espèces/chèques
  - `WITHDRAWAL` : Retrait
  - `TRANSFER` : Virement
  - `FEE` : Frais bancaires
  - `DIRECT_DEBIT` : Prélèvement
  - `CHECK` : Chèque émis
- `is_reconciled` : Rapproché avec un AccountMove
- `account_move_id` : AccountMove correspondant (après rapprochement)
- `bank_deposit_id` : Bordereau de dépôt correspondant (si type DEPOSIT)

**Relations :**
- `account` : Compte bancaire
- `account_move` : Écriture comptable rapprochée
- `bank_deposit` : Dépôt d'origine (si applicable)

**Workflow :**
1. Import fichier Excel relevé bancaire mensuel
2. Parsing automatique → création BankTransaction
3. Algorithme de rapprochement automatique
4. Validation manuelle si écarts

---

### 📄 **5. EXPORTS & REPORTING**

#### **QuadratusExport**
Export comptable mensuel vers le logiciel diocésain.

**Champs principaux :**
- `id` : Identifiant unique
- `month` : Mois concerné
- `year` : Année
- `generated_at` : Date génération
- `file_path` : Chemin du fichier Excel généré
- `total_income` : Total recettes du mois
- `total_expense` : Total dépenses du mois
- `status` : État (enum)
  - `DRAFT` : Brouillon
  - `SENT` : Envoyé à l'économat
  - `VALIDATED` : Validé par l'économat

**Relations :**
- `account_moves` : Liste des AccountMove inclus dans l'export

**Contenu du fichier :**
Format Excel compatible import direct Quadratus, avec **substitution intelligente** : les dépôts bancaires agrégés sont remplacés par le détail d'origine (par nature comptable).

---

### 🙏 **6. MODULE SACREMENTS (Phase 2 - Optionnel)**

#### **Sacrament**
Suivi des sacrements (baptêmes, mariages, obsèques) avec gestion des casuels.

**Champs principaux :**
- `id` : Identifiant unique
- `sacrament_type` : Type (enum)
  - `BAPTISM` : Baptême
  - `MARRIAGE` : Mariage
  - `FUNERAL` : Obsèques
- `date` : Date de célébration
- `location` : Lieu ("Église St-Pierre")
- `person_name` : Nom principal (défunt, baptisé, époux)
- `person_name_2` : 2e époux (pour mariages)
- `family_contact_id` : Contact de la famille
- `priest_id` : Prêtre célébrant
- `casuel_expected` : Montant habituel du casuel
- `casuel_received` : Montant réellement reçu
- `casuel_paid` : Casuel payé (True/False)
- `payment_date` : Date paiement
- `counting_item_id` : Lien vers item de comptage (si payé)
- `account_move_id` : Lien vers écriture comptable
- `notes` : Remarques

**Relations :**
- `family_contact` : Contact de la famille
- `priest` : Prêtre célébrant
- `counting_item` : Item de comptage correspondant

**Cas d'usage :**
- Suivi des sacrements à venir
- Traçabilité des casuels
- Liaison automatique comptage ↔ sacrement
- Dashboard "casuels en attente de paiement"

---

## 🔗 Relations clés entre modèles

```
CountingSession
    ├─→ CountingItem (1-N)
    │       ├─→ AccountMoveLine (1-1) via account_move
    │       └─→ Sacrament (0-1) optionnel
    │
    ├─→ BankDeposit (1-N)
    │       ├─→ CountingItem (N-N) via table de liaison
    │       └─→ BankTransaction (1-1)
    │
    └─→ AccountMove (1-1) type ENTRY
            └─→ AccountMoveLine (1-N)

Contact
    ├─→ AccountMove (1-N) [en tant que partner]
    └─→ CountingSession (1-N) [en tant que counted_by]

Account
    ├─→ AccountMove (1-N)
    └─→ BankTransaction (1-N)
```

---

## 📖 Glossaire des termes métier

### **Comptabilité**
- **Comptabilité de trésorerie** : On enregistre uniquement les **flux réels d'argent** (quand l'argent entre/sort effectivement), pas les créances/dettes
- **Débit** : Augmentation d'un compte d'actif ou diminution d'un compte de passif (en simplifié : l'argent "entre")
- **Crédit** : Augmentation d'un compte de passif ou diminution d'un compte d'actif (en simplifié : l'argent "sort")
- **Équilibrage** : Dans chaque AccountMove, ∑ débits = ∑ crédits (règle d'or de la comptabilité en partie double)
- **Plan comptable** : Liste structurée des comptes (codes à 5 chiffres : 70xxx = produits, 60xxx = charges)

### **Paroisse**
- **Quête** : Collecte d'argent lors des messes (paniers passés dans l'assemblée)
- **Quête dominicale** : Quête du dimanche (la plus importante)
- **Quête de semaine** : Quête lors des messes en semaine
- **Quête impérée** : Quête dont le produit doit être reversé (diocèse, œuvres missionnaires...). "Impérée" = ordonnée par l'évêque
- **Tronc** : Boîte à offrandes fixe dans l'église (cierges, intentions...)
- **Casuel** : Offrande versée à l'occasion d'un sacrement (baptême, mariage, obsèques)
- **Offrande de messe** : Don pour faire célébrer une messe pour une intention particulière (défunt, anniversaire...)
- **Intention de messe** : Demande de célébration d'une messe (accompagnée d'une offrande)
- **Denier de l'Église** : Don formalisé annuel des fidèles au diocèse (génère reçu fiscal, géré par le diocèse)
- **Économat diocésain** : Service comptable central du diocèse (supervision finances paroisses)
- **Curé** : Prêtre responsable de la paroisse
- **Vicaire** : Prêtre assistant le curé
- **Diacre** : Ministre ordonné (niveau inférieur au prêtre)

### **Banque**
- **Bordereau de dépôt** : Document papier accompagnant un dépôt d'espèces/chèques (duplicata carbone conservé comme justificatif)
- **Poche** : Sachet fourni par la banque pour déposer les espèces (avec bordereau pré-imprimé)
- **Remise de chèques** : Enveloppe dédiée au dépôt de chèques (avec bordereau listant les chèques)
- **Crédit** : Opération bancaire ajoutant de l'argent sur le compte
- **Débit** : Opération bancaire retirant de l'argent du compte
- **Rapprochement bancaire** : Vérification que les écritures comptables correspondent aux opérations du relevé bancaire
- **Écart de caisse** : Différence entre montant attendu et montant réel (erreur comptage ou erreur banque)

### **Workflow ParoGest**
- **Session de comptage** : Réunion hebdomadaire (jeudi/vendredi) où on compte tous les sacs de la semaine
- **Comptage** : Action de compter le contenu d'un sac (pièces, billets, chèques)
- **Répartition** : Phase où on décide comment regrouper les espèces comptées dans les poches/enveloppes de dépôt
- **Clôture** : Validation finale d'une session → génération des écritures comptables (AccountMove)
- **Substitution** : Processus qui remplace les lignes bancaires agrégées ("DEPOT 800€") par les détails d'origine ("Quête St-Pierre 320€ + Quête ND 180€...")
- **Export Quadratus** : Fichier Excel mensuel envoyé à l'économat diocésain (format compatible import logiciel Quadratus)

---

## 🎯 Acronymes & conventions

- **CA** : Crédit Agricole (banque)
- **IBAN** : International Bank Account Number (coordonnées bancaires)
- **BIC** : Bank Identifier Code (code banque)
- **SIRET** : Numéro identification entreprise française (14 chiffres)
- **TVA** : Taxe sur la valeur ajoutée
- **JSON** : Format de stockage de données structurées (pour détails pièces/billets)
- **PDF** : Format de document (pour borderaux, rapports)
- **XLSX** : Format Excel (relevés bancaires, export Quadratus)
- **ORM** : Object-Relational Mapping (SQLAlchemy)
- **CRUD** : Create, Read, Update, Delete

---

## 🎓 Règles métier importantes

### **Comptage**
1. Une session de comptage génère **UN SEUL** AccountMove (type ENTRY)
2. Chaque CountingItem génère **UNE** AccountMoveLine dans cet AccountMove
3. Les items sont comptés avec leur date d'événement réelle (pas date comptage)
4. Le total compté DOIT égaler le total déposé DOIT égaler le total crédité

### **Dépôts bancaires**
1. Un CountingItem peut être réparti sur **plusieurs** BankDeposit (si trop volumineux)
2. Un BankDeposit peut contenir **plusieurs** CountingItem (regroupement)
3. Le numéro de bordereau est manuscrit sur la poche physique (duplicata carbone conservé)

### **Rapprochement**
1. Une BankTransaction de type DEPOSIT doit correspondre à un BankDeposit
2. Si écart détecté : imputation temporaire en compte "Écart de caisse" (658000)
3. Correction automatique lors de la régularisation bancaire (mois suivant)

### **Export Quadratus**
1. Les lignes de dépôt bancaire sont **substituées** par les détails d'origine
2. Format : 1 ligne par AccountMoveLine (débit/crédit)
3. Équilibre vérifié : ∑ débits = ∑ crédits
4. Fichier Excel conforme format import Quadratus

### **Quêtes impérées**
1. Marquage spécial `is_impereed=True` sur le CountingItem
2. Génération automatique d'un AccountMove de reversement
3. Isolation dans l'export Quadratus (section dédiée)
4. Rappel automatique si non reversé après 30 jours

---

## 📊 Types d'AccountMove (simplifiés)

| Type | Code | Usage | Exemple |
|------|------|-------|---------|
| **ENTRY** | `entry` | Pièce comptable générique | Session de comptage, opérations diverses |
| **IN_INVOICE** | `in_invoice` | Facture fournisseur | Facture EDF, plombier, organiste |
| **IN_REFUND** | `in_refund` | Avoir fournisseur | Remboursement par fournisseur |
| **BANK_TRANSFER** | `bank_transfer` | Virement interne | Transfert caisse → banque |

**Note** : Cette liste minimaliste permet de couvrir tous les besoins. Les détails sont portés par les codes comptables (Category.code), pas par le type d'AccountMove.

---

## 🔄 Workflow complet : Du comptage à l'export

### **1. Séance de comptage (Jeudi/Vendredi)**
```
Création CountingSession
    ↓
Comptage de chaque sac (CountingItem)
    - Pièces par valeur
    - Billets par valeur
    - Chèques individuels
    ↓
Validation des totaux
    ↓
Status: COMPLETED
```

### **2. Répartition en dépôts**
```
Interface de répartition
    ↓
Création BankDeposit (poches/enveloppes)
    - Regrouper ou diviser les items
    - Numérotation borderaux
    ↓
Impression borderaux
    ↓
Clôture session
    ↓
Status: CLOSED
    ↓
Génération AccountMove (type ENTRY)
    - 1 ligne débit caisse (total)
    - N lignes crédit produits (par item)
```

### **3. Dépôt physique banque (J+1 à J+3)**
```
Dépôt poches/enveloppes au Crédit Agricole
    ↓
Conservation duplicatas carbone
    ↓
Attente crédit bancaire (1-3 jours)
    ↓
Banque crédite le compte
```

### **4. Import relevé bancaire (Fin de mois)**
```
Export Excel depuis espace client CA
    ↓
Upload dans ParoGest
    ↓
Parsing automatique
    ↓
Création BankTransaction
```

### **5. Rapprochement automatique**
```
Algorithme de matching
    ↓
BankTransaction.DEPOSIT ↔ BankDeposit
    ↓
Vérification totaux
    ↓
Détection écarts éventuels
    ↓
Validation ou correction manuelle
```

### **6. Export Quadratus (Fin de mois)**
```
Génération fichier Excel
    ↓
SUBSTITUTION INTELLIGENTE:
    Ligne banque "DEPOT 800€"
        ↓ remplacée par
    - Quête St-Pierre 70100: 320€
    - Quête ND Lourdes 70100: 180€
    - Tronc St-Pierre 70130: 150€
    - Offrandes messes 70200: 150€
    ↓
Envoi email économat diocèse
```

---

## 🚀 Points clés de l'architecture

1. **Traçabilité totale** : Chaque euro collecté est traçable depuis le sac physique jusqu'à l'écriture comptable finale
2. **Substitution intelligente** : Les dépôts bancaires agrégés sont "éclatés" en détail par nature comptable
3. **Automatisation maximale** : Calculs, suggestions, rapprochement, génération documents, notifications
4. **Conformité diocésaine** : Export direct compatible Quadratus sans retraitement manuel
5. **Simplicité d'usage** : Interface adaptée aux utilisateurs peu formés à la comptabilité

---

**Version du lexique** : 1.0  
**Dernière mise à jour** : 24 octobre 2024  
**Statut** : Architecture validée, implémentation en cours (Phase 1)
