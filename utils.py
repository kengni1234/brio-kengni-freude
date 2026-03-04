"""
nas/utils.py — Utilitaires : génération de tokens, envoi d'emails
"""
import uuid
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta


# ── Constantes configurables via .env ─────────────────────────
MAIL_SERVER   = os.getenv('MAIL_SERVER',   'smtp.gmail.com')
MAIL_PORT     = int(os.getenv('MAIL_PORT', '587'))
MAIL_USE_TLS  = os.getenv('MAIL_USE_TLS',  'true').lower() == 'true'
MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
MAIL_SENDER   = os.getenv('MAIL_DEFAULT_SENDER', MAIL_USERNAME)
ADMIN_EMAIL   = os.getenv('NAS_ADMIN_NOTIFICATION_EMAIL', MAIL_USERNAME)
BASE_URL       = os.getenv('BASE_URL', 'http://localhost:5000')


# ── Génération de token ───────────────────────────────────────
def generate_token() -> str:
    """Génère un UUID4 sans tirets (32 chars hex)."""
    return uuid.uuid4().hex


def compute_expiry(days: int) -> datetime | None:
    """Calcule la date d'expiration. days=-1 → pas d'expiration."""
    if days <= 0:
        return None
    return datetime.utcnow() + timedelta(days=days)


# ── Envoi d'emails ────────────────────────────────────────────
def _send(to: str, subject: str, html: str, text: str = '') -> bool:
    """Envoie un email HTML. Retourne True si succès."""
    if not MAIL_USERNAME or not MAIL_PASSWORD:
        print(f"[NAS] Email non envoyé (SMTP non configuré) → {subject}")
        return False
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From']    = MAIL_SENDER
        msg['To']      = to
        if text:
            msg.attach(MIMEText(text, 'plain', 'utf-8'))
        msg.attach(MIMEText(html, 'html', 'utf-8'))

        with smtplib.SMTP(MAIL_SERVER, MAIL_PORT) as srv:
            if MAIL_USE_TLS:
                srv.starttls()
            srv.login(MAIL_USERNAME, MAIL_PASSWORD)
            srv.sendmail(MAIL_SENDER, to, msg.as_string())
        return True
    except Exception as e:
        print(f"[NAS] Erreur SMTP: {e}")
        return False


def send_request_confirmation(email: str, full_name: str) -> bool:
    """Mail envoyé au visiteur après sa demande d'accès."""
    subject = "Demande d'accès reçue — Kengni Finance NAS"
    html = f"""
<!DOCTYPE html><html><body style="margin:0;padding:0;background:#07090f;font-family:'Segoe UI',Arial,sans-serif">
<div style="max-width:560px;margin:40px auto;background:#0d1117;border:1px solid rgba(255,255,255,.07);border-radius:18px;overflow:hidden">
  <div style="background:linear-gradient(135deg,#00c853,#009944);padding:28px 32px">
    <h1 style="margin:0;color:#000;font-size:22px;font-weight:800">🗄️ Kengni Finance NAS</h1>
  </div>
  <div style="padding:32px">
    <p style="color:#f0f0f0;font-size:16px;font-weight:700;margin:0 0 12px">Bonjour {full_name},</p>
    <p style="color:#8a9bb0;font-size:14px;line-height:1.7;margin:0 0 20px">
      Votre demande d'accès au serveur de fichiers privés <strong style="color:#f0f0f0">Kengni Finance</strong> a bien été reçue.<br>
      Notre équipe l'examinera dans les meilleurs délais. Vous recevrez un email dès qu'une décision sera prise.
    </p>
    <div style="background:#131a24;border-radius:10px;padding:16px;border-left:3px solid #00e676">
      <p style="color:#5a6478;font-size:12px;margin:0 0 4px;text-transform:uppercase;letter-spacing:1px">Statut</p>
      <p style="color:#ffd700;font-size:14px;font-weight:700;margin:0">⏳ En attente de validation</p>
    </div>
  </div>
  <div style="padding:16px 32px;border-top:1px solid rgba(255,255,255,.07)">
    <p style="color:#5a6478;font-size:12px;margin:0">Kengni Finance · Cet email est automatique, ne pas répondre.</p>
  </div>
</div></body></html>"""
    return _send(email, subject, html)


