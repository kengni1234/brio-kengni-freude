#!/bin/bash
# ══════════════════════════════════════════════════════════
#  Installation COMPLÈTE — Kengni Finance Hotspot
#  Lance une seule fois, tout est configuré!
# ══════════════════════════════════════════════════════════
GREEN='\033[0;32m'; CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$SCRIPT_DIR"

echo -e "${CYAN}${BOLD}  Installation Kengni Finance Hotspot...${NC}"

# Rendre les scripts exécutables
chmod +x "$APP_DIR/setup_hotspot.sh"
chmod +x "$APP_DIR/start_reseau.sh"
echo -e "${GREEN}✅ Scripts configurés${NC}"

# Copier le logo si présent
[ -f "$APP_DIR/logo.jpeg" ] && {
    mkdir -p "$APP_DIR/static/img"
    cp "$APP_DIR/logo.jpeg" "$APP_DIR/static/img/logo.jpeg"
    echo -e "${GREEN}✅ Logo installé${NC}"
}

# Raccourci bureau
if   [ -d "$HOME/Bureau" ];  then DESK="$HOME/Bureau"
elif [ -d "$HOME/Desktop" ]; then DESK="$HOME/Desktop"
else DESK="$HOME"; fi

sed "s|/home/keni/Documents/Afin/bak/file/kengni-finance-final|$APP_DIR|g" \
    "$APP_DIR/KengniFinance.desktop" > "$DESK/KengniFinance.desktop"
chmod +x "$DESK/KengniFinance.desktop"
gio set "$DESK/KengniFinance.desktop" metadata::trusted true 2>/dev/null || true
echo -e "${GREEN}✅ Raccourci bureau créé${NC}"

# Menu Applications
mkdir -p "$HOME/.local/share/applications"
cp "$DESK/KengniFinance.desktop" "$HOME/.local/share/applications/"
echo -e "${GREEN}✅ Menu Applications mis à jour${NC}"

echo ""
echo -e "${CYAN}${BOLD}🎉 Prêt! Double-cliquez sur l'icône du bureau pour démarrer.${NC}"
echo ""
