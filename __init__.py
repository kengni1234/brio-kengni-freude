"""
Blueprint NAS — Serveur de fichiers privés avec accès par token
Kengni Finance
"""
from flask import Blueprint

nas_bp = Blueprint(
    'nas',
    __name__,
    url_prefix='/nas',
    template_folder='templates'
)

from . import routes  # noqa: E402, F401