def send_access_granted(email: str, full_name: str, token: str,
                        files: list, expires_at: datetime | None,
                        max_uses: int) -> bool:
    """Mail envoyé au visiteur avec le lien d'accès token."""
    access_url = f"{BASE_URL}/nas/access/{token}"
    expiry_str = expires_at.strftime('%d/%m/%Y à %H:%M UTC') if expires_at else 'Illimitée'
    uses_str   = str(max_uses) if max_uses > 0 else 'Illimité'

    files_html = ''.join(
        f'<li style="color:#8a9bb0;font-size:13px;padding:4px 0">'
        f'📄 {f["title"]}</li>' for f in files
    ) or '<li style="color:#5a6478;font-size:13px">Tous les fichiers autorisés</li>'

    subject = "✅ Votre accès NAS Kengni Finance est activé"
    html = f"""
<!DOCTYPE html><html><body style="margin:0;padding:0;background:#07090f;font-family:'Segoe UI',Arial,sans-serif">
<div style="max-width:560px;margin:40px auto;background:#0d1117;border:1px solid rgba(255,255,255,.07);border-radius:18px;overflow:hidden">
  <div style="background:linear-gradient(135deg,#00c853,#009944);padding:28px 32px">
    <h1 style="margin:0;color:#000;font-size:22px;font-weight:800">✅ Accès Accordé</h1>
    <p style="margin:6px 0 0;color:rgba(0,0,0,.7);font-size:14px">Kengni Finance — Serveur de fichiers privés</p>
  </div>
  <div style="padding:32px">
    <p style="color:#f0f0f0;font-size:16px;font-weight:700;margin:0 0 12px">Bonjour {full_name},</p>
    <p style="color:#8a9bb0;font-size:14px;line-height:1.7;margin:0 0 24px">
      Votre demande d'accès a été <strong style="color:#00e676">approuvée</strong>. Cliquez sur le bouton ci-dessous pour accéder aux fichiers qui vous ont été attribués.
    </p>
    <div style="text-align:center;margin-bottom:28px">
      <a href="{access_url}" style="display:inline-block;background:linear-gradient(135deg,#00c853,#009944);color:#000;font-weight:800;font-size:15px;padding:14px 32px;border-radius:12px;text-decoration:none">
        🔓 Accéder aux fichiers
      </a>
    </div>
    <div style="background:#131a24;border-radius:10px;padding:16px;margin-bottom:16px">
      <p style="color:#5a6478;font-size:11px;text-transform:uppercase;letter-spacing:1px;margin:0 0 8px">Détails de votre accès</p>
      <p style="color:#f0f0f0;font-size:13px;margin:0 0 6px">⏰ <strong>Expiration :</strong> <span style="color:#ffd700">{expiry_str}</span></p>
      <p style="color:#f0f0f0;font-size:13px;margin:0 0 10px">🔢 <strong>Téléchargements max :</strong> <span style="color:#4a9eff">{uses_str}</span></p>
      <p style="color:#5a6478;font-size:12px;text-transform:uppercase;letter-spacing:.5px;margin:0 0 6px">Fichiers accessibles</p>
      <ul style="margin:0;padding-left:16px">{files_html}</ul>
    </div>
    <div style="background:#131a24;border-radius:10px;padding:12px 16px;border-left:3px solid #4a9eff">
      <p style="color:#5a6478;font-size:12px;margin:0 0 4px">Lien d'accès direct</p>
      <p style="color:#4a9eff;font-size:12px;font-family:monospace;margin:0;word-break:break-all">{access_url}</p>
    </div>
  </div>
  <div style="padding:16px 32px;border-top:1px solid rgba(255,255,255,.07)">
    <p style="color:#5a6478;font-size:12px;margin:0">⚠️ Ne partagez pas ce lien. Il est personnel et lié à votre adresse email.</p>
  </div>
</div></body></html>"""
    return _send(email, subject, html)


