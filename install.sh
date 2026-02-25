#!/bin/bash
# ============================================
# Script d'installation - Kengni Finance
# Raccourci bureau + Démarrage automatique
# Compatible Parrot OS / Debian / Ubuntu
# ============================================

set -e

# ---- Variables à personnaliser ----
APP_DIR="$(cd "$(dirname "$0")" && pwd)"   # Dossier du script = dossier de l'app
APP_FILE="$APP_DIR/app.py"
USER_NAME="$(whoami)"
PYTHON_BIN="$(which python3)"
SERVICE_NAME="kengni-finance"
# ------------------------------------

echo "================================================"
echo "  Installation Kengni Finance"
echo "================================================"
echo "Dossier app     : $APP_DIR"
echo "Utilisateur     : $USER_NAME"
echo "Python          : $PYTHON_BIN"
echo ""

# 1. Créer le raccourci bureau
DESKTOP_FILE="$HOME/Desktop/kengni-finance.desktop"

cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Kengni Finance
Comment=Application de gestion financière et trading avec IA
Exec=bash -c "cd $APP_DIR && $PYTHON_BIN $APP_FILE && sleep 3 && xdg-open http://localhost:5001"
Icon=utilities-finance
Terminal=false
Categories=Finance;Office;
StartupNotify=true
EOF

# Rendre le fichier .desktop exécutable
chmod +x "$DESKTOP_FILE"
# Marquer comme approuvé (nécessaire sur certains environnements XFCE/MATE)
gio set "$DESKTOP_FILE" metadata::trusted true 2>/dev/null || true

echo "[OK] Raccourci bureau créé : $DESKTOP_FILE"

# 2. Créer le service systemd pour le démarrage automatique
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

sudo bash -c "cat > $SERVICE_FILE" <<EOF
[Unit]
Description=Kengni Finance - Gestion financière et trading IA
After=network.target

[Service]
Type=simple
User=$USER_NAME
WorkingDirectory=$APP_DIR
ExecStart=$PYTHON_BIN $APP_FILE
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

echo "[OK] Fichier service créé : $SERVICE_FILE"

# 3. Activer et démarrer le service
sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"
sudo systemctl start "$SERVICE_NAME"

echo ""
echo "================================================"
echo "  Installation terminée avec succès !"
echo "================================================"
echo ""
echo "✅ Raccourci bureau    : ~/Desktop/kengni-finance.desktop"
echo "✅ Service systemd     : $SERVICE_NAME (actif)"
echo "✅ URL de l'application: http://localhost:5001"
echo ""
echo "Commandes utiles :"
echo "  sudo systemctl status $SERVICE_NAME    # Voir l'état"
echo "  sudo systemctl stop $SERVICE_NAME      # Arrêter"
echo "  sudo systemctl restart $SERVICE_NAME   # Redémarrer"
echo "  journalctl -u $SERVICE_NAME -f         # Voir les logs"
echo ""
