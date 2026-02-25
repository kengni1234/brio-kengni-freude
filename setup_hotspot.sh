#!/bin/bash
# ══════════════════════════════════════════════════════════════
#  Kengni Finance — Configuration Point d'Accès Mobile
#  Windows + Linux + Android + iPhone — Raccourcis + Navigateur
# ══════════════════════════════════════════════════════════════

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'
BOLD='\033[1m'; RED='\033[0;31m'; BLUE='\033[0;34m'; NC='\033[0m'

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT=5001

clear
echo ""
echo -e "${CYAN}${BOLD}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}${BOLD}║  📡 Kengni Finance — Point d'Accès Mobile        ║${NC}"
echo -e "${CYAN}${BOLD}║  Windows · Linux · Android · iPhone              ║${NC}"
echo -e "${CYAN}${BOLD}╚══════════════════════════════════════════════════╝${NC}"
echo ""

# ══════════════════════════════════════════════
# ÉTAPE 1 — Ouvrir le pare-feu
# ══════════════════════════════════════════════
echo -e "${BOLD}[1/5] 🔓 Ouverture du pare-feu...${NC}"

if command -v ufw &>/dev/null; then
    sudo ufw allow $PORT/tcp comment "Kengni Finance" &>/dev/null 2>&1
    sudo ufw --force enable &>/dev/null 2>&1
    echo -e "  ${GREEN}✅ Port $PORT ouvert dans UFW (Parrot OS)${NC}"
fi
sudo iptables -I INPUT -p tcp --dport $PORT -j ACCEPT &>/dev/null 2>&1
echo -e "  ${GREEN}✅ Règle iptables OK${NC}"

# ══════════════════════════════════════════════
# ÉTAPE 2 — Détecter l'IP du hotspot
# ══════════════════════════════════════════════
echo ""
echo -e "${BOLD}[2/5] 📡 Détection IP sur le hotspot mobile...${NC}"

# Sur hotspot mobile, l'interface est souvent usb0, wlan0 ou enp
# On prend la meilleure IP disponible
MAIN_IP=$(ip route get 8.8.8.8 2>/dev/null | grep -oP 'src \K\S+' | head -1)
[ -z "$MAIN_IP" ] && MAIN_IP=$(ip addr show 2>/dev/null | grep "inet " | grep -v "127.0.0.1" | awk '{print $2}' | cut -d/ -f1 | head -1)
[ -z "$MAIN_IP" ] && MAIN_IP=$(hostname -I 2>/dev/null | awk '{print $1}')
[ -z "$MAIN_IP" ] && MAIN_IP="192.168.43.X"

APP_URL="http://$MAIN_IP:$PORT"

echo -e "  ${GREEN}✅ IP détectée: ${CYAN}${BOLD}$MAIN_IP${NC}"
echo ""
echo -e "  ${BOLD}Toutes les interfaces:${NC}"
ip addr show 2>/dev/null | grep "inet " | grep -v "127.0.0.1" | while read -r line; do
    ip_addr=$(echo "$line" | awk '{print $2}' | cut -d/ -f1)
    echo -e "  ${GREEN}  ●${NC} http://$ip_addr:$PORT"
done

# ══════════════════════════════════════════════
# ÉTAPE 3 — Générer QR Code ASCII
# ══════════════════════════════════════════════
echo ""
echo -e "${BOLD}[3/5] 📱 Génération QR Code...${NC}"

if command -v qrencode &>/dev/null; then
    echo ""
    echo -e "${CYAN}  Scannez ce QR code avec votre téléphone:${NC}"
    echo ""
    qrencode -t ANSIUTF8 "$APP_URL"
    echo ""
    echo -e "  ${GREEN}✅ QR Code généré${NC}"
else
    echo -e "  ${YELLOW}  Installation de qrencode...${NC}"
    sudo apt-get install -y qrencode &>/dev/null 2>&1
    if command -v qrencode &>/dev/null; then
        echo ""
        qrencode -t ANSIUTF8 "$APP_URL"
        echo -e "  ${GREEN}✅ QR Code généré${NC}"
    else
        echo -e "  ${YELLOW}  ⚠️ qrencode non dispo — utilisez l'URL manuellement${NC}"
    fi
fi

# ══════════════════════════════════════════════
# ÉTAPE 4 — Créer les fichiers d'accès
# ══════════════════════════════════════════════
echo ""
echo -e "${BOLD}[4/5] 📁 Création des fichiers d'accès...${NC}"

ICON_PATH="$APP_DIR/static/img/logo.jpeg"
[ ! -f "$ICON_PATH" ] && ICON_PATH="applications-office"

# Détecter bureau
if   [ -d "$HOME/Bureau" ];     then DESK="$HOME/Bureau"
elif [ -d "$HOME/Desktop" ];    then DESK="$HOME/Desktop"
else DESK="$HOME"; fi

