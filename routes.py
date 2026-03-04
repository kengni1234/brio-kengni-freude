"""
nas/routes.py — Toutes les routes du module NAS
Blueprint : /nas
"""
import os
import json
import sqlite3
import uuid
from datetime import datetime
from functools import wraps

from flask import (
    current_app, g, request, jsonify, render_template,
    redirect, url_for, session, send_file, abort, flash
)
from werkzeug.utils import secure_filename

from . import nas_bp
from .utils import (
    generate_token, compute_expiry,
    send_request_confirmation, send_access_granted,
    send_access_rejected, send_admin_new_request,
    allowed_file, human_size, mime_icon, is_previewable,
    ADMIN_EMAIL, MAX_FILE_SIZE
)


# ══════════════════════════════════════════════════════════════
#  Helpers DB
# ══════════════════════════════════════════════════════════════

def get_db():
    db_path = current_app.config.get('DATABASE', 'database.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def get_nas_upload_folder():
    base = current_app.config.get(
        'NAS_UPLOAD_FOLDER',
        os.path.join(current_app.root_path, 'uploads', 'nas')
    )
    os.makedirs(base, exist_ok=True)
    return base


# ══════════════════════════════════════════════════════════════
#  Décorateurs
# ══════════════════════════════════════════════════════════════

def admin_required(f):
    """Vérifie que l'utilisateur est connecté en tant qu'admin."""
    @wraps(f)
    def decorated(*args, **kwargs):
        # Adapter selon le système d'auth existant :
        # session.get('user_id') ou session.get('admin') selon votre app
        if not session.get('user_id') and not session.get('admin'):
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated


def validate_token(token: str):
    """
    Vérifie un token visiteur.
    Retourne la row de nas_access_requests ou None si invalide.
    """
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM nas_access_requests WHERE token=? AND status='approved'",
        (token,)
    ).fetchone()
    conn.close()
    if not row:
        return None
    # Expiration
    if row['token_expires_at']:
        exp = datetime.fromisoformat(row['token_expires_at'])
        if datetime.utcnow() > exp:
            return None
    # Nb usages
    if row['token_max_uses'] > 0 and row['token_used_count'] >= row['token_max_uses']:
        return None
    return row


# ══════════════════════════════════════════════════════════════
#  ROUTES VISITEURS
# ══════════════════════════════════════════════════════════════

@nas_bp.route('/access', methods=['GET', 'POST'])
def access():
    """Page de demande d'accès visiteur."""
    conn = get_db()
    # Charger les fichiers publiquement listables (pour les checkboxes)
    files = conn.execute(
        "SELECT id, title, category FROM nas_files ORDER BY category, title"
    ).fetchall()

    if request.method == 'POST':
        email     = request.form.get('email', '').strip().lower()
        full_name = request.form.get('full_name', '').strip()
        reason    = request.form.get('reason', '').strip()
        req_files = request.form.getlist('requested_files')

        if not email or not full_name:
            conn.close()
            return jsonify({'success': False, 'error': 'Nom et email requis'})

        # Vérifier doublon en attente
        existing = conn.execute(
            "SELECT id FROM nas_access_requests WHERE email=? AND status='pending'",
            (email,)
        ).fetchone()
        if existing:
            conn.close()
            return jsonify({'success': False,
                            'error': 'Une demande est déjà en attente pour cet email'})

        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        conn.execute(
            """INSERT INTO nas_access_requests
               (email, full_name, reason, requested_files, ip_address)
               VALUES (?, ?, ?, ?, ?)""",
            (email, full_name, reason, json.dumps(req_files), ip)
        )
        conn.commit()
        conn.close()

        # Emails
        send_request_confirmation(email, full_name)
        send_admin_new_request(ADMIN_EMAIL, full_name, email, reason)

        return jsonify({'success': True,
                        'message': 'Demande envoyée ! Vous recevrez un email sous peu.'})

    conn.close()
    return render_template('nas_access.html', files=files)


