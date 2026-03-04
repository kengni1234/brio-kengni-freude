#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════
  KENGNI FINANCE — MODULE BOUTIQUE DOCUMENTS TRADING
  documents_store.py — v1.0
═══════════════════════════════════════════════════════════════════════
"""

import os, json, secrets, time
from datetime import datetime, timedelta
from functools import wraps

from flask import (
    Blueprint, render_template, request, jsonify,
    session, redirect, url_for, send_file, abort
)
from werkzeug.utils import secure_filename
import sqlite3

# ── Blueprint ──────────────────────────────────────────────────────────────
documents_bp = Blueprint('documents', __name__, url_prefix='/documents',
                         template_folder='templates')

# ── Config ─────────────────────────────────────────────────────────────────
DB_FILE        = os.environ.get('DB_PATH', 'kengni_finance.db')
UPLOAD_DOCS    = 'static/uploads/docs'
ALLOWED_DOCS   = {'pdf','xlsx','xls','docx','doc','zip','rar','mp4','mp3','pptx','png','jpg','jpeg','gif','webp'}
TOKEN_VALIDITY = int(os.environ.get('DOC_TOKEN_MINUTES', 10))
SESSION_HOURS  = int(os.environ.get('DOC_SESSION_HOURS', 24))

GMAIL = {
    'sender':   os.environ.get('GMAIL_SENDER', 'fabrice.kengni12@gmail.com'),
    'name':     'Kengni Finance — Boutique',
    'host':     'smtp.gmail.com',
    'port':     587,
    'password': os.environ.get('GMAIL_APP_PASSWORD', ''),
}

os.makedirs(UPLOAD_DOCS, exist_ok=True)

# ── Helpers DB ──────────────────────────────────────────────────────────────
def _db():
    conn = sqlite3.connect(DB_FILE, timeout=30, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=30000;")
    return conn

def _unread_notifications(user_id: int) -> int:
    try:
        conn = _db()
        c    = conn.cursor()
        c.execute("SELECT COUNT(*) as cnt FROM notifications WHERE user_id=? AND is_read=0", (user_id,))
        cnt  = c.fetchone()['cnt']
        conn.close()
        return cnt
    except Exception:
        return 0

def init_documents_db():
    """Crée les tables nécessaires. Idempotent."""
    conn = _db()
    c    = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS trading_documents (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        title         TEXT    NOT NULL,
        description   TEXT,
        file_path     TEXT,
        file_url      TEXT,
        link_url      TEXT,
        link_label    TEXT    DEFAULT 'Ouvrir le lien',
        doc_type      TEXT    NOT NULL DEFAULT 'file'
                      CHECK(doc_type IN ('file','link','both')),
        category      TEXT    NOT NULL DEFAULT 'Général',
        tags          TEXT    DEFAULT '[]',
        price         REAL    DEFAULT 0,
        currency      TEXT    DEFAULT 'XAF',
        is_free       INTEGER DEFAULT 1,
        is_published  INTEGER DEFAULT 1,
        thumbnail_url TEXT,
        downloads     INTEGER DEFAULT 0,
        views         INTEGER DEFAULT 0,
        created_by    INTEGER,
        created_at    TEXT    DEFAULT (datetime('now')),
        updated_at    TEXT    DEFAULT (datetime('now')),
        FOREIGN KEY(created_by) REFERENCES users(id)
    )''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS doc_access_tokens (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        email       TEXT    NOT NULL,
        username    TEXT    NOT NULL,
        token       TEXT    NOT NULL UNIQUE,
        expires_at  TEXT    NOT NULL,
        used        INTEGER DEFAULT 0,
        used_at     TEXT,
        ip          TEXT,
        created_at  TEXT    DEFAULT (datetime('now'))
    )''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS doc_sessions (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        session_key TEXT    NOT NULL UNIQUE,
        email       TEXT    NOT NULL,
        username    TEXT    NOT NULL,
        token_id    INTEGER,
        expires_at  TEXT    NOT NULL,
        ip          TEXT,
        created_at  TEXT    DEFAULT (datetime('now')),
        FOREIGN KEY(token_id) REFERENCES doc_access_tokens(id)
    )''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS doc_purchases (
        id             INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id    INTEGER NOT NULL,
        email          TEXT    NOT NULL,
        username       TEXT    NOT NULL,
        amount         REAL    DEFAULT 0,
        currency       TEXT    DEFAULT 'XAF',
        status         TEXT    DEFAULT 'pending'
                       CHECK(status IN ('pending','confirmed','rejected')),
        payment_method TEXT,
        payment_ref    TEXT,
        confirmed_by   INTEGER,
        confirmed_at   TEXT,
        notes          TEXT,
        created_at     TEXT    DEFAULT (datetime('now')),
        FOREIGN KEY(document_id) REFERENCES trading_documents(id)
    )''')

    try:
        c.execute("ALTER TABLE users ADD COLUMN allowed_pages TEXT DEFAULT NULL")
    except Exception:
        pass

    conn.commit()
    conn.close()
    print("✅  Documents Store DB initialisé")


# ═══════════════════════════════════════════════════════════════
#  DÉCORATEURS ACCÈS
# ═══════════════════════════════════════════════════════════════

def _get_doc_session():
    sk = session.get('doc_session_key')
    if not sk:
        return None
    conn = _db()
    c    = conn.cursor()
    c.execute("SELECT * FROM doc_sessions WHERE session_key=? AND expires_at > datetime('now')", (sk,))
    row  = c.fetchone()
    conn.close()
    return dict(row) if row else None

def doc_access_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('role') in ('admin','superadmin') and session.get('user_id'):
            return f(*args, **kwargs)
        if _get_doc_session():
            return f(*args, **kwargs)
        return redirect(url_for('documents.access_page'))
    return decorated

def admin_only_doc(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('role') not in ('admin','superadmin'):
            return jsonify({'success': False, 'error': 'Accès admin requis'}), 403
        return f(*args, **kwargs)
    return decorated


# ═══════════════════════════════════════════════════════════════
#  ACCÈS — PAGE DE DEMANDE & VÉRIFICATION TOKEN
# ═══════════════════════════════════════════════════════════════

@documents_bp.route('/access', methods=['GET'])
def access_page():
    if session.get('role') in ('admin','superadmin') and session.get('user_id'):
        return redirect(url_for('documents.store'))
    if _get_doc_session():
        return redirect(url_for('documents.store'))
    return render_template('document_access.html', token_minutes=TOKEN_VALIDITY)

@documents_bp.route('/access/request', methods=['POST'])
def request_access():
    data     = request.get_json(force=True, silent=True) or request.form
    email    = str(data.get('email', '')).strip().lower()
    username = str(data.get('username', '')).strip()

    if not email or '@' not in email:
        return jsonify({'success': False, 'error': 'Email invalide'}), 400
    if not username or len(username) < 2:
        return jsonify({'success': False, 'error': 'Identifiant trop court (min 2 car.)'}), 400

    if os.environ.get('DOC_CHECK_USER', '0') == '1':
        conn = _db()
        c    = conn.cursor()
        c.execute("SELECT id FROM users WHERE LOWER(email)=? AND username=? AND status='active'",
                  (email, username))
        if not c.fetchone():
            conn.close()
            return jsonify({'success': False,
                            'error': 'Aucun compte actif trouvé avec ces identifiants.'}), 404
        conn.close()

    conn = _db()
    c    = conn.cursor()
    c.execute("DELETE FROM doc_access_tokens WHERE email=? AND used=0 AND expires_at<=datetime('now')", (email,))
    c.execute("SELECT COUNT(*) as cnt FROM doc_access_tokens WHERE email=? AND created_at>=datetime('now','-1 hour')", (email,))
    if c.fetchone()['cnt'] >= 3:
        conn.close()
        return jsonify({'success': False, 'error': 'Trop de demandes. Attendez 1 heure.'}), 429

    token      = str(secrets.randbelow(1_000_000)).zfill(6)
    expires_at = (datetime.now() + timedelta(minutes=TOKEN_VALIDITY)).isoformat()
    ip         = request.headers.get('X-Forwarded-For', request.remote_addr or '')[:60]

    c.execute("INSERT INTO doc_access_tokens (email,username,token,expires_at,ip) VALUES (?,?,?,?,?)",
              (email, username, token, expires_at, ip))
    token_id = c.lastrowid
    conn.commit()
    conn.close()

    sent = _send_access_email(email, username, token)
    if not sent:
        if os.environ.get('FLASK_DEBUG') == '1':
            session['doc_pending_token_id'] = token_id
            session['doc_pending_email']    = email
            session['doc_pending_username'] = username
            return jsonify({'success': True, 'debug_token': token,
                            'message': f'[DEV] Token : {token}'})
        return jsonify({'success': False,
                        'error': 'Erreur d\'envoi email. Vérifiez la config GMAIL_APP_PASSWORD.'}), 500

    session['doc_pending_token_id'] = token_id
    session['doc_pending_email']    = email
    session['doc_pending_username'] = username
    return jsonify({'success': True,
                    'message': f'Code envoyé à {email}. Valable {TOKEN_VALIDITY} min.'})

@documents_bp.route('/access/verify', methods=['POST'])
def verify_access():
    data  = request.get_json(force=True, silent=True) or request.form
    token = str(data.get('token', '')).strip()

    email    = session.get('doc_pending_email', '')
    username = session.get('doc_pending_username', '')
    tid      = session.get('doc_pending_token_id')

    if not email or not tid:
        return jsonify({'success': False, 'error': 'Session expirée. Recommencez.'}), 400

    conn = _db()
    c    = conn.cursor()
    c.execute("SELECT * FROM doc_access_tokens WHERE id=? AND email=? AND used=0 AND expires_at>datetime('now')",
              (tid, email))
    row = c.fetchone()

    if not row or row['token'] != token:
        conn.close()
        return jsonify({'success': False, 'error': 'Code incorrect ou expiré.'}), 401

    c.execute("UPDATE doc_access_tokens SET used=1, used_at=datetime('now') WHERE id=?", (tid,))

    sk         = secrets.token_urlsafe(48)
    expires_at = (datetime.now() + timedelta(hours=SESSION_HOURS)).isoformat()
    ip         = request.headers.get('X-Forwarded-For', request.remote_addr or '')[:60]
    c.execute("INSERT INTO doc_sessions (session_key,email,username,token_id,expires_at,ip) VALUES (?,?,?,?,?,?)",
              (sk, email, username, tid, expires_at, ip))
    conn.commit()
    conn.close()

    session['doc_session_key']    = sk
    session['doc_email']          = email
    session['doc_username']       = username
    for k in ('doc_pending_token_id','doc_pending_email','doc_pending_username'):
        session.pop(k, None)

    return jsonify({'success': True, 'redirect': url_for('documents.store')})

@documents_bp.route('/access/logout', methods=['POST'])
def logout_doc():
    sk = session.pop('doc_session_key', None)
    session.pop('doc_email', None)
    session.pop('doc_username', None)
    if sk:
        conn = _db()
        conn.execute("DELETE FROM doc_sessions WHERE session_key=?", (sk,))
        conn.commit()
        conn.close()
    return redirect(url_for('documents.access_page'))


# ═══════════════════════════════════════════════════════════════
#  BOUTIQUE PRINCIPALE
# ═══════════════════════════════════════════════════════════════

@documents_bp.route('/', methods=['GET'])
@documents_bp.route('', methods=['GET'])
@doc_access_required
def store():
    doc_sess    = _get_doc_session()
    is_admin    = session.get('role') in ('admin','superadmin')
    viewer_name = session.get('username') if is_admin else (doc_sess or {}).get('username', 'Visiteur')
    viewer_mail = session.get('email')    if is_admin else (doc_sess or {}).get('email', '')
    user_id     = session.get('user_id', 0)

    category = request.args.get('category', '')
    q        = request.args.get('q', '').strip()

    conn = _db()
    c    = conn.cursor()

    sql    = "SELECT * FROM trading_documents WHERE 1=1"
    params = []
    if not is_admin:
        sql += " AND is_published=1"
    if category:
        sql += " AND category=?"; params.append(category)
    if q:
        sql += " AND (title LIKE ? OR description LIKE ?)"; params += [f'%{q}%', f'%{q}%']
    sql += " ORDER BY created_at DESC"

    c.execute(sql, params)
    docs = [dict(r) for r in c.fetchall()]
    for d in docs:
        try:    d['tags'] = json.loads(d['tags'] or '[]')
        except: d['tags'] = []

    c.execute("SELECT DISTINCT category FROM trading_documents WHERE is_published=1 ORDER BY category")
    categories = [r[0] for r in c.fetchall()]

    stats = {'total': 0, 'free': 0, 'paid': 0, 'downloads': 0, 'active_sessions': 0}
    purchases = []

    if is_admin:
        c.execute("SELECT COUNT(*) as t, COALESCE(SUM(is_free),0) as fr, COALESCE(SUM(downloads),0) as d FROM trading_documents WHERE is_published=1")
        row = c.fetchone()
        stats.update({'total': row['t'], 'free': row['fr'],
                      'paid': row['t'] - row['fr'], 'downloads': row['d']})
        c.execute("SELECT COUNT(*) as s FROM doc_sessions WHERE expires_at>datetime('now')")
        stats['active_sessions'] = c.fetchone()['s']
        c.execute("""SELECT dp.*, td.title as doc_title
                     FROM doc_purchases dp
                     JOIN trading_documents td ON td.id=dp.document_id
                     ORDER BY dp.created_at DESC LIMIT 30""")
        purchases = [dict(r) for r in c.fetchall()]

    purchased_ids = set()
    if not is_admin and viewer_mail:
        c.execute("SELECT document_id FROM doc_purchases WHERE email=? AND status='confirmed'",
                  (viewer_mail,))
        purchased_ids = {r[0] for r in c.fetchall()}

    conn.close()
    unread = _unread_notifications(user_id) if user_id else 0

    return render_template('documents.html',
        docs=docs, categories=categories,
        stats=stats, purchases=purchases,
        is_admin=is_admin,
        viewer_name=viewer_name, viewer_mail=viewer_mail,
        current_category=category, search_q=q,
        purchased_ids=list(purchased_ids),
        unread_notifications=unread,
        token_minutes=TOKEN_VALIDITY,
    )


# ═══════════════════════════════════════════════════════════════
#  CRUD DOCUMENTS (admin)
# ═══════════════════════════════════════════════════════════════

@documents_bp.route('/add', methods=['POST'])
@doc_access_required
@admin_only_doc
def add_document():
    title       = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    category    = request.form.get('category', 'Général').strip() or 'Général'
    tags_raw    = request.form.get('tags', '')
    price       = float(request.form.get('price', 0) or 0)
    currency    = request.form.get('currency', 'XAF')
    is_free     = 1 if price == 0 else 0
    link_url    = request.form.get('link_url', '').strip()
    link_label  = request.form.get('link_label', '').strip() or 'Ouvrir le lien'
    file_url    = request.form.get('file_url', '').strip()
    thumbnail   = request.form.get('thumbnail_url', '').strip()

    if not title:
        return jsonify({'success': False, 'error': 'Le titre est requis'}), 400

    file_path = None
    f = request.files.get('document_file')
    if f and f.filename:
        ext = (f.filename.rsplit('.', 1)[-1].lower()) if '.' in f.filename else ''
        if ext not in ALLOWED_DOCS:
            return jsonify({'success': False, 'error': f'Extension .{ext} non autorisée'}), 400
        fname = secure_filename(
            f"doc_{session['user_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{f.filename}")
        f.save(os.path.join(UPLOAD_DOCS, fname))
        file_path = f'static/uploads/docs/{fname}'

    has_file = bool(file_path or file_url)
    has_link = bool(link_url)
    doc_type = 'both' if (has_file and has_link) else ('link' if has_link else 'file')
    tags_json = json.dumps([t.strip() for t in tags_raw.split(',') if t.strip()])

    conn = _db()
    c    = conn.cursor()
    c.execute('''
        INSERT INTO trading_documents
        (title,description,file_path,file_url,link_url,link_label,doc_type,
         category,tags,price,currency,is_free,is_published,thumbnail_url,
         created_by,created_at,updated_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,1,?,?,datetime('now'),datetime('now'))
    ''', (title, description, file_path, file_url or None, link_url or None, link_label,
          doc_type, category, tags_json, price, currency, is_free,
          thumbnail or None, session['user_id']))
    new_id = c.lastrowid
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'id': new_id, 'message': f'Document « {title} » ajouté !'})

@documents_bp.route('/update/<int:doc_id>', methods=['POST'])
@doc_access_required
@admin_only_doc
def update_document(doc_id):
    data = request.get_json(force=True, silent=True) or {}
    editable = ['title','description','category','price','currency','is_free',
                'is_published','link_url','link_label','file_url','thumbnail_url','tags']
    sets, params = [], []
    for f in editable:
        if f in data:
            val = data[f]
            if f == 'tags' and isinstance(val, list): val = json.dumps(val)
            sets.append(f'{f}=?'); params.append(val)
    if not sets:
        return jsonify({'success': False, 'error': 'Rien à modifier'}), 400
    sets.append("updated_at=datetime('now')")
    params.append(doc_id)
    conn = _db()
    conn.execute(f"UPDATE trading_documents SET {', '.join(sets)} WHERE id=?", params)
    conn.commit(); conn.close()
    return jsonify({'success': True})

@documents_bp.route('/delete/<int:doc_id>', methods=['POST','DELETE'])
@doc_access_required
@admin_only_doc
def delete_document(doc_id):
    conn = _db()
    c    = conn.cursor()
    c.execute("SELECT file_path FROM trading_documents WHERE id=?", (doc_id,))
    row  = c.fetchone()
    if row and row['file_path']:
        try: os.remove(row['file_path'])
        except: pass
    c.execute("DELETE FROM trading_documents WHERE id=?", (doc_id,))
    conn.commit(); conn.close()
    return jsonify({'success': True, 'message': 'Document supprimé'})


# ═══════════════════════════════════════════════════════════════
#  TÉLÉCHARGEMENT / ACCÈS LIEN
# ═══════════════════════════════════════════════════════════════

@documents_bp.route('/download/<int:doc_id>')
@doc_access_required
def download_doc(doc_id):
    doc_sess = _get_doc_session()
    is_admin = session.get('role') in ('admin','superadmin')
    email    = session.get('email') if is_admin else (doc_sess or {}).get('email', '')

    conn = _db()
    c    = conn.cursor()
    c.execute("SELECT * FROM trading_documents WHERE id=? AND is_published=1", (doc_id,))
    doc  = c.fetchone()
    if not doc: conn.close(); abort(404)
    doc  = dict(doc)

    if not doc['is_free'] and not is_admin:
        c.execute("SELECT id FROM doc_purchases WHERE document_id=? AND email=? AND status='confirmed'",
                  (doc_id, email))
        if not c.fetchone():
            conn.close()
            return jsonify({'success': False,
                            'error': 'Achat requis pour télécharger ce document.'}), 403

    c.execute("UPDATE trading_documents SET downloads=downloads+1 WHERE id=?", (doc_id,))
    conn.commit(); conn.close()

    if doc['file_url']:
        from flask import redirect as _redir
        return _redir(doc['file_url'])
    if doc['file_path'] and os.path.exists(doc['file_path']):
        return send_file(doc['file_path'], as_attachment=True,
                         download_name=os.path.basename(doc['file_path']))
    return jsonify({'error': 'Fichier introuvable'}), 404

@documents_bp.route('/view/<int:doc_id>')
@doc_access_required
def view_doc(doc_id):
    conn = _db()
    c    = conn.cursor()
    c.execute("UPDATE trading_documents SET views=views+1 WHERE id=?", (doc_id,))
    c.execute("SELECT * FROM trading_documents WHERE id=?", (doc_id,))
    doc  = c.fetchone()
    conn.commit(); conn.close()
    if not doc: abort(404)
    doc = dict(doc)
    try:    doc['tags'] = json.loads(doc['tags'] or '[]')
    except: doc['tags'] = []
    return jsonify({'success': True, 'doc': doc})


# ═══════════════════════════════════════════════════════════════
#  COMMANDES / ACHATS
# ═══════════════════════════════════════════════════════════════

@documents_bp.route('/purchase/<int:doc_id>', methods=['POST'])
@doc_access_required
def purchase_doc(doc_id):
    doc_sess = _get_doc_session()
    is_admin = session.get('role') in ('admin','superadmin')
    email    = session.get('email')    if is_admin else (doc_sess or {}).get('email', '')
    username = session.get('username') if is_admin else (doc_sess or {}).get('username', '')
    data     = request.get_json(force=True, silent=True) or {}

    conn = _db()
    c    = conn.cursor()
    c.execute("SELECT * FROM trading_documents WHERE id=?", (doc_id,))
    doc  = c.fetchone()
    if not doc: conn.close(); return jsonify({'success': False, 'error': 'Document introuvable'}), 404
    doc  = dict(doc)

    c.execute("SELECT id,status FROM doc_purchases WHERE document_id=? AND email=?",
              (doc_id, email))
    existing = c.fetchone()
    if existing:
        conn.close()
        if existing['status'] == 'confirmed':
            return jsonify({'success': True, 'already_purchased': True,
                            'message': 'Vous avez déjà acheté ce document.'})
        return jsonify({'success': False,
                        'error': 'Commande déjà en attente de confirmation'}), 409

    c.execute('''INSERT INTO doc_purchases
                 (document_id,email,username,amount,currency,status,payment_method,payment_ref,notes)
                 VALUES (?,?,?,?,?,'pending',?,?,?)''',
              (doc_id, email, username, doc['price'], doc['currency'],
               data.get('payment_method',''), data.get('payment_ref',''),
               data.get('notes','')))
    conn.commit(); conn.close()
    return jsonify({'success': True,
                    'message': 'Commande enregistrée. En attente de confirmation admin.'})

@documents_bp.route('/purchase/confirm/<int:pid>', methods=['POST'])
@doc_access_required
@admin_only_doc
def confirm_purchase(pid):
    conn = _db()
    conn.execute("UPDATE doc_purchases SET status='confirmed', confirmed_by=?, confirmed_at=datetime('now') WHERE id=?",
                 (session['user_id'], pid))
    conn.commit(); conn.close()
    return jsonify({'success': True, 'message': 'Achat confirmé ✅'})

@documents_bp.route('/purchase/reject/<int:pid>', methods=['POST'])
@doc_access_required
@admin_only_doc
def reject_purchase(pid):
    conn = _db()
    conn.execute("UPDATE doc_purchases SET status='rejected' WHERE id=?", (pid,))
    conn.commit(); conn.close()
    return jsonify({'success': True})


# ═══════════════════════════════════════════════════════════════
#  API ADMIN — STATS & SESSIONS
# ═══════════════════════════════════════════════════════════════

@documents_bp.route('/api/stats')
@doc_access_required
@admin_only_doc
def api_stats():
    conn = _db()
    c    = conn.cursor()
    c.execute("SELECT COUNT(*) as t, COALESCE(SUM(is_free),0) as fr FROM trading_documents WHERE is_published=1")
    row  = dict(c.fetchone())
    c.execute("SELECT COUNT(*) as s FROM doc_sessions WHERE expires_at>datetime('now')")
    row['active_sessions'] = c.fetchone()['s']
    c.execute("SELECT status, COUNT(*) as cnt FROM doc_purchases GROUP BY status")
    row['purchases'] = {r['status']: r['cnt'] for r in c.fetchall()}
    conn.close()
    return jsonify({'success': True, 'stats': row})

@documents_bp.route('/api/sessions')
@doc_access_required
@admin_only_doc
def api_sessions():
    conn = _db()
    c    = conn.cursor()
    c.execute("SELECT * FROM doc_sessions WHERE expires_at>datetime('now') ORDER BY created_at DESC LIMIT 50")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return jsonify({'sessions': rows})


# ═══════════════════════════════════════════════════════════════
#  EMAIL TOKEN
# ═══════════════════════════════════════════════════════════════

def _send_access_email(to_email: str, username: str, token: str) -> bool:
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    if not GMAIL.get('password'):
        print(f"[DocStore] ⚠️  GMAIL_APP_PASSWORD absent — token debug : {token}")
        return False

    html = f"""<!DOCTYPE html>