# ── .desktop bureau (ouvre directement dans navigateur) ──
cat > "$DESK/KengniFinance.desktop" << DEOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Kengni Finance
GenericName=Finance & Trading k-ni
Comment=Ouvre Kengni Finance — http://$MAIN_IP:$PORT
Exec=bash -c "cd '$APP_DIR' && python3 app.py & sleep 3 && xdg-open $APP_URL"
Icon=$ICON_PATH
Terminal=false
Categories=Office;Finance;
StartupNotify=true
DEOF
chmod +x "$DESK/KengniFinance.desktop"
gio set "$DESK/KengniFinance.desktop" metadata::trusted true 2>/dev/null || true
echo -e "  ${GREEN}✅ Raccourci bureau Linux créé${NC}"

# ── Fichier .url pour Windows ──
cat > "$APP_DIR/Kengni-Finance-Windows.url" << WEOF
[InternetShortcut]
URL=$APP_URL
IconFile=logo.jpeg
WEOF
echo -e "  ${GREEN}✅ Raccourci Windows (.url) créé${NC}"

# ── Page HTML d'accès rapide (fonctionne sur TOUS les appareils) ──
cat > "$APP_DIR/OUVRIR_KENGNI_FINANCE.html" << HEOF
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Kengni Finance — Accès Réseau</title>
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: linear-gradient(135deg, #0f1419 0%, #1a1a2e 50%, #16213e 100%);
    min-height: 100vh; display:flex; align-items:center; justify-content:center;
    color: white;
  }
  .card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(0,212,170,0.3);
    border-radius: 24px; padding: 3rem 2.5rem;
    text-align: center; max-width: 480px; width: 90%;
    backdrop-filter: blur(20px);
    box-shadow: 0 30px 80px rgba(0,0,0,0.5), 0 0 60px rgba(0,212,170,0.1);
  }
  .logo { font-size: 3.5rem; margin-bottom: 1rem; }
  h1 { font-size: 1.8rem; font-weight: 800; color: #00d4aa; margin-bottom: 0.3rem; }
  .sub { color: #a8b2d1; font-size: 0.9rem; margin-bottom: 2rem; }
  .url-box {
    background: rgba(0,212,170,0.1); border: 2px solid #00d4aa;
    border-radius: 14px; padding: 1.2rem 1.5rem;
    font-size: 1.3rem; font-weight: 800; color: #00d4aa;
    margin-bottom: 2rem; word-break: break-all;
    cursor: pointer; transition: all 0.3s;
  }
  .url-box:hover { background: rgba(0,212,170,0.2); transform: scale(1.02); }
  .btn-open {
    display: block; width: 100%;
    background: linear-gradient(135deg, #00d4aa, #00ff88);
    color: #0f1419; border: none; border-radius: 14px;
    padding: 1.1rem; font-size: 1.1rem; font-weight: 800;
    text-decoration: none; cursor: pointer;
    transition: all 0.3s; margin-bottom: 1rem;
  }
  .btn-open:hover { transform: translateY(-3px); box-shadow: 0 15px 35px rgba(0,212,170,0.4); color: #0f1419; }
  .creds {
    background: rgba(255,255,255,0.04); border-radius: 12px;
    padding: 1rem; margin-top: 1.5rem; font-size: 0.85rem; color: #a8b2d1;
  }
  .creds strong { color: #e0e6f8; }
  .devices { display: flex; justify-content: center; gap: 1rem; margin: 1.5rem 0; flex-wrap: wrap; }
  .dev { background: rgba(255,255,255,0.06); border-radius: 12px; padding: 0.6rem 1rem; font-size: 0.85rem; }
  .note { font-size: 0.78rem; color: #666; margin-top: 1rem; }
</style>
</head>
<body>
<div class="card">
  <div class="logo">📊</div>
  <h1>Kengni Finance</h1>
  <p class="sub">k-ni chez Htech-training — Finance & Trading avec IA</p>

  <div class="url-box" onclick="window.location.href='$APP_URL'" title="Cliquez pour ouvrir">
    🌐 $APP_URL
  </div>

  <a class="btn-open" href="$APP_URL">
    🚀 Ouvrir Kengni Finance
  </a>

  <div class="devices">
    <span class="dev">📱 Android</span>
    <span class="dev">🍎 iPhone</span>
    <span class="dev">💻 Windows</span>
    <span class="dev">🐧 Linux</span>
  </div>

  <div class="creds">
    <strong>Email:</strong> fabrice.kengni@icloud.com<br>
    <strong>Password:</strong> kengni
  </div>

  <p class="note">⚠️ Connectez-vous au même point d'accès mobile que le PC serveur</p>
</div>

<script>
  // Redirection automatique après 3 secondes
  setTimeout(() => { window.location.href = '$APP_URL'; }, 3000);
  // Compte à rebours
  let n = 3;
  const btn = document.querySelector('.btn-open');
  const timer = setInterval(() => {
    n--;
    btn.textContent = n > 0 ? '🚀 Redirection dans ' + n + 's...' : '🚀 Ouverture...';
    if (n <= 0) clearInterval(timer);
  }, 1000);
</script>
</body>
</html>
HEOF
echo -e "  ${GREEN}✅ Page HTML d'accès rapide créée${NC}"

# ── Fichier texte info ──
cat > "$APP_DIR/ACCES_RESEAU.txt" << TEOF
╔══════════════════════════════════════════════════╗
║    KENGNI FINANCE — ACCÈS POINT D'ACCÈS MOBILE   ║
╚══════════════════════════════════════════════════╝

URL D'ACCÈS: $APP_URL

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📱 ANDROID (Chrome/Firefox):
   1. Connectez-vous au hotspot du PC
   2. Ouvrez Chrome
   3. Tapez: $APP_URL
   OU: Scannez le QR code avec l'appareil photo

🍎 IPHONE/IPAD (Safari):
   1. Réglages → WiFi → Connectez au hotspot
   2. Ouvrez Safari
   3. Tapez: $APP_URL

💻 WINDOWS:
   1. Connectez au hotspot
   2. Copiez Kengni-Finance-Windows.url → Bureau Windows
   3. Double-clic sur le raccourci
   OU: Ouvrez Chrome → $APP_URL

🐧 LINUX (autre machine):
   1. Connectez au hotspot
   2. Firefox/Chrome → $APP_URL

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔐 IDENTIFIANTS:
   Email:    fabrice.kengni@icloud.com
   Password: kengni

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  CONDITIONS REQUISES:
   ✓ Ce PC (Parrot OS) est le serveur
   ✓ Tous les appareils sur LE MÊME hotspot
   ✓ Lancer: ./setup_hotspot.sh avant utilisation
   ✓ Ne pas éteindre ce PC pendant l'utilisation

Généré: $(date '+%d/%m/%Y à %H:%M')
IP serveur: $MAIN_IP:$PORT
TEOF
echo -e "  ${GREEN}✅ ACCES_RESEAU.txt mis à jour${NC}"

# ── Alias terminal ──
mkdir -p "$HOME/.local/bin"
cat > "$HOME/.local/bin/kengni-finance" << LCMD
#!/bin/bash
cd "$APP_DIR" && bash setup_hotspot.sh
LCMD
chmod +x "$HOME/.local/bin/kengni-finance"

for RC in "$HOME/.bashrc" "$HOME/.zshrc"; do
    [ -f "$RC" ] && ! grep -q "kengni-finance" "$RC" && {
        echo -e "\n# Kengni Finance Hotspot\nalias kengni-finance='cd \"$APP_DIR\" && bash setup_hotspot.sh'" >> "$RC"
        echo -e "  ${GREEN}✅ Alias ajouté dans $(basename $RC)${NC}"
    }
done

# ══════════════════════════════════════════════
# ÉTAPE 5 — Démarrer le serveur
# ══════════════════════════════════════════════
echo ""
echo -e "${BOLD}[5/5] 🚀 Démarrage du serveur...${NC}"
pkill -f "python3 app.py" 2>/dev/null; pkill -f "python app.py" 2>/dev/null
sleep 1

# ══════════════════════════════════════════════
# RÉSUMÉ
# ══════════════════════════════════════════════
echo ""
echo -e "${CYAN}${BOLD}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}${BOLD}║  ✅ PRÊT! Partagez cette URL sur votre hotspot   ║${NC}"
echo -e "${CYAN}${BOLD}╚══════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "  ${YELLOW}${BOLD}▶▶▶  $APP_URL  ◀◀◀${NC}"
echo ""
echo -e "${BOLD}📱 Android / iPhone:${NC}  Chrome/Safari → ${CYAN}$APP_URL${NC}"
echo -e "${BOLD}💻 Windows:${NC}           Chrome → ${CYAN}$APP_URL${NC}"
echo -e "${BOLD}🐧 Linux:${NC}             Firefox → ${CYAN}$APP_URL${NC}"
echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BOLD}Fichiers utiles créés:${NC}"
echo -e "  📄 ${CYAN}ACCES_RESEAU.txt${NC}              → infos complètes"
echo -e "  🌐 ${CYAN}OUVRIR_KENGNI_FINANCE.html${NC}    → page d'accueil réseau"
echo -e "  💻 ${CYAN}Kengni-Finance-Windows.url${NC}    → raccourci Windows"
echo -e "  🖥️  ${CYAN}~/Bureau/KengniFinance.desktop${NC} → raccourci Linux"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${RED}Ctrl+C pour arrêter le serveur${NC}"
echo ""

cd "$APP_DIR"
python3 app.py