@nas_bp.route('/access/<token>')
def access_files(token):
    """Page d'accès visiteur avec token valide."""
    req_row = validate_token(token)
    if not req_row:
        return render_template('nas_access.html', token_error=True, files=[])

    conn = get_db()

    # Déterminer les fichiers autorisés
    allowed_ids = json.loads(req_row['allowed_files'] or '[]')
    if allowed_ids:
        placeholders = ','.join('?' * len(allowed_ids))
        files = conn.execute(
            f"SELECT * FROM nas_files WHERE id IN ({placeholders}) ORDER BY category, title",
            allowed_ids
        ).fetchall()
    else:
        files = conn.execute(
            "SELECT * FROM nas_files ORDER BY category, title"
        ).fetchall()

    # Log de la visite
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ua = request.headers.get('User-Agent', '')
    conn.execute(
        """INSERT INTO nas_access_logs (request_id, file_id, action, ip_address, user_agent)
           VALUES (?, NULL, 'view', ?, ?)""",
        (req_row['id'], ip, ua)
    )
    conn.execute(
        "UPDATE nas_access_requests SET token_used_count = token_used_count + 1 WHERE id=?",
        (req_row['id'],)
    )
    conn.commit()

    # Préparer les données fichiers pour le template
    files_data = []
    for f in files:
        files_data.append({
            'id':       f['id'],
            'title':    f['title'],
            'category': f['category'],
            'description': f['description'] or '',
            'filesize': human_size(f['filesize']),
            'mimetype': f['mimetype'],
            'icon':     mime_icon(f['mimetype']),
            'previewable': is_previewable(f['mimetype']),
            'download_count': f['download_count'],
        })

    # Calculer info token
    exp = None
    if req_row['token_expires_at']:
        exp = datetime.fromisoformat(req_row['token_expires_at'])

    uses_left = -1
    if req_row['token_max_uses'] > 0:
        uses_left = req_row['token_max_uses'] - req_row['token_used_count']

    conn.close()
    return render_template(
        'nas_files.html',
        token=token,
        req=req_row,
        files=files_data,
        token_expires=exp,
        uses_left=uses_left,
    )


@nas_bp.route('/download/<token>/<int:file_id>')
def download_file(token, file_id):
    """Téléchargement sécurisé d'un fichier."""
    req_row = validate_token(token)
    if not req_row:
        abort(403)

    # Vérifier que le fichier est autorisé
    allowed_ids = json.loads(req_row['allowed_files'] or '[]')
    if allowed_ids and file_id not in [int(x) for x in allowed_ids]:
        abort(403)

    conn = get_db()
    f = conn.execute("SELECT * FROM nas_files WHERE id=?", (file_id,)).fetchone()
    if not f:
        conn.close()
        abort(404)

    # Log téléchargement
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ua = request.headers.get('User-Agent', '')
    conn.execute(
        """INSERT INTO nas_access_logs (request_id, file_id, action, ip_address, user_agent)
           VALUES (?, ?, 'download', ?, ?)""",
        (req_row['id'], file_id, ip, ua)
    )
    conn.execute(
        "UPDATE nas_files SET download_count = download_count + 1 WHERE id=?", (file_id,)
    )
    conn.commit()
    conn.close()

    filepath = f['filepath']
    if not os.path.exists(filepath):
        abort(404)

    return send_file(
        filepath,
        as_attachment=True,
        download_name=f['filename_original'],
        mimetype=f['mimetype']
    )


@nas_bp.route('/preview/<token>/<int:file_id>')
def preview_file(token, file_id):
    """Prévisualisation en ligne (PDF / images)."""
    req_row = validate_token(token)
    if not req_row:
        abort(403)

    allowed_ids = json.loads(req_row['allowed_files'] or '[]')
    if allowed_ids and file_id not in [int(x) for x in allowed_ids]:
        abort(403)

    conn = get_db()
    f = conn.execute("SELECT * FROM nas_files WHERE id=?", (file_id,)).fetchone()
    conn.close()

    if not f or not is_previewable(f['mimetype']):
        abort(400)

    if not os.path.exists(f['filepath']):
        abort(404)

    return send_file(f['filepath'], mimetype=f['mimetype'])


# ══════════════════════════════════════════════════════════════
#  ROUTES ADMIN
# ══════════════════════════════════════════════════════════════

