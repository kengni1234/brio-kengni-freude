# 🚀 KENGNI FINANCE v2.1 - GUIDE D'INSTALLATION ULTRA-RAPIDE

## ⚡ Installation en 3 étapes (5 minutes)

### Étape 1: Télécharger et Extraire
```bash
# Téléchargez le fichier kengni_finance_v2.1_complete.tar.gz
# Puis :
tar -xzf kengni_finance_v2.1_complete.tar.gz
cd kengni_finance_v2_complete
```

### Étape 2: Installer
```bash
chmod +x install.sh
./install.sh
```

Le script va automatiquement:
- ✅ Vérifier Python 3 et pip
- ✅ Créer un environnement virtuel
- ✅ Installer toutes les dépendances
- ✅ Initialiser la base de données
- ✅ Créer un raccourci bureau
- ✅ Configurer un alias de lancement rapide

### Étape 3: Lancer l'application

**4 méthodes au choix:**

#### A) Raccourci Bureau (Le plus simple) 🖱️
- Double-cliquez sur l'icône **KengniFinance** sur votre bureau
- L'application démarre automatiquement

#### B) Script de lancement 🚀
```bash
./start_kengni_finance.sh
```

#### C) Commande manuelle 💻
```bash
source venv/bin/activate
python3 app.py
```

#### D) Alias rapide ⚡
```bash
kengni-finance
```
(Après redémarrage du terminal)

### Étape 4: Accéder à l'application 🌐

Ouvrez votre navigateur : **http://localhost:5001**

---

## 🔑 Première Connexion

### Option 1: Créer votre propre compte (RECOMMANDÉ) ✨

1. Sur la page de connexion, cliquez sur **"Créer un compte"**
2. Remplissez le formulaire:
   - Nom d'utilisateur (min. 3 caractères)
   - Email (valide)
   - Mot de passe (min. 6 caractères)
   - Devise préférée
3. Cliquez sur **"Créer mon compte"**
4. **NOUVEAU v2.1**: Vérification par email
   - Un code à 6 chiffres sera envoyé à votre email
   - Entrez le code pour activer votre compte
   - ⚠️ Si l'email est désactivé (par défaut), le code s'affichera dans le terminal

### Option 2: Compte par défaut 🔓

- **Email**: fabrice.kengni@icloud.com
- **Mot de passe**: kengni
- ⚠️ **IMPORTANT**: Changez le mot de passe dans Paramètres !

---

## ✨ NOUVELLES FONCTIONNALITÉS v2.1

### 🔐 Double Authentification (2FA)

**Activation:**
1. Allez dans **Paramètres**
2. Activez **"Double authentification"**
3. À chaque connexion, vous recevrez un code par email

**Configuration Email (optionnel):**
Éditez `app.py` ligne 35-40:
```python
EMAIL_CONFIG = {
    'SMTP_SERVER': 'smtp.gmail.com',
    'SMTP_PORT': 587,
    'SMTP_USERNAME': 'votre-email@gmail.com',
    'SMTP_PASSWORD': 'votre-app-password',  # Mot de passe d'application Gmail
    'ENABLED': True  # ⬅️ Changez en True
}
```

**Obtenir un mot de passe d'application Gmail:**
1. Allez sur https://myaccount.google.com/security
2. Activez la validation en 2 étapes
3. Générez un mot de passe d'application
4. Utilisez ce mot de passe dans `SMTP_PASSWORD`

### 📄 Rapports PDF Professionnels

**Générer un rapport:**
1. Allez dans **Rapports**
2. Sélectionnez le type (Financier / Trading)
3. Choisissez la période
4. Cliquez sur **"Générer le rapport PDF"**
5. Le PDF est créé avec:
   - ✅ Logo Kengni Finance
   - ✅ Filigrane officiel
   - ✅ Données certifiées
   - ✅ Graphiques et tableaux

**Télécharger:**
- Le fichier PDF est automatiquement téléchargé
- Aussi disponible dans `static/pdf_reports/`

### 🎨 Dashboard Animé

**Effets visuels en temps réel:**

1. **Pluie d'or et d'argent** 💰
   - Pièces d'or (🪙) tombent du haut de l'écran
   - Pièces d'argent (⚪) créent un effet visuel
   - Représentent vos gains

2. **Signaux de trading** 📊
   - Signaux BUY (📈) en vert
   - Signaux SELL (📉) en rouge
   - Apparaissent aléatoirement sur le dashboard

3. **Effets de lueur** ✨
   - Les statistiques brillent avec un effet de lueur
   - Les montants positifs ont un effet doré
   - Animation de pulsation sur les cartes

4. **Animations fluides** 🌊
   - Transitions douces
   - Effets de shimmer sur les textes
   - Graphiques avec ombres portées

### 🗑️ Fonctions de Suppression

**Toutes les suppressions sont maintenant opérationnelles:**

#### Supprimer une transaction financière
1. Allez dans **Finances**
2. Trouvez la transaction
3. Cliquez sur l'icône **🗑️ Supprimer**
4. Confirmez la suppression

#### Supprimer un trade
1. Allez dans **Trading** ou **Portfolio**
2. Trouvez le trade
3. Cliquez sur **Supprimer**
4. Confirmez

#### Supprimer une position
1. Allez dans **Portfolio**
2. Cliquez sur **Actions** > **Supprimer**
3. Confirmez

#### Supprimer une entrée de journal
1. Allez dans **Journal de Trading**
2. Cliquez sur l'icône **🗑️**
3. Confirmez la suppression définitive

