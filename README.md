# 🚀 Kengni Finance v2.1 - Enhanced Edition

## 📋 Description

Kengni Finance est une application complète de gestion financière et de trading enrichie par l'Intelligence Artificielle.

## ✨ Nouveautés v2.1

### 🔐 Sécurité
- **Double authentification (2FA)** par email
- Vérification par token à 6 chiffres
- Sessions sécurisées améliorées

### 📄 Rapports PDF
- Génération automatique de rapports professionnels
- Rapports financiers certifiés
- Rapports de trading détaillés
- Filigrane Kengni Finance officiel

### 🎨 Dashboard Animé
- Pluie d'or et d'argent (effets réels)
- Signaux de trading en temps réel
- Effets de lueur sur les stats
- Animations fluides et professionnelles

### 🗑️ Fonctions de Suppression
- Suppression de transactions financières
- Suppression de trades
- Suppression de positions
- Suppression d'entrées de journal
- Confirmation avant suppression

### 🔔 Notifications
- Système de notifications en temps réel
- Historique complet
- Marquer comme lu/non lu
- Notifications par email (configurable)

## 🚀 Installation Rapide

```bash
# 1. Extraire l'archive
unzip kengni_finance_v2.1.zip
cd kengni_finance_v2.1

# 2. Installer
chmod +x install.sh
./install.sh

# 3. Lancer
./start_kengni_finance.sh
```

## 🌐 Accès

URL: **http://localhost:5001**

### Identifiants par défaut
- Email: `fabrice.kengni@icloud.com`
- Mot de passe: `kengni`

**⚠️ Changez le mot de passe dès la première connexion!**

## 📱 Fonctionnalités Complètes

### 💰 Gestion Financière
- Transactions détaillées (revenus, dépenses, créances, dettes)
- Catégorisation avancée
- Analyse automatique IA
- Graphiques interactifs

### 📈 Trading Professionnel
- Exécution de trades
- Portfolio en temps réel
- Journal de trading avec images
- Score trader (0-100)
- Analyse psychologique

### 🤖 Intelligence Artificielle
- Détection FOMO, Revenge Trading, Overtrading
- Assistant IA conversationnel
- Recommandations personnalisées
- Analyse de performance

### 📊 Rapports & Analytics
- Rapports PDF professionnels
- Export CSV, Excel
- Comparaisons historiques
- Statistiques détaillées

## 🔧 Configuration

### Email 2FA (optionnel)
Modifiez `app.py` ligne 35-40 :
```python
EMAIL_CONFIG = {
    'SMTP_SERVER': 'smtp.gmail.com',
    'SMTP_PORT': 587,
    'SMTP_USERNAME': 'votre-email@gmail.com',
    'SMTP_PASSWORD': 'votre-app-password',
    'ENABLED': True  # Activez ici
}
```

## 📂 Structure

```
kengni_finance_v2.1/
├── app.py                  # Application principale
├── requirements.txt        # Dépendances
├── install.sh             # Script d'installation
├── start_kengni_finance.sh # Script de lancement
├── README.md              # Ce fichier
├── kengni_finance.db      # Base de données
├── static/
│   ├── css/
│   │   └── animations.css # Animations dashboard
│   ├── js/
│   │   └── animations.js  # Logique animations
│   ├── img/               # Images et logo
│   ├── uploads/           # Fichiers utilisateur
│   └── pdf_reports/       # Rapports PDF générés
└── templates/             # Templates HTML
    ├── base.html
    ├── dashboard.html
    ├── finances.html
    ├── trading.html
    ├── portfolio.html
    ├── trading_journal.html
    ├── ai_assistant.html
    ├── analysis.html
    ├── reports.html
    ├── settings.html
    ├── notifications.html
    ├── login.html
    ├── register.html
    └── verify_token.html  # Nouveau: 2FA
```

## 🛠️ Dépannage

### Port 5001 déjà utilisé
```bash
# Modifier le port dans app.py (dernière ligne)
app.run(debug=True, host='0.0.0.0', port=5002)
```

### Erreur base de données
```bash
rm kengni_finance.db
python3 -c "from app import init_db; init_db()"
```

### Modules manquants
```bash
source venv/bin/activate
pip install -r requirements.txt --force-reinstall
```

## 📈 Utilisation

1. **Premier lancement**: Créez votre compte ou utilisez les identifiants par défaut
2. **Configuration**: Allez dans Paramètres pour personnaliser
3. **Finances**: Ajoutez vos transactions
4. **Trading**: Exécutez des trades, consultez votre portfolio
5. **Journal**: Documentez vos trades avec images
6. **Analyse IA**: Consultez votre score et recommandations
7. **Rapports**: Générez des rapports PDF professionnels

## 🎯 Raccourcis Clavier

- `Ctrl+N`: Nouvelle transaction
- `Ctrl+T`: Nouveau trade
- `Ctrl+R`: Générer rapport
- `Ctrl+P`: Voir portfolio

## 📧 Support

Email: fabrice.kengni@icloud.com  
Version: 2.1.0  
Date: Février 2025

## 📄 Licence

© 2025 Kengni Finance - Tous droits réservés

---

**Bon trading! 📈💰**