@nas_bp.route('/admin')
@admin_required
def admin():
    """Tableau de bord admin principal."""
    conn = get_db()

    # Stats
    nb_files    = conn.execute("SELECT COUNT(*) FROM nas_files").fetchone()[0]
    nb_pending  = conn.execute(
        "SELECT COUNT(*) FROM nas_access_requests WHERE status='pending'"
    ).fetchone()[0]
    nb_active   = conn.execute(
        "SELECT COUNT(*) FROM nas_access_requests WHERE status='approved'"
    ).fetchone()[0]
    nb_dl       = conn.execute(
        "SELECT COALESCE(SUM(download_count),0) FROM nas_files"
    ).fetchone()[0]

    # Espace disque
    sizes = conn.execute("SELECT COALESCE(SUM(filesize),0) FROM nas_files").fetchone()[0]
    disk_used = human_size(sizes)

    # Demandes en attente
    pending = conn.execute(
        """SELECT * FROM nas_access_requests
           WHERE status='pending' ORDER BY created_at DESC"""
    ).fetchall()

    # Demandes récentes (toutes)
    all_requests = conn.execute(
        """SELECT * FROM nas_access_requests ORDER BY created_at DESC LIMIT 30"""
    ).fetchall()

    # Fichiers
    files = conn.execute(
        "SELECT * FROM nas_files ORDER BY created_at DESC"
    ).fetchall()

    # Logs récents
    logs = conn.execute(
        """SELECT l.*, r.email, r.full_name, f.title as file_title
           FROM nas_access_logs l
           LEFT JOIN nas_access_requests r ON l.request_id = r.id
           LEFT JOIN nas_files f ON l.file_id = f.id
           ORDER BY l.accessed_at DESC LIMIT 50"""
    ).fetchall()

    conn.close()

    files_data = [{
        'id': f['id'], 'title': f['title'],
        'filename_original': f['filename_original'],
        'category': f['category'], 'description': f['description'] or '',
        'filesize': human_size(f['filesize']), 'mimetype': f['mimetype'],
        'icon': mime_icon(f['mimetype']),
        'download_count': f['download_count'],
        'created_at': f['created_at'],
    } for f in files]

    return render_template(
        'nas_admin.html',
        nb_files=nb_files, nb_pending=nb_pending,
        nb_active=nb_active, nb_dl=nb_dl, disk_used=disk_used,
        pending=pending, all_requests=all_requests,
        files=files_data, logs=logs,
    )


# ── Upload ──────────────────────────────────────────────────

