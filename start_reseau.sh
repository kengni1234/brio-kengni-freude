#!/bin/bash
# ══════════════════════════════════════════════════════════════
#  Kengni Finance — Lancement Réseau Local
#  Accès depuis tous les appareils du réseau WiFi/LAN
# ══════════════════════════════════════════════════════════════

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'
BOLD='\033[1m'; RED='\033[0;31m'; NC='\033[0m'

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT=5001

echo ""
echo -e "${CYAN}${BOLD}╔══════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}${BOLD}║   🌐 Kengni Finance — Réseau Local           ║${NC}"
echo -e "${CYAN}${BOLD}╚══════════════════════════════════════════════╝${NC}"
echo ""

# ── Vérifier si déjà en cours ──
if lsof -i :$PORT &>/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Port $PORT déjà utilisé. Arrêt de l'ancien processus...${NC}"
    pkill -f "app.py" 2>/dev/null
    sleep 1
fi

# ── Récupérer toutes les IPs locales ──
echo -e "${BOLD}📡 Adresses IP détectées sur ce PC:${NC}"
echo ""

# IP WiFi
WIFI_IP=$(ip addr show 2>/dev/null | grep -E "inet " | grep -v "127.0.0.1" | awk '{print $2}' | cut -d/ -f1 | head -5)

if [ -z "$WIFI_IP" ]; then
    WIFI_IP=$(hostname -I 2>/dev/null | tr ' ' '\n' | grep -v "127.0.0.1" | head -1)
fi

# Afficher toutes les IPs disponibles
ALL_IPS=$(ip addr show 2>/dev/null | grep "inet " | grep -v "127.0.0.1" | awk '{print $2}' | cut -d/ -f1)
MAIN_IP=""

for ip in $ALL_IPS; do
    IFACE=$(ip addr show 2>/dev/null | grep -B2 "inet $ip" | head -1 | awk '{print $2}' | tr -d ':')
    echo -e "   ${GREEN}●${NC} $ip  ${YELLOW}($IFACE)${NC}"
    if [ -z "$MAIN_IP" ]; then MAIN_IP="$ip"; fi
done

if [ -z "$MAIN_IP" ]; then
    MAIN_IP="localhost"
    echo -e "   ${RED}● Aucune IP réseau trouvée — mode local uniquement${NC}"
fi

echo ""
echo -e "${CYAN}${BOLD}══════════════════════════════════════════════${NC}"
echo -e "${BOLD}🔗 URLs d'accès depuis le réseau:${NC}"
echo ""
echo -e "  ${GREEN}● Ce PC (local):${NC}        http://localhost:$PORT"
for ip in $ALL_IPS; do
    echo -e "  ${GREEN}● Réseau WiFi/LAN:${NC}      ${CYAN}${BOLD}http://$ip:$PORT${NC}"
done
echo ""
echo -e "${BOLD}👤 Identifiants:${NC}"
echo -e "  Email:     fabrice.kengni@icloud.com"
echo -e "  Password:  kengni"
echo -e "${CYAN}${BOLD}══════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}📱 Sur téléphone/tablette Android:${NC}"
echo -e "   Ouvrez Chrome/Firefox → tapez l'URL ci-dessus"
echo ""
echo -e "${YELLOW}💻 Sur PC Windows du même réseau:${NC}"
echo -e "   Ouvrez Chrome → tapez l'URL ci-dessus"
echo ""
echo -e "${YELLOW}🍎 Sur iPhone/iPad:${NC}"
echo -e "   Ouvrez Safari → tapez l'URL ci-dessus"
echo ""
echo -e "${RED}⚠️  IMPORTANT: Tous les appareils doivent être${NC}"
echo -e "${RED}   connectés au MÊME WiFi/réseau!${NC}"
echo ""
echo -e "${YELLOW}Appuyez sur Ctrl+C pour arrêter le serveur${NC}"
echo ""

# ── Lancer l'application ──
cd "$APP_DIR"
python3 app.py
