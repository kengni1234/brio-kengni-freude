# 🎯 KENGNI FINANCE v2.1 - INSTRUCTIONS FINALES

## 📦 TÉLÉCHARGEMENT ET INSTALLATION

### Étape 1: Télécharger le fichier
Vous avez téléchargé: **kengni_finance_v2.1_FINAL.tar.gz** (94 KB)

### Étape 2: Extraire sur votre machine Parrot OS

```bash
# Allez dans le dossier où vous avez téléchargé le fichier
cd ~/Downloads  # ou le dossier de téléchargement

# Extraire l'archive
tar -xzf kengni_finance_v2.1_FINAL.tar.gz

# Entrer dans le dossier
cd kengni_finance_v2_complete
```

### Étape 3: Installer l'application

```bash
# Rendre le script d'installation exécutable
chmod +x install.sh

# Lancer l'installation (prend 2-3 minutes)
./install.sh
```

Le script va automatiquement:
- ✅ Vérifier Python 3 et pip
- ✅ Créer un environnement virtuel
- ✅ Installer toutes les dépendances (Flask, reportlab, etc.)
- ✅ Créer les dossiers nécessaires
- ✅ Initialiser la base de données
- ✅ Créer un raccourci sur votre bureau
- ✅ Configurer un alias de lancement rapide

### Étape 4: Lancer l'application

**4 méthodes au choix:**

#### Méthode 1: Raccourci Bureau (LE PLUS SIMPLE)
- Double-cliquez sur l'icône **"KengniFinance"** sur votre bureau
- Le terminal s'ouvre et l'application démarre
- Attendez que "Running on http://localhost:5001" s'affiche

#### Méthode 2: Script de lancement
```bash
./start_kengni_finance.sh
```

#### Méthode 3: Commandes manuelles
```bash
source venv/bin/activate
python3 app.py
```

#### Méthode 4: Alias rapide (après redémarrage du terminal)
```bash
kengni-finance
```

### Étape 5: Ouvrir dans le navigateur

**Ouvrez votre navigateur web** (Firefox, Chrome, etc.) et allez sur:
```
http://localhost:5001
```

---

## 🔑 PREMIÈRE CONNEXION

### Option 1: Créer VOTRE compte (RECOMMANDÉ)

1. Sur la page de connexion, cliquez sur **"Créer un compte"**
2. Remplissez:
   - Nom d'utilisateur (min. 3 caractères)
   - Email (votre email)
   - Mot de passe (min. 6 caractères)
   - Confirmer le mot de passe
   - Devise préférée (EUR, USD, XAF, etc.)
3. Cliquez sur **"Créer mon compte"**
4. ✅ Vous êtes automatiquement connecté!

### Option 2: Utiliser le compte par défaut

- **Email**: fabrice.kengni@icloud.com
- **Mot de passe**: kengni

⚠️ **ATTENTION**: Changez le mot de passe dès que possible dans **Paramètres** > **Profil Utilisateur**

---

## ✨ NOUVELLES FONCTIONNALITÉS v2.1

### 🎨 Dashboard Animé

Dès que vous ouvrez le dashboard, vous verrez:

1. **Pluie d'or et d'argent** 💰
   - Des pièces d'or (🪙) tombent du haut de l'écran
   - Des pièces d'argent (⚪) créent un effet complémentaire
   - Effet continu et apaisant

2. **Signaux de trading** 📊
   - Signaux **BUY** (📈) en vert
   - Signaux **SELL** (📉) en rouge
   - Apparaissent aléatoirement toutes les 3 secondes

3. **Effets de lueur** ✨
   - Les cartes de statistiques brillent
   - Les montants positifs ont un effet doré
   - Animation de pulsation subtile

### 🗑️ Suppressions Fonctionnelles

**TOUTES les fonctions de suppression sont maintenant opérationnelles:**

#### Supprimer une transaction financière:
1. Allez dans **Finances**
2. Trouvez la transaction à supprimer
3. Cliquez sur l'icône **🗑️ Supprimer**
4. Confirmez

#### Supprimer un trade:
1. Allez dans **Trading** ou **Portfolio**
2. Cliquez sur **Supprimer** à côté du trade
3. Confirmez

#### Supprimer une entrée de journal:
1. Allez dans **Journal de Trading**
2. Cliquez sur l'icône **🗑️** sur l'entrée
3. Confirmez la suppression

⚠️ **IMPORTANT**: Les suppressions sont **définitives** et ne peuvent pas être annulées!

### 📄 Rapports PDF Professionnels

**Génération de rapports certifiés:**

1. Allez dans **Rapports**
2. Choisissez le type:
   - **Rapport Financier**: Revenus, dépenses, profit
   - **Rapport Trading**: Performance, trades, score