@nas_bp.route('/admin/upload', methods=['POST'])
@admin_required
def upload_file():
    """Upload un ou plusieurs fichiers."""
    uploaded = request.files.getlist('files')
    if not uploaded:
        return jsonify({'success': False, 'error': 'Aucun fichier reçu'})

    title    = request.form.get('title', '').strip()
    category = request.form.get('category', 'Général').strip() or 'Général'
    desc     = request.form.get('description', '').strip()
    upload_folder = get_nas_upload_folder()
    conn = get_db()
    added = []

    for file in uploaded:
        if not file or not file.filename:
            continue
        if not allowed_file(file.filename):
            continue

        orig_name = secure_filename(file.filename)
        ext       = orig_name.rsplit('.', 1)[-1].lower() if '.' in orig_name else 'bin'
        stored    = f"{uuid.uuid4().hex}.{ext}"
        dest_path = os.path.join(upload_folder, stored)

        file.seek(0, 2)
        size = file.tell()
        file.seek(0)
        if size > MAX_FILE_SIZE:
            continue

        file.save(dest_path)
        mime = file.content_type or 'application/octet-stream'
        file_title = title if len(uploaded) == 1 and title else orig_name

        conn.execute(
            """INSERT INTO nas_files
               (title, filename_original, filename_stored, filepath, filesize, mimetype, category, description)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (file_title, orig_name, stored, dest_path, size, mime, category, desc)
        )
        added.append(orig_name)

    conn.commit()
    conn.close()

    if not added:
        return jsonify({'success': False, 'error': 'Aucun fichier valide uploadé'})
    return jsonify({'success': True, 'message': f'{len(added)} fichier(s) uploadé(s)', 'files': added})


@nas_bp.route('/admin/files/edit/<int:file_id>', methods=['POST'])
@admin_required
def edit_file(file_id):
    """Modifier les métadonnées d'un fichier."""
    data = request.get_json()
    conn = get_db()
    conn.execute(
        """UPDATE nas_files SET title=?, category=?, description=?, updated_at=?
           WHERE id=?""",
        (data.get('title'), data.get('category', 'Général'),
         data.get('description', ''), datetime.utcnow().isoformat(), file_id)
    )
    conn.commit()
    conn.close()
    return jsonify({'success': True})


@nas_bp.route('/admin/files/delete/<int:file_id>', methods=['POST'])
@admin_required
def delete_file(file_id):
    """Supprime un fichier (disque + base)."""
    conn = get_db()
    f = conn.execute("SELECT * FROM nas_files WHERE id=?", (file_id,)).fetchone()
    if not f:
        conn.close()
        return jsonify({'success': False, 'error': 'Fichier introuvable'})
    try:
        if os.path.exists(f['filepath']):
            os.remove(f['filepath'])
    except Exception:
        pass
    conn.execute("DELETE FROM nas_files WHERE id=?", (file_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})


# ── Gestion des demandes ────────────────────────────────────

@nas_bp.route('/admin/requests/approve/<int:req_id>', methods=['POST'])
@admin_required
def approve_request(req_id):
    """Approuver une demande + générer token + envoyer mail."""
    data      = request.get_json() or {}
    days      = int(data.get('expiry_days', 7))
    max_uses  = int(data.get('max_uses', -1))
    file_ids  = data.get('allowed_files', [])   # [] = tous
    admin_note = data.get('admin_note', '')

    conn = get_db()
    req = conn.execute(
        "SELECT * FROM nas_access_requests WHERE id=?", (req_id,)
    ).fetchone()
    if not req:
        conn.close()
        return jsonify({'success': False, 'error': 'Demande introuvable'})

    token   = generate_token()
    expires = compute_expiry(days)
    exp_iso = expires.isoformat() if expires else None

    conn.execute(
        """UPDATE nas_access_requests SET
           status='approved', token=?, token_expires_at=?,
           token_max_uses=?, allowed_files=?,
           admin_note=?, approved_at=?
           WHERE id=?""",
        (token, exp_iso, max_uses, json.dumps(file_ids),
         admin_note, datetime.utcnow().isoformat(), req_id)
    )
    conn.commit()

    # Récupérer les fichiers pour l'email
    if file_ids:
        placeholders = ','.join('?' * len(file_ids))
        files = conn.execute(
            f"SELECT id, title FROM nas_files WHERE id IN ({placeholders})",
            file_ids
        ).fetchall()
    else:
        files = conn.execute("SELECT id, title FROM nas_files").fetchall()

    conn.close()

    files_list = [{'title': f['title']} for f in files]
    send_access_granted(req['email'], req['full_name'], token,
                        files_list, expires, max_uses)

    return jsonify({'success': True, 'token': token})


@nas_bp.route('/admin/requests/reject/<int:req_id>', methods=['POST'])
@admin_required
def reject_request(req_id):
    """Rejeter une demande d'accès."""
    data   = request.get_json() or {}
    reason = data.get('reason', '')

    conn = get_db()
    req = conn.execute(
        "SELECT * FROM nas_access_requests WHERE id=?", (req_id,)
    ).fetchone()
    if not req:
        conn.close()
        return jsonify({'success': False, 'error': 'Demande introuvable'})

    conn.execute(
        "UPDATE nas_access_requests SET status='rejected', admin_note=? WHERE id=?",
        (reason, req_id)
    )
    conn.commit()
    conn.close()

    send_access_rejected(req['email'], req['full_name'], reason)
    return jsonify({'success': True})


@nas_bp.route('/admin/requests/revoke/<int:req_id>', methods=['POST'])
@admin_required
def revoke_token(req_id):
    """Révoquer un token actif."""
    conn = get_db()
    conn.execute(
        "UPDATE nas_access_requests SET status='revoked', token=NULL WHERE id=?",
        (req_id,)
    )
    conn.commit()
    conn.close()
    return jsonify({'success': True})


# ── Stats JSON ──────────────────────────────────────────────

@nas_bp.route('/admin/stats')
@admin_required
def stats():
    conn = get_db()
    data = {
        'nb_files':   conn.execute("SELECT COUNT(*) FROM nas_files").fetchone()[0],
        'nb_pending': conn.execute(
            "SELECT COUNT(*) FROM nas_access_requests WHERE status='pending'"
        ).fetchone()[0],
        'nb_active':  conn.execute(
            "SELECT COUNT(*) FROM nas_access_requests WHERE status='approved'"
        ).fetchone()[0],
        'nb_dl':      conn.execute(
            "SELECT COALESCE(SUM(download_count),0) FROM nas_files"
        ).fetchone()[0],
        'disk_bytes': conn.execute(
            "SELECT COALESCE(SUM(filesize),0) FROM nas_files"
        ).fetchone()[0],
    }
    conn.close()
    return jsonify(data)
