#!/bin/bash
# ══════════════════════════════════════════════════════════════
#  Kengni Finance — Raccourci bureau avec logo k-ni Htech
# ══════════════════════════════════════════════════════════════

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'
CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'

echo ""
echo -e "${CYAN}${BOLD}══════════════════════════════════════════════${NC}"
echo -e "${CYAN}${BOLD}   🚀 k-ni Htech — Installation Raccourci     ${NC}"
echo -e "${CYAN}${BOLD}══════════════════════════════════════════════${NC}"
echo ""

# ── Chemin de l'application ──
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$SCRIPT_DIR"

if [ ! -f "$APP_DIR/app.py" ]; then
    echo -e "${YELLOW}⚠️  Entrez le chemin complet de kengni-finance-final:${NC}"
    read -rp "   Chemin: " APP_DIR
    if [ ! -f "$APP_DIR/app.py" ]; then
        echo -e "${RED}❌ app.py introuvable. Abandon.${NC}"; exit 1
    fi
fi
echo -e "${GREEN}✅ Application: $APP_DIR${NC}"

# ── Copier le logo dans static/img/ ──
LOGO_SRC="$APP_DIR/logo.jpeg"
LOGO_DEST="$APP_DIR/static/img/logo.jpeg"
mkdir -p "$APP_DIR/static/img"

if [ -f "$LOGO_SRC" ]; then
    cp "$LOGO_SRC" "$LOGO_DEST"
    echo -e "${GREEN}✅ Logo copié dans static/img/${NC}"
elif [ -f "$LOGO_DEST" ]; then
    echo -e "${GREEN}✅ Logo déjà présent: $LOGO_DEST${NC}"
else
    echo -e "${YELLOW}⚠️  Placez logo.jpeg dans $APP_DIR puis relancez${NC}"
fi
ICON_PATH="$LOGO_DEST"

# ── Détecter le bureau ──
if   [ -d "$HOME/Bureau" ];     then DESK="$HOME/Bureau"
elif [ -d "$HOME/Desktop" ];    then DESK="$HOME/Desktop"
elif [ -d "$HOME/Escritorio" ]; then DESK="$HOME/Escritorio"
else DESK="$HOME"; fi
echo -e "${CYAN}📂 Bureau: $DESK${NC}"

# ── Créer le .desktop ──
DESKTOP_FILE="$DESK/KengniFinance.desktop"
cat > "$DESKTOP_FILE" << DEOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Kengni Finance
GenericName=Gestion Financière & Trading
Comment=k-ni chez Htech-training — Finance & Trading avec IA
Exec=bash -c "cd '$APP_DIR' && python3 app.py & sleep 3 && xdg-open http://localhost:5001"
Icon=$ICON_PATH
Terminal=false
Categories=Office;Finance;
StartupNotify=true
Keywords=finance;trading;kengni;kni;htech;
DEOF

chmod +x "$DESKTOP_FILE"
gio set "$DESKTOP_FILE" metadata::trusted true 2>/dev/null || true
echo -e "${GREEN}✅ Raccourci bureau créé avec votre logo k-ni${NC}"

# ── Menu Applications ──
mkdir -p "$HOME/.local/share/applications"
cp "$DESKTOP_FILE" "$HOME/.local/share/applications/KengniFinance.desktop"
echo -e "${GREEN}✅ Ajouté au menu Applications${NC}"

# ── Commande rapide ──
mkdir -p "$HOME/.local/bin"
cat > "$HOME/.local/bin/kengni-finance" << LCMD
#!/bin/bash
cd "$APP_DIR" && python3 app.py & sleep 3 && xdg-open http://localhost:5001
LCMD
chmod +x "$HOME/.local/bin/kengni-finance"
echo -e "${GREEN}✅ Commande: kengni-finance${NC}"

# ── Alias ──
ALIAS_LINE="alias kengni-finance='cd \"$APP_DIR\" && python3 app.py & sleep 3 && xdg-open http://localhost:5001'"
for RC in "$HOME/.bashrc" "$HOME/.zshrc"; do
    [ -f "$RC" ] && ! grep -q "kengni-finance" "$RC" && {
        echo -e "\n# Kengni Finance\n$ALIAS_LINE" >> "$RC"
        echo -e "${GREEN}✅ Alias ajouté dans $(basename $RC)${NC}"
    }
done

echo ""
echo -e "${CYAN}${BOLD}══════════════════════════════════════════════${NC}"
echo -e "${GREEN}${BOLD}🎉 Raccourci avec logo k-ni installé!${NC}"
echo -e "${CYAN}${BOLD}══════════════════════════════════════════════${NC}"
echo ""
echo -e "  ${YELLOW}1.${NC} Double-clic icône ${BOLD}KengniFinance${NC} sur le bureau"
echo -e "  ${YELLOW}2.${NC} Menu Applications → Finance"
echo -e "  ${YELLOW}3.${NC} Terminal: ${CYAN}kengni-finance${NC}  (après source ~/.bashrc)"
echo ""
echo -e "${YELLOW}Si l'icône ne s'affiche pas:${NC}"
echo -e "  Clic droit → ${BOLD}Autoriser l'exécution${NC}"
echo ""