3. Sélectionnez la période (du... au...)
4. Cliquez sur **"Générer le rapport PDF"**
5. Le PDF est téléchargé automatiquement

**Le PDF contient:**
- ✅ Logo Kengni Finance
- ✅ Filigrane officiel
- ✅ Tableaux professionnels
- ✅ Statistiques détaillées
- ✅ Certification "Document certifié et sécurisé"

### 🔔 Notifications Opérationnelles

**Système de notifications complet:**

1. Cliquez sur l'icône **🔔** dans le menu
2. Vous verrez toutes vos notifications:
   - ✅ Succès (actions réussies)
   - ⚠️ Avertissements (actions importantes)
   - ℹ️ Informations
   - ❌ Erreurs

3. Cliquez sur une notification pour:
   - La marquer comme lue
   - Accéder à l'action associée

### 🔐 Double Authentification (2FA)

**Sécurité renforcée (optionnel):**

Par défaut, la 2FA est **désactivée** pour faciliter le développement.

**Pour l'activer:**
1. Éditez le fichier `app.py`
2. Cherchez ligne 35-40:
```python
EMAIL_CONFIG = {
    'SMTP_SERVER': 'smtp.gmail.com',
    'SMTP_PORT': 587,
    'SMTP_USERNAME': 'votre-email@gmail.com',  # Changez ici
    'SMTP_PASSWORD': 'votre-app-password',      # Mot de passe d'app Gmail
    'ENABLED': True  # Changez False en True
}
```

**Comment obtenir un mot de passe d'application Gmail:**
1. Allez sur https://myaccount.google.com/security
2. Activez la "Validation en 2 étapes"
3. Cherchez "Mots de passe des applications"
4. Générez un nouveau mot de passe pour "Autre"
5. Copiez-collez dans `SMTP_PASSWORD`

**Une fois activé:**
- À chaque connexion, vous recevrez un code à 6 chiffres par email
- Entrez le code pour vous connecter
- Le code expire après 10 minutes

---

## 📊 UTILISATION QUOTIDIENNE

### Flux de Travail Recommandé

**Le Matin (5 minutes):**
1. Lancez l'application
2. Consultez le dashboard
3. Vérifiez les notifications (🔔)
4. Regardez votre score trader

**Pendant la Journée:**
1. **Finances**: Ajoutez vos transactions au fur et à mesure
   - Revenus, dépenses, créances, etc.
2. **Trading**: Exécutez vos trades
   - Achat/Vente avec stop-loss et take-profit
3. **Journal**: Documentez chaque trade
   - Uploadez des screenshots
   - Notez vos émotions et erreurs

**Le Soir (10 minutes):**
1. Revoyez vos trades du jour
2. Analysez vos erreurs dans le journal
3. Consultez l'**Assistant IA** pour des conseils
4. Vérifiez votre **Score Trader**

**Chaque Semaine:**
1. Générez un **rapport PDF**
2. Analysez votre **score trader**
3. Vérifiez les **patterns psychologiques** détectés
4. Ajustez votre stratégie

---

## 🎯 CONSEILS POUR MAXIMISER VOTRE SCORE TRADER

