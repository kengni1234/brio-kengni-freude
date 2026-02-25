# 🚀 GUIDE D'INSTALLATION RAPIDE - Kengni Finance v2.0.1

## ⚡ Installation en 3 Étapes (5 minutes)

### 1️⃣ Extraction
```bash
unzip kengni_finance_v2_complete.zip
cd kengni_finance_v2_complete
```

### 2️⃣ Installation Automatique
```bash
chmod +x install.sh
./install.sh
```

### 3️⃣ Lancement
**4 Méthodes au choix :**

**A) Raccourci Bureau** (Le plus simple)
- Double-cliquez sur l'icône **KengniFinance** sur votre bureau
- Le terminal s'ouvrira automatiquement
- L'application démarrera

**B) Script de démarrage**
```bash
./start_kengni_finance.sh
```

**C) Ligne de commande**
```bash
source venv/bin/activate
python3 app.py
```

**D) Alias rapide** (après redémarrage terminal)
```bash
kengni-finance
```

### 4️⃣ Accès
Ouvrez votre navigateur : **http://localhost:5001**

---

## 👤 Première Connexion

### Option 1 : Créer votre compte (Recommandé) ✨
1. Cliquez sur **"Créer un compte"**
2. Remplissez le formulaire :
   - Nom d'utilisateur (min. 3 caractères)
   - Email
   - Mot de passe (min. 6 caractères)
   - Devise préférée
3. Cliquez sur **"Créer mon compte"**
4. ✅ Vous êtes connecté automatiquement !

### Option 2 : Compte par défaut
- **Email** : fabrice.kengni@icloud.com
- **Mot de passe** : kengni
- ⚠️ **Changez le mot de passe dans Paramètres !**

---

## 🎯 Fonctionnalités Principales

### 💰 Gestion Financière
- Suivi complet des revenus, dépenses, créances, dettes
- Catégorisation avancée
- Analyse automatique IA

### 📈 Trading avec IA
- Exécution de trades
- Portfolio en temps réel
- Journal avec images
- Score trader (0-100)

### 🤖 Intelligence Artificielle
- Score trader détaillé
- Détection FOMO, Revenge Trading, Overtrading
- Assistant IA conversationnel
- Recommandations personnalisées

### 🎨 Interface Moderne
- Thème sombre/clair
- Design responsive
- Animations fluides

---

## 🖥️ Raccourci Bureau

Le script d'installation crée automatiquement :
- **Icône sur le bureau** : KengniFinance.desktop
- **Entrée dans le menu Applications** : Office > Kengni Finance
- **Alias terminal** : `kengni-finance`

Pour lancer depuis le bureau :
1. Double-cliquez sur l'icône
2. Le terminal s'ouvre
3. L'application démarre
4. Ouvrez http://localhost:5001

---

## 📱 Compatibilité

- ✅ Parrot OS
- ✅ Debian / Ubuntu
- ✅ Linux Mint
- ✅ Kali Linux
- ⚠️ Windows (avec WSL)
- ⚠️ macOS (non testé)

---

## 🛠️ Dépannage Rapide

### Problème 1 : Port 5001 déjà utilisé
**Solution** : Changez le port
```bash
nano app.py
# Ligne 1702 : changez port=5001 en port=5002
```

### Problème 2 : Module non trouvé
**Solution** : Réinstallez les dépendances
```bash
source venv/bin/activate
pip install -r requirements.txt --force-reinstall
```

### Problème 3 : Erreur base de données
**Solution** : Réinitialisez
```bash
rm kengni_finance.db
python3 -c "from app import init_db; init_db()"
```

### Problème 4 : Raccourci bureau ne fonctionne pas
**Solution** : Rendez-le exécutable
```bash
chmod +x ~/Desktop/KengniFinance.desktop
```

---

## 📊 Utilisation Recommandée

### Premier Usage
1. ✅ Créez votre compte ou connectez-vous
2. ✅ Configurez vos préférences (Paramètres)
3. ✅ Ajoutez vos premières transactions financières
4. ✅ Exécutez quelques trades
5. ✅ Consultez votre score trader

### Routine Quotidienne
1. 📊 Dashboard : Vue d'ensemble
2. 💰 Finances : Ajouter transactions
3. 📈 Trading : Exécuter trades
4. 📓 Journal : Documenter avec images
5. 🤖 Analyse IA : Consulter recommandations
6. 💬 Assistant IA : Poser questions

---

## 🔐 Sécurité

- ✅ Mots de passe hashés
- ✅ Sessions sécurisées
- ✅ Isolation des données
- ✅ Validation stricte
- ⚠️ **Changez le mot de passe par défaut !**

---

## 📧 Support

**Email** : fabrice.kengni@icloud.com  
**GitHub** : https://github.com/kengni

---

## 🎉 C'est parti !

Vous êtes prêt à :
- 💰 Gérer vos finances intelligemment
- 📈 Améliorer votre trading
- 🧠 Comprendre votre psychologie
- 🚀 Atteindre vos objectifs financiers

**Bon trading ! 📈💰**

---

**Kengni Finance v2.0.1** - © 2025 - Tous droits réservés