<html><body style="margin:0;padding:0;background:#07090f;font-family:'Segoe UI',Arial,sans-serif;">
<div style="max-width:560px;margin:0 auto;padding:32px 16px;">
  <div style="background:linear-gradient(145deg,#0d1117,#131a24);border-radius:20px;padding:36px;border:1px solid rgba(255,255,255,.07);">
    <div style="text-align:center;margin-bottom:28px;">
      <div style="display:inline-block;width:64px;height:64px;border-radius:18px;background:linear-gradient(135deg,rgba(0,230,118,.2),rgba(74,158,255,.15));border:1px solid rgba(0,230,118,.3);line-height:64px;font-size:2rem;">📊</div>
      <h2 style="color:#00e676;font-weight:800;margin:12px 0 2px;">Kengni Finance</h2>
      <p style="color:#5a6478;font-size:13px;margin:0;">Boutique Documents Trading</p>
    </div>
    <p style="color:#f0f0f0;font-size:16px;margin-bottom:6px;">Bonjour <strong style="color:#00e676;">{username}</strong>,</p>
    <p style="color:#8a94a8;font-size:14px;line-height:1.7;margin-bottom:28px;">
      Voici votre code d'accès à la boutique de documents.<br>
      Valable <strong style="color:#ffd700;">{TOKEN_VALIDITY} minutes</strong>.
    </p>
    <div style="background:rgba(0,230,118,.06);border:2px solid rgba(0,230,118,.3);border-radius:16px;padding:28px;text-align:center;margin-bottom:28px;">
      <p style="color:#5a6478;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:2px;margin:0 0 12px;">Code de vérification</p>
      <div style="font-size:3rem;font-weight:900;letter-spacing:10px;color:#00e676;font-family:monospace;">{token}</div>
      <p style="color:#5a6478;font-size:12px;margin:12px 0 0;">Saisissez ce code sur la page d'accès</p>
    </div>
    <div style="background:rgba(255,71,87,.06);border-radius:12px;padding:14px 18px;border:1px solid rgba(255,71,87,.15);">
      <p style="color:#ff4757;font-size:12px;margin:0;"><strong>⚠️ Sécurité :</strong> Si vous n'avez pas demandé cet accès, ignorez cet email.</p>
    </div>
    <div style="border-top:1px solid rgba(255,255,255,.06);padding-top:18px;text-align:center;margin-top:20px;">
      <p style="color:#3a4255;font-size:11px;margin:0;">© {datetime.now().year} Kengni Finance — Tous droits réservés</p>
    </div>
  </div>