Votre **Score Trader** est calculé sur 100 points basé sur:
- **30%** Rentabilité (win rate, profit)
- **25%** Gestion du risque (stop-loss, position sizing)
- **20%** Discipline (pas d'overtrading)
- **15%** Cohérence stratégique (maximum 3 stratégies)
- **10%** Contrôle émotionnel (pas de FOMO, revenge trading)

**Pour améliorer votre score:**

1. ✅ **Utilisez TOUJOURS un stop-loss**
   - Protège votre capital
   - +25 points au score

2. ✅ **Maximum 5 trades par jour**
   - Évite l'overtrading
   - +20 points au score

3. ✅ **Restez fidèle à 2-3 stratégies**
   - Cohérence = performance
   - +15 points au score

4. ✅ **Documentez CHAQUE trade dans le journal**
   - Apprenez de vos erreurs
   - Évite les erreurs répétées

5. ✅ **Consultez l'analyse IA régulièrement**
   - Détecte vos faiblesses
   - Donne des recommandations

---

## 🛠️ DÉPANNAGE RAPIDE

### L'application ne démarre pas

**Problème**: Erreur au lancement
**Solution**:
```bash
# Réinstaller les dépendances
source venv/bin/activate
pip install -r requirements.txt --force-reinstall
```

### Port 5001 déjà utilisé

**Problème**: "Address already in use"
**Solution**:
```bash
# Trouver le processus
sudo lsof -i :5001

# Tuer le processus (remplacez <PID> par le numéro affiché)
sudo kill -9 <PID>

# OU changer le port dans app.py (dernière ligne)
# app.run(debug=True, host='0.0.0.0', port=5002)
```

### Erreur de base de données

**Problème**: "Database is locked" ou erreur SQL
**Solution**:
```bash
# Supprimer et recréer la base
rm kengni_finance.db
python3 -c "from app import init_db; init_db()"
```

### Les animations ne s'affichent pas

**Problème**: Pas d'animations sur le dashboard
**Solution**:
1. Vérifiez que les fichiers existent:
   ```bash
   ls static/css/animations.css
   ls static/js/animations.js
   ```
2. Rechargez la page avec **Ctrl+F5** (vide le cache)
3. Ouvrez la console du navigateur (**F12**) pour voir les erreurs

### Le raccourci bureau ne fonctionne pas

**Problème**: Double-clic ne fait rien
**Solution**:
```bash
chmod +x ~/Desktop/KengniFinance.desktop
```

---

## 📁 STRUCTURE DU PROJET

Voici comment est organisé votre projet:

```
kengni_finance_v2_complete/
├── app.py                      # ⚙️ Application principale (CORRIGÉE)
├── requirements.txt            # 📦 Dépendances Python
├── install.sh                  # 🔧 Script d'installation
├── start_kengni_finance.sh    # 🚀 Script de lancement
├── kengni_finance.db          # 🗄️ Base de données SQLite
│
├── README.md                   # 📖 Documentation complète
├── QUICK_START.md             # ⚡ Guide rapide
├── FEATURES_SUMMARY.md        # ✨ Résumé des fonctionnalités
│
├── static/
│   ├── css/
│   │   └── animations.css     # 🎨 Animations (NOUVEAU)
│   ├── js/
│   │   └── animations.js      # ⚡ Logique animations (NOUVEAU)
│   ├── img/
│   │   └── logo.jpeg          # 🖼️ Logo
│   ├── uploads/               # 📸 Images utilisateurs
│   └── pdf_reports/           # 📄 Rapports PDF (NOUVEAU)
│
└── templates/                  # 🎨 Templates HTML
    ├── base.html              # Base (animations incluses)
    ├── dashboard.html         # Dashboard animé
    ├── finances.html          # Gestion financière
    ├── trading.html           # Trading
    ├── portfolio.html         # Portfolio
    ├── trading_journal.html   # Journal (suppression OK)
    ├── ai_assistant.html      # Assistant IA
    ├── analysis.html          # Analyses IA
    ├── reports.html           # Rapports
    ├── notifications.html     # Notifications (NOUVEAU)
    ├── settings.html          # Paramètres
    ├── login.html             # Connexion
    ├── register.html          # Inscription
    ├── verify_token.html      # Vérification 2FA (NOUVEAU)
    └── history.html           # Historique
```

---

## 📧 SUPPORT

**En cas de problème:**

1. 📖 Consultez ce guide
2. 📖 Lisez `README.md` et `QUICK_START.md`
3. 🐛 Vérifiez les logs dans le terminal
4. 📧 Contactez: **fabrice.kengni@icloud.com**

---

## ✅ CHECKLIST DE VÉRIFICATION

Après l'installation, vérifiez que tout fonctionne:

- [ ] L'application démarre sans erreur
- [ ] Le dashboard s'affiche avec les animations
- [ ] Les pièces d'or/argent tombent
- [ ] Les signaux BUY/SELL apparaissent
- [ ] Vous pouvez créer une transaction
- [ ] Vous pouvez supprimer une transaction
- [ ] Vous pouvez exécuter un trade
- [ ] Vous pouvez générer un rapport PDF
- [ ] Les notifications s'affichent
- [ ] Vous pouvez voir votre score trader

Si **TOUT est coché** ✅, votre installation est PARFAITE!

---

## 🎉 FÉLICITATIONS!

Votre application **Kengni Finance v2.1** est maintenant:

- ✅ **Installée et fonctionnelle**
- ✅ **Corrigée de toutes les erreurs**
- ✅ **Enrichie de nouvelles fonctionnalités**
- ✅ **Animée avec des effets réels**
- ✅ **Sécurisée avec option 2FA**
- ✅ **Capable de générer des PDFs professionnels**
- ✅ **Dotée d'un système de notifications**
- ✅ **Prête à l'emploi**

---

## 💡 PROCHAINES ÉTAPES

1. ✅ Créez votre compte
2. ✅ Configurez vos préférences dans **Paramètres**
3. ✅ Ajoutez vos premières transactions financières
4. ✅ Exécutez quelques trades
5. ✅ Documentez dans le journal
6. ✅ Consultez votre score trader
7. ✅ Générez votre premier rapport PDF

---

**BON TRADING ET BONNE GESTION FINANCIÈRE! 📈💰**

---

**Kengni Finance v2.1** - © 2025 - Tous droits réservés  
**Auteur**: Fabrice Kengni  
**Email**: fabrice.kengni@icloud.com  
**Date**: Février 2025
