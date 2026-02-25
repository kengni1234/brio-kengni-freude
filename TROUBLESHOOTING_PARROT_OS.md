# 🔧 GUIDE DE DÉPANNAGE - PARROT OS

## ❌ Erreur: Permission denied lors de l'installation

### Problème
```
Error: [Errno 13] Permission denied: '.../venv'
```

### Solution Rapide

**Option 1: Déplacer le dossier (RECOMMANDÉ)**
```bash
# Le problème vient des espaces et parenthèses dans le nom du dossier
# Déplacez-le dans un dossier simple

mv "kengni_finance_v2.1_READY (2)" ~/kengni_finance
cd ~/kengni_finance/kengni_finance_v2_complete
chmod +x install.sh
./install.sh
```

**Option 2: Installation manuelle**
```bash
# 1. Installer python3-venv
sudo apt-get update
sudo apt-get install -y python3-venv python3-full

# 2. Créer l'environnement virtuel
python3 -m venv venv

# 3. Activer l'environnement
source venv/bin/activate

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Initialiser la base de données
python3 -c "from app import init_db; init_db()"

# 6. Lancer l'application
python3 app.py
```

**Option 3: Installation système (sans venv)**
```bash
# Installer les packages système
sudo apt-get install -y python3-flask python3-pandas python3-pil python3-requests

# Installer les packages manquants avec pip
pip3 install --break-system-packages yfinance reportlab python-dotenv Flask-CORS

# Initialiser la base
python3 -c "from app import init_db; init_db()"

# Lancer
python3 app.py
```

---

## ❌ Erreur: externally-managed-environment

### Problème
```
error: externally-managed-environment
× This environment is externally managed
```

### Solution
Ceci est normal sur Parrot OS / Debian 12+. Le script d'installation a été mis à jour pour gérer cela automatiquement.

**Utilisez le nouveau script d'installation:**
```bash
chmod +x install.sh
./install.sh
```

Le script détectera automatiquement le problème et:
1. Essaiera de créer un venv
2. Si ça échoue, utilisera `--break-system-packages`
3. Installera les packages en mode utilisateur

---

## 🚀 LANCEMENT RAPIDE (Sans installation)

Si vous voulez juste tester rapidement:

```bash
# 1. Installer les dépendances système
sudo apt-get install -y python3-flask python3-pandas python3-pil \
    python3-requests python3-werkzeug python3-numpy

# 2. Installer les packages manquants
pip3 install --break-system-packages yfinance reportlab Flask-CORS

# 3. Initialiser la base
python3 << EOF
from app import init_db
init_db()
EOF

# 4. Lancer
python3 app.py
```

Puis ouvrez: **http://localhost:5001**

---

## 🔍 VÉRIFICATION DE L'INSTALLATION

### Vérifier Python et pip
```bash
python3 --version  # Doit afficher Python 3.11.x
pip3 --version     # Doit afficher pip 23.x
```

### Vérifier les packages
```bash
python3 << EOF
import flask
import pandas
import yfinance
from reportlab.pdfgen import canvas
print("✅ Tous les packages sont installés!")
EOF
```

### Vérifier la base de données
```bash
ls -lh kengni_finance.db
# Doit afficher un fichier d'environ 70K
```

---

## 📝 CRÉER UN LANCEUR MANUEL

Si le script d'installation échoue complètement, créez un lanceur manuel:

```bash
# 1. Créer le fichier
nano ~/kengni-finance-launcher.sh

# 2. Coller ce contenu:
#!/bin/bash
cd ~/kengni_finance/kengni_finance_v2_complete
python3 app.py

# 3. Sauvegarder (Ctrl+X, puis Y, puis Entrée)

# 4. Rendre exécutable
chmod +x ~/kengni-finance-launcher.sh

# 5. Lancer
~/kengni-finance-launcher.sh
```

---

## 🖥️ CRÉER UN RACCOURCI BUREAU MANUEL

```bash
# 1. Créer le fichier
nano ~/Desktop/KengniFinance.desktop

# 2. Coller ce contenu (MODIFIEZ LE CHEMIN):
[Desktop Entry]
Version=1.0
Type=Application
Name=Kengni Finance
Comment=Financial Management & Trading
Exec=bash -c "cd /home/VOTRE_USER/kengni_finance/kengni_finance_v2_complete && python3 app.py"
Icon=/home/VOTRE_USER/kengni_finance/kengni_finance_v2_complete/static/img/logo.jpeg
Terminal=true
Categories=Office;Finance;

# 3. Remplacez VOTRE_USER par votre nom d'utilisateur
# Exemple: /home/keni/kengni_finance/...

# 4. Sauvegarder et rendre exécutable
chmod +x ~/Desktop/KengniFinance.desktop
```

---

## ⚠️ ERREURS COURANTES ET SOLUTIONS

### Port 5001 déjà utilisé
```bash
# Trouver le processus
sudo lsof -i :5001

# Tuer le processus
sudo kill -9 <PID>

# OU changer le port dans app.py (dernière ligne):
# app.run(debug=True, host='0.0.0.0', port=5002)
```

### Module 'flask' non trouvé
```bash
pip3 install --break-system-packages flask
```

### Module 'reportlab' non trouvé
```bash
pip3 install --break-system-packages reportlab
```

### Module 'yfinance' non trouvé
```bash
pip3 install --break-system-packages yfinance
```

### Base de données verrouillée
```bash
rm kengni_finance.db
python3 -c "from app import init_db; init_db()"
```

---

## 💡 ASTUCE: Installation dans un nouveau dossier

Pour éviter tous les problèmes de permissions:

```bash
# 1. Créer un nouveau dossier propre
mkdir -p ~/kengni_finance
cd ~/kengni_finance

# 2. Extraire l'archive directement ici
tar -xzf ~/Downloads/kengni_finance_v2.1_READY.tar.gz

# 3. Entrer dans le dossier
cd kengni_finance_v2_complete

# 4. Lancer l'installation
chmod +x install.sh
./install.sh
```

---

## 📧 AIDE SUPPLÉMENTAIRE

Si aucune solution ne fonctionne:

1. Copiez le message d'erreur complet
2. Notez votre version de Parrot OS (`cat /etc/os-release`)
3. Contactez: **fabrice.kengni@icloud.com**

---

## ✅ VÉRIFICATION FINALE

Une fois l'installation réussie, vous devriez voir:

```
====================================================================
✅ Installation completed successfully!
====================================================================

To start the application:
   ./start_kengni_finance.sh

   Then open browser: http://localhost:5001
```

Si vous voyez ce message, tout fonctionne! 🎉
