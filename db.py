"""
nas/db.py — Initialisation des tables SQLite pour le module NAS
Appeler init_nas_db(db_path) au démarrage de l'application.
"""
import sqlite3


NAS_SCHEMA = """
-- ── Fichiers hébergés ──────────────────────────────────────────
CREATE TABLE IF NOT EXISTS nas_files (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    title             TEXT    NOT NULL,
    filename_original TEXT    NOT NULL,
    filename_stored   TEXT    NOT NULL UNIQUE,
    filepath          TEXT    NOT NULL,
    filesize          INTEGER NOT NULL DEFAULT 0,
    mimetype          TEXT    NOT NULL DEFAULT 'application/octet-stream',
    category          TEXT    NOT NULL DEFAULT 'Général',
    description       TEXT,
    is_public         INTEGER NOT NULL DEFAULT 0,
    download_count    INTEGER NOT NULL DEFAULT 0,
    created_at        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at        DATETIME
);

-- ── Demandes d'accès visiteurs ─────────────────────────────────
CREATE TABLE IF NOT EXISTS nas_access_requests (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    email            TEXT    NOT NULL,
    full_name        TEXT    NOT NULL,
    reason           TEXT,
    requested_files  TEXT    DEFAULT '[]',   -- JSON array of file ids
    status           TEXT    NOT NULL DEFAULT 'pending',  -- pending/approved/rejected/revoked
    token            TEXT    UNIQUE,
    token_expires_at DATETIME,
    token_used_count INTEGER NOT NULL DEFAULT 0,
    token_max_uses   INTEGER NOT NULL DEFAULT -1,  -- -1 = illimité
    allowed_files    TEXT    DEFAULT '[]',   -- JSON array of file ids autorisés
    admin_note       TEXT,
    ip_address       TEXT,
    created_at       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    approved_at      DATETIME
);

-- ── Logs d'accès ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS nas_access_logs (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id  INTEGER NOT NULL REFERENCES nas_access_requests(id),
    file_id     INTEGER REFERENCES nas_files(id),
    action      TEXT    NOT NULL DEFAULT 'view',  -- view/download
    ip_address  TEXT,
    user_agent  TEXT,
    accessed_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def init_nas_db(db_path: str) -> None:
    """Crée les tables NAS si elles n'existent pas encore."""
    conn = sqlite3.connect(db_path)
    conn.executescript(NAS_SCHEMA)
    conn.commit()
    conn.close()
