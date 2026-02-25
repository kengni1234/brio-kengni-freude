-- ══════════════════════════════════════════════════════════════
-- Script de correction de la base de données Kengni Finance
-- Problème: type 'epargne' non accepté dans financial_transactions
-- ══════════════════════════════════════════════════════════════

-- ÉTAPE 1: Créer une nouvelle table avec le bon CHECK constraint
CREATE TABLE IF NOT EXISTS financial_transactions_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('revenue', 'expense', 'receivable', 'credit', 'debt', 'investment', 'epargne')),
    category TEXT NOT NULL,
    subcategory TEXT,
    reason TEXT NOT NULL,
    usage TEXT,
    amount REAL NOT NULL,
    currency TEXT DEFAULT 'EUR',
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    payment_method TEXT,
    reference TEXT,
    status TEXT DEFAULT 'completed' CHECK(status IN ('completed', 'pending', 'cancelled')),
    notes TEXT,
    tags TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- ÉTAPE 2: Copier les données existantes
INSERT INTO financial_transactions_new 
SELECT * FROM financial_transactions;

-- ÉTAPE 3: Supprimer l'ancienne table
DROP TABLE financial_transactions;

-- ÉTAPE 4: Renommer la nouvelle table
ALTER TABLE financial_transactions_new RENAME TO financial_transactions;

-- ✅ Base de données corrigée!