def send_access_rejected(email: str, full_name: str, reason: str = '') -> bool:
    """Mail de refus envoyé au visiteur."""
    reason_block = (
        f'<div style="background:#131a24;border-radius:10px;padding:16px;border-left:3px solid #ff4757;margin-top:16px">'
        f'<p style="color:#5a6478;font-size:11px;text-transform:uppercase;margin:0 0 4px">Motif</p>'
        f'<p style="color:#f0f0f0;font-size:13px;margin:0">{reason}</p></div>'
    ) if reason else ''

    subject = "Demande d'accès — Kengni Finance NAS"
    html = f"""
<!DOCTYPE html><html><body style="margin:0;padding:0;background:#07090f;font-family:'Segoe UI',Arial,sans-serif">
<div style="max-width:560px;margin:40px auto;background:#0d1117;border:1px solid rgba(255,255,255,.07);border-radius:18px;overflow:hidden">
  <div style="background:linear-gradient(135deg,#ff4757,#c0392b);padding:28px 32px">
    <h1 style="margin:0;color:#fff;font-size:22px;font-weight:800">❌ Demande non accordée</h1>
  </div>
  <div style="padding:32px">
    <p style="color:#f0f0f0;font-size:16px;font-weight:700;margin:0 0 12px">Bonjour {full_name},</p>
    <p style="color:#8a9bb0;font-size:14px;line-height:1.7;margin:0">
      Votre demande d'accès au serveur de fichiers Kengni Finance n'a pas pu être accordée.
    </p>
    {reason_block}
  </div>
  <div style="padding:16px 32px;border-top:1px solid rgba(255,255,255,.07)">
    <p style="color:#5a6478;font-size:12px;margin:0">Kengni Finance · Cet email est automatique.</p>
  </div>
</div></body></html>"""
    return _send(email, subject, html)


def send_admin_new_request(admin_email: str, full_name: str,
                           visitor_email: str, reason: str) -> bool:
    """Notification à l'admin pour une nouvelle demande."""
    dashboard_url = f"{BASE_URL}/nas/admin"
    subject = f"[NAS] Nouvelle demande d'accès de {full_name}"
    html = f"""
<!DOCTYPE html><html><body style="margin:0;padding:0;background:#07090f;font-family:'Segoe UI',Arial,sans-serif">
<div style="max-width:560px;margin:40px auto;background:#0d1117;border:1px solid rgba(255,255,255,.07);border-radius:18px;overflow:hidden">
  <div style="background:linear-gradient(135deg,#4a9eff,#7c6aff);padding:28px 32px">
    <h1 style="margin:0;color:#fff;font-size:20px;font-weight:800">🔔 Nouvelle demande NAS</h1>
  </div>
  <div style="padding:32px">
    <div style="background:#131a24;border-radius:10px;padding:16px;margin-bottom:20px">
      <p style="color:#f0f0f0;font-size:14px;margin:0 0 8px"><strong>Nom :</strong> {full_name}</p>
      <p style="color:#f0f0f0;font-size:14px;margin:0 0 8px"><strong>Email :</strong> {visitor_email}</p>
      <p style="color:#8a9bb0;font-size:13px;margin:0"><strong>Motif :</strong> {reason or 'Non précisé'}</p>
    </div>
    <div style="text-align:center">
      <a href="{dashboard_url}" style="display:inline-block;background:linear-gradient(135deg,#4a9eff,#7c6aff);color:#fff;font-weight:800;font-size:14px;padding:12px 28px;border-radius:10px;text-decoration:none">
        Voir le tableau de bord
      </a>
    </div>
  </div>
</div></body></html>"""
    return _send(admin_email, subject, html)


# ── Helpers fichiers ──────────────────────────────────────────
MIME_ICONS = {
    'application/pdf': '📄',
    'application/zip': '🗜️',
    'application/x-zip-compressed': '🗜️',
    'application/vnd.ms-excel': '📊',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '📊',
    'application/msword': '📝',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '📝',
    'video/mp4': '🎬',
    'video/avi': '🎬',
    'video/quicktime': '🎬',
    'image/jpeg': '🖼️',
    'image/png': '🖼️',
    'image/gif': '🖼️',
    'image/webp': '🖼️',
    'text/plain': '📃',
    'text/csv': '📊',
    'application/json': '⚙️',
}

ALLOWED_EXTENSIONS = {
    'pdf', 'docx', 'doc', 'xlsx', 'xls', 'csv',
    'zip', 'rar', '7z',
    'mp4', 'avi', 'mov', 'mkv',
    'png', 'jpg', 'jpeg', 'gif', 'webp',
    'txt', 'json', 'pptx', 'ppt'
}

MAX_FILE_SIZE = int(os.getenv('NAS_MAX_FILE_SIZE', str(500 * 1024 * 1024)))  # 500 Mo


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def human_size(size: int) -> str:
    for unit in ('o', 'Ko', 'Mo', 'Go'):
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} To"


def mime_icon(mime: str) -> str:
    return MIME_ICONS.get(mime, '📁')


def is_previewable(mime: str) -> bool:
    return mime in ('application/pdf',) or mime.startswith('image/')