</div>
</body></html>"""

    text = f"Bonjour {username},\nCode d'accès Kengni Finance Boutique : {token}\nValable {TOKEN_VALIDITY} min.\n\n— Kengni Finance"

    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"🔐 [{token}] Code d'accès — Kengni Finance Boutique"
    msg['From']    = f"{GMAIL['name']} <{GMAIL['sender']}>"
    msg['To']      = to_email
    msg.attach(MIMEText(text, 'plain', 'utf-8'))
    msg.attach(MIMEText(html, 'html',  'utf-8'))

    for attempt in range(1, 4):
        try:
            with smtplib.SMTP(GMAIL['host'], GMAIL['port'], timeout=15) as s:
                s.ehlo(); s.starttls(); s.ehlo()
                s.login(GMAIL['sender'], GMAIL['password'])
                s.sendmail(GMAIL['sender'], to_email, msg.as_string())
            print(f"[DocStore] ✅ Token envoyé à {to_email}")
            return True
        except smtplib.SMTPAuthenticationError:
            print("[DocStore] ❌ Auth Gmail échouée — vérifiez GMAIL_APP_PASSWORD")
            return False
        except Exception as e:
            print(f"[DocStore] ⚠️  Tentative {attempt}/3 : {e}")
            if attempt < 3: time.sleep(2 * attempt)
    return False