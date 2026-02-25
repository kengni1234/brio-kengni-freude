# 🐧 GUIDE POUR PARROT OS / DEBIAN

## ❌ Erreur rencontrée
```bash
python fix_templates.py
bash: python : commande introuvable
```

## ✅ SOLUTION RAPIDE

Sur Parrot OS/Debian, utilisez `python3` au lieu de `python` :

```bash
python3 fix_templates.py
```

---

## 🚀 SOLUTION AUTOMATIQUE (RECOMMANDÉE)

J'ai créé un script qui détecte automatiquement votre système :

```bash
# Rendre le script exécutable
chmod +x auto_fix.sh

# Exécuter la correction automatique
./auto_fix.sh
```

Ce script va :
- ✅ Détecter automatiquement `python3` ou `python`
- ✅ Créer tous les templates HTML manquants
- ✅ Vérifier les dépendances
- ✅ Tout configurer pour vous

---

## 📋 COMMANDES ÉTAPE PAR ÉTAPE

### Étape 1 : Créer les templates
```bash
python3 fix_templates.py
```

### Étape 2 : Installer les dépendances (si nécessaire)
```bash
# Avec pip3
pip3 install flask werkzeug pandas yfinance numpy pillow

# OU avec le fichier requirements.txt
pip3 install -r requirements.txt
```

### Étape 3 : Lancer l'application
```bash
python3 app.py
```

---

## 🔧 SCRIPT DE LANCEMENT AUTOMATIQUE

Pour simplifier le lancement, utilisez le script fourni :

```bash
# Rendre le script exécutable
chmod +x start.sh

# Lancer l'application
./start.sh
```

---

## 📦 INSTALLATION COMPLÈTE (depuis zéro)

Si vous n'avez rien installé :

```bash
# 1. Installer Python et pip (si pas déjà installés)
sudo apt update
sudo apt install python3 python3-pip python3-venv -y

# 2. Créer un environnement virtuel (recommandé)
python3 -m venv venv
source venv/bin/activate

# 3. Installer les dépendances
pip3 install -r requirements.txt

# 4. Créer les templates
python3 fix_templates.py

# 5. Lancer l'application
python3 app.py
```

---

## 🎯 COMMANDES RAPIDES

### Tout corriger en une commande :
```bash
chmod +x auto_fix.sh && ./auto_fix.sh
```

### Lancer directement :
```bash
chmod +x start.sh && ./start.sh
```

---

## 🐛 DÉPANNAGE

### Python n'est pas trouvé
```bash
# Installer Python 3
sudo apt update
sudo apt install python3 python3-pip -y
```

### pip n'est pas trouvé
```bash
# Installer pip pour Python 3
sudo apt install python3-pip -y
```

### Problème de permissions
```bash
# Donner les droits d'exécution
chmod +x *.sh

# Ou pour un fichier spécifique
chmod +x auto_fix.sh
chmod +x start.sh
```

### Module Flask introuvable
```bash
# Installer Flask et dépendances
pip3 install --user flask werkzeug pandas yfinance numpy pillow

# OU avec sudo si nécessaire
sudo pip3 install flask werkzeug pandas yfinance numpy pillow
```

### L'application ne démarre pas sur le port 5001
```bash
# Vérifier si le port est utilisé
sudo lsof -i :5001

# Tuer le processus si nécessaire
sudo kill -9 <PID>

# Ou changer le port dans app.py (dernière ligne)
# Remplacez port=5001 par port=5002 ou autre
```

---

## 📁 FICHIERS FOURNIS

| Fichier | Utilisation | Commande |
|---------|-------------|----------|
| `fix_templates.py` | Crée tous les templates | `python3 fix_templates.py` |
| `auto_fix.sh` | Correction automatique complète | `./auto_fix.sh` |
| `start.sh` | Lance l'application | `./start.sh` |
| `requirements.txt` | Liste des dépendances | `pip3 install -r requirements.txt` |

---

## ✅ VÉRIFICATION FINALE

Après avoir suivi les étapes, vérifiez :

```bash
# 1. Python est installé
python3 --version
# Devrait afficher: Python 3.x.x

# 2. Les templates sont créés
ls -la templates/
# Devrait lister 15 fichiers .html

# 3. Flask est installé
python3 -c "import flask; print(flask.__version__)"
# Devrait afficher la version de Flask

# 4. L'application peut démarrer
python3 app.py
# L'application devrait se lancer sur http://localhost:5001
```

---

## 🎉 SUCCÈS !

Une fois que tout fonctionne, vous verrez :
```
======================================================================
🚀 Kengni Finance v2.0 - VERSION CORRIGÉE
======================================================================
✅ Database initialized successfully
✅ Default templates created successfully
✅ Default user created

📋 Application prête:
   🌐 URL: http://localhost:5001
   👤 Email: fabrice.kengni@icloud.com
   🔐 Password: kengni
======================================================================
```

Ouvrez votre navigateur sur `http://localhost:5001` et connectez-vous !

---

## 💡 ASTUCE PARROT OS

Sur Parrot OS, vous pouvez créer un alias permanent pour utiliser `python` au lieu de `python3` :

```bash
# Ajouter à votre ~/.bashrc ou ~/.zshrc
echo "alias python=python3" >> ~/.bashrc
echo "alias pip=pip3" >> ~/.bashrc

# Recharger la configuration
source ~/.bashrc

# Maintenant vous pouvez utiliser
python fix_templates.py  # Au lieu de python3
```

---

**🚀 Tout est prêt ! Bon développement !**