**⚠️ ATTENTION**: Les suppressions sont définitives et ne peuvent pas être annulées!

### 🔔 Notifications Opérationnelles

**Accéder aux notifications:**
1. Cliquez sur l'icône **🔔** dans le menu
2. Consultez toutes vos notifications
3. Cliquez pour marquer comme lu

**Types de notifications:**
- ✅ **Succès**: Opérations réussies
- ⚠️ **Avertissement**: Actions importantes
- ℹ️ **Info**: Informations générales
- ❌ **Erreur**: Problèmes détectés

**Recevoir par email:**
1. Allez dans **Paramètres**
2. Activez **"Notifications par email"**
3. Configurez l'email dans `app.py`

---

## 📊 FONCTIONNALITÉS COMPLÈTES

### 💰 Gestion Financière
- Transactions illimitées (revenus, dépenses, créances, dettes)
- Catégorisation avancée
- Graphiques interactifs
- Analyse des tendances

### 📈 Trading Professionnel
- Exécution de trades en temps réel
- Portfolio avec P&L automatique
- Stop-loss et take-profit
- Historique complet

### 📓 Journal de Trading
- Documentation de chaque trade
- Upload de screenshots/charts
- Notes et émotions
- Erreurs et leçons apprises

### 🤖 Intelligence Artificielle
- **Score Trader** (0-100)
  - Rentabilité
  - Gestion du risque
  - Discipline
  - Cohérence stratégique
  - Contrôle émotionnel

- **Détection Psychologique**
  - FOMO (Fear of Missing Out)
  - Revenge Trading
  - Overtrading
  - Overconfidence

- **Assistant IA Conversationnel**
  - Posez des questions en langage naturel
  - Recevez des conseils personnalisés

### 📊 Rapports & Analytics
- Rapports mensuels, trimestriels, annuels
- Export PDF, CSV, Excel
- Comparaisons historiques
- Benchmarks de performance

---

## 🛠️ DÉPANNAGE

### Le port 5001 est déjà utilisé
```bash
# Trouver le processus
sudo lsof -i :5001

# Le tuer
sudo kill -9 <PID>

# Ou changer le port dans app.py (dernière ligne)
app.run(debug=True, host='0.0.0.0', port=5002)
```

### Erreur de base de données
```bash
rm kengni_finance.db
python3 -c "from app import init_db; init_db()"
```

### Module manquant
```bash
source venv/bin/activate
pip install -r requirements.txt --force-reinstall
```

### Les animations ne s'affichent pas
1. Vérifiez que `static/css/animations.css` existe
2. Vérifiez que `static/js/animations.js` existe
3. Ouvrez la console du navigateur (F12) pour voir les erreurs
4. Rechargez la page avec `Ctrl+F5`

### Les emails 2FA ne fonctionnent pas
1. Vérifiez la configuration dans `app.py`
2. Assurez-vous que `ENABLED = True`
3. Utilisez un mot de passe d'application Gmail
4. Vérifiez les logs dans le terminal

### Le raccourci bureau ne fonctionne pas
```bash
chmod +x ~/Desktop/KengniFinance.desktop
```

---

## 📱 UTILISATION QUOTIDIENNE

### Routine Recommandée

**Matin (5 min):**
1. Ouvrez l'application
2. Consultez le dashboard
3. Vérifiez les notifications
4. Analysez votre score trader

**Pendant la journée:**
1. Ajoutez les transactions au fur et à mesure
2. Exécutez vos trades
3. Documentez dans le journal
4. Prenez des screenshots

**Soir (10 min):**
1. Revoyez vos trades du jour
2. Analysez les erreurs
3. Consultez l'assistant IA
4. Planifiez le lendemain

**Hebdomadaire:**
1. Générez un rapport PDF
2. Analysez votre score
3. Vérifiez les patterns psychologiques
4. Ajustez votre stratégie

---

## 🎯 ASTUCES PRO

### Maximiser votre Score Trader
1. ✅ Utilisez toujours un stop-loss
2. ✅ Ne tradez pas plus de 5 fois par jour
3. ✅ Restez fidèle à 2-3 stratégies maximum
4. ✅ Documentez chaque trade dans le journal
5. ✅ Analysez vos erreurs

### Optimiser vos Finances
1. ✅ Catégorisez toutes vos transactions
2. ✅ Visez un ratio dépenses/revenus < 70%
3. ✅ Suivez vos créances et dettes
4. ✅ Générez des rapports mensuels

### Utiliser l'IA Efficacement
1. ✅ Posez des questions spécifiques
2. ✅ Suivez les recommandations
3. ✅ Travaillez sur vos points faibles
4. ✅ Consultez régulièrement votre analyse

---

## 📧 SUPPORT

**Email**: fabrice.kengni@icloud.com

**En cas de problème:**
1. Consultez ce guide
2. Vérifiez les logs dans le terminal
3. Consultez `README.md`
4. Contactez le support

---

## 🎉 PRÊT À COMMENCER!

Votre application Kengni Finance v2.1 est maintenant installée avec:
- ✅ Double authentification
- ✅ Rapports PDF professionnels
- ✅ Dashboard animé avec effets réels
- ✅ Suppressions opérationnelles
- ✅ Notifications complètes
- ✅ Intelligence artificielle avancée

**Bon trading et bonne gestion financière! 📈💰**

---

**Kengni Finance v2.1** - © 2025 - Tous droits réservés
