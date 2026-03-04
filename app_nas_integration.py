"""
app_nas_integration.py
═══════════════════════════════════════════════════════════════
Montre COMMENT intégrer le blueprint NAS dans votre app Flask existante.
Copiez uniquement les lignes marquées  ← AJOUTER  dans votre vrai app.py / __init__.py
═══════════════════════════════════════════════════════════════
"""
import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()  # charge .env

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'changez-moi-en-production')
app.config['DATABASE']          = os.getenv('DATABASE_PATH', 'database.db')
app.config['NAS_UPLOAD_FOLDER'] = os.getenv('NAS_UPLOAD_FOLDER',
                                             os.path.join(app.root_path, 'uploads', 'nas'))
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('NAS_MAX_FILE_SIZE', str(500 * 1024 * 1024)))

# ─── Blueprints existants (exemple) ───────────────────────────
# from blueprints.documents import documents_bp
# app.register_blueprint(documents_bp)

# ─── ← AJOUTER : Blueprint NAS ────────────────────────────────
from blueprints.nas import nas_bp                   # ← AJOUTER
from blueprints.nas.db import init_nas_db           # ← AJOUTER
app.register_blueprint(nas_bp)                      # ← AJOUTER

# ─── ← AJOUTER : Init DB NAS (1 seule fois au démarrage) ──────
with app.app_context():
    db_path = app.config['DATABASE']
    init_nas_db(db_path)                            # ← AJOUTER
    os.makedirs(app.config['NAS_UPLOAD_FOLDER'], exist_ok=True)  # ← AJOUTER

if __name__ == '__main__':
    app.run(debug=True)


# ═══════════════════════════════════════════════════════════════
# STRUCTURE FINALE DU PROJET
# ═══════════════════════════════════════════════════════════════
#
# project/
# ├── app.py  (ou __init__.py selon votre structure)
# ├── .env
# ├── database.db
# ├── uploads/
# │   └── nas/          ← créé automatiquement, hors webroot
# └── blueprints/
#     ├── documents/    ← votre blueprint existant
#     │   └── ...
#     └── nas/          ← NOUVEAU module à copier
#         ├── __init__.py
#         ├── routes.py
#         ├── utils.py
#         ├── db.py
#         └── templates/
#             ├── nas_admin.html
#             ├── nas_access.html
#             └── nas_files.html
#
# ═══════════════════════════════════════════════════════════════
# FICHIER .env à créer / compléter
# ═══════════════════════════════════════════════════════════════
#
# SECRET_KEY=votre_cle_secrete_longue_et_aleatoire
# DATABASE_PATH=/chemin/absolu/vers/database.db
#
# # SMTP (Gmail exemple — créer un App Password dans compte Google)
# MAIL_SERVER=smtp.gmail.com
# MAIL_PORT=587
# MAIL_USE_TLS=true
# MAIL_USERNAME=votre@gmail.com
# MAIL_PASSWORD=xxxx_xxxx_xxxx_xxxx   ← App Password Gmail
# MAIL_DEFAULT_SENDER=noreply@kengni-finance.com
# NAS_ADMIN_NOTIFICATION_EMAIL=admin@kengni-finance.com
#
# # NAS
# NAS_UPLOAD_FOLDER=/chemin/absolu/vers/uploads/nas/
# NAS_MAX_FILE_SIZE=524288000         ← 500 Mo
# BASE_URL=https://kengni-finance.com
#
# ═══════════════════════════════════════════════════════════════
# ROUTES DISPONIBLES après intégration
# ═══════════════════════════════════════════════════════════════
#
# [Visiteur — public]
#   GET  /nas/access                → Formulaire demande d'accès
#   POST /nas/access                → Soumettre la demande
#   GET  /nas/access/<token>        → Liste des fichiers (token requis)
#   GET  /nas/download/<token>/<id> → Télécharger un fichier
#   GET  /nas/preview/<token>/<id>  → Prévisualiser en ligne
#
# [Admin — session requise]
#   GET  /nas/admin                         → Dashboard
#   POST /nas/admin/upload                  → Upload fichier(s)
#   POST /nas/admin/files/edit/<id>         → Modifier métadonnées
#   POST /nas/admin/files/delete/<id>       → Supprimer fichier
#   POST /nas/admin/requests/approve/<id>   → Approuver + envoyer token
#   POST /nas/admin/requests/reject/<id>    → Rejeter demande
#   POST /nas/admin/requests/revoke/<id>    → Révoquer token
#   GET  /nas/admin/stats                   → Stats JSON (AJAX)
# ═══════════════════════════════════════════════════════════════
