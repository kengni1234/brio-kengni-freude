# 🔗 Guide d'intégration WordPress + k-Ni + Claude IA

## Architecture complète

```
k-Ni Finance (Flask / PythonAnywhere)
        │
        ▼
  WordPress REST API   ◄──► WordPress MCP Plugin ◄──► Claude IA
        │
        ▼
  WooCommerce (boutique WP)
```

---

## ÉTAPE 1 — Installer WordPress (si pas encore fait)

### Option A : Hébergement WordPress séparé (recommandé)
- **Infomaniak**, **OVH**, **Hostinger**, **PlanetHoster** (Cameroun friendly)
- Ou WordPress.com (plan Business minimum pour les plugins)

### Option B : Même serveur PythonAnywhere
> ⚠️ PythonAnywhere ne supporte pas PHP. Utilisez un hébergement WordPress séparé.

---

## ÉTAPE 2 — Installer le plugin WordPress MCP

1. **Télécharger** le fichier `wordpress-mcp.zip` fourni
2. Dans WordPress admin → **Extensions → Téléverser une extension**
3. Sélectionner `wordpress-mcp.zip` → **Installer maintenant → Activer**
4. Aller dans **Réglages → WordPress MCP**

---

## ÉTAPE 3 — Configurer l'authentification WordPress

### Option A : JWT Token (recommandé pour MCP)
1. Dans **Réglages → WordPress MCP → Authentication Tokens**
2. Cliquer **Generate New Token**
3. Copier le token JWT (commence par `eyJhbGci...`)
4. Durée recommandée : 24h (à renouveler via cron job)

### Option B : Application Password (plus simple)
1. Dans WordPress admin → **Utilisateurs → Votre profil**
2. Descendre jusqu'à **Mots de passe d'application**
3. Nom : "k-Ni Integration" → **Ajouter**
4. Copier le mot de passe (format : `xxxx xxxx xxxx xxxx xxxx xxxx`)

---

## ÉTAPE 4 — Variables d'environnement PythonAnywhere

Aller sur **PythonAnywhere → Web → ton application → Fichier WSGI**
Ou dans l'onglet **Files** → modifier le fichier `.env`

```bash
# Dans PythonAnywhere > Web > Environment variables
WP_SITE_URL=https://votre-site-wordpress.com
WP_USERNAME=votre-username-admin
WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
WP_JWT_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Ou** dans ton `app.py` (moins sécurisé) :
```python
os.environ.setdefault('WP_SITE_URL', 'https://votre-site.com')
```

**Ou** via PythonAnywhere WSGI file :
```python
import os
os.environ['WP_SITE_URL'] = 'https://votre-site.com'
os.environ['WP_JWT_TOKEN'] = 'eyJ...'
```

---

## ÉTAPE 5 — Activer le plugin WordPress MCP

Dans **Réglages → WordPress MCP** :
- ✅ Activer **Posts Tools** (créer/modifier articles)
- ✅ Activer **Pages Tools**
- ✅ Activer **Media Tools**
- ✅ Activer **Users Tools**
- ✅ Activer **Settings Tools**
- Si WooCommerce installé : ✅ **WooCommerce Products & Orders**

---

## ÉTAPE 6 — Installer et configurer Yoast SEO (optionnel mais recommandé)

1. Dans WordPress → Extensions → Ajouter → Chercher "Yoast SEO"
2. Installer et activer **Yoast SEO** (version gratuite)
3. Les meta descriptions et scores SEO apparaîtront dans l'API WordPress

---

## ÉTAPE 7 — Tester l'intégration

### Test 1 : Connexion basique
```bash
curl https://votre-site.com/wp-json/wp/v2/posts
# Doit retourner la liste des articles
```

### Test 2 : Authentification
```bash
curl -H "Authorization: Bearer VOTRE_JWT_TOKEN" \
     https://votre-site.com/wp-json/wp/v2/wpmcp/streamable \
     -X POST \
     -H "Content-Type: application/json" \
     -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

### Test 3 : Depuis k-Ni Admin
1. Aller dans k-Ni Admin → **WordPress**
2. Remplir l'URL et le JWT Token
3. Cliquer **Tester la connexion**
4. ✅ Si vert : tout fonctionne !

---

## Fonctionnalités disponibles dans k-Ni Admin

### 📰 WordPress
- Voir et gérer les articles WordPress
- Créer des brouillons directement depuis k-Ni
- Synchroniser les produits k-Ni → WooCommerce
- Accéder aux outils MCP (liste complète)

### 🔍 SEO & Contenu IA (Claude)
- **Audit SEO** : Score + recommandations pour n'importe quelle URL/page
- **Générer article** : Article complet 400-1500 mots optimisé SEO
- **Optimiser article** : Améliore un article WordPress existant
- **Meta Tags** : Génère title, description, OG, Twitter Card

### 🔑 Mots-clés IA
- Recherche de mots-clés ciblés Cameroun
- Longue traîne + questions Google
- Analyse de saisonnalité locale

### 📅 Calendrier éditorial
- Planning 30 jours avec Claude
- Articles organisés par semaine et intention

---

## Routes API disponibles (k-Ni)

| Route | Méthode | Description |
|---|---|---|
| `/wp/status` | GET | Statut connexion WordPress |
| `/wp/api/posts` | GET | Liste les articles |
| `/wp/api/posts` | POST | Crée un article |
| `/wp/api/posts/:id` | PUT | Met à jour un article |
| `/wp/api/posts/:id` | DELETE | Supprime un article |
| `/wp/api/pages` | GET | Liste les pages |
| `/wp/api/media` | GET | Liste les médias |
| `/wp/api/ai/seo-audit` | POST | Audit SEO avec Claude |
| `/wp/api/ai/generate-article` | POST | Génère un article SEO |
| `/wp/api/ai/meta-tags` | POST | Génère les meta tags |
| `/wp/api/ai/keywords` | POST | Recherche mots-clés |
| `/wp/api/ai/optimize-post` | POST | Optimise un article WP |
| `/wp/api/ai/content-calendar` | POST | Calendrier éditorial |
| `/wp/mcp/tools` | GET | Liste outils MCP |
| `/wp/mcp/call` | POST | Appelle un outil MCP |
| `/wp/mcp/sync-products` | POST | Sync k-Ni → WooCommerce |

---

## Renouveler le JWT Token automatiquement

Le token JWT expire (1-24h). Pour l'automatiser sur PythonAnywhere :

### Script Python à ajouter dans un Scheduled Task (PythonAnywhere)
```python
# renew_wp_token.py — À exécuter toutes les 12h
import requests, os

WP_URL      = os.environ.get('WP_SITE_URL')
WP_USER     = os.environ.get('WP_USERNAME')
WP_PASSWORD = os.environ.get('WP_APP_PASSWORD')

# Générer un nouveau JWT via l'endpoint WordPress
resp = requests.post(
    f'{WP_URL}/wp-json/wp/v2/wpmcp',
    json={'method': 'generate_token', 'params': {}},
    auth=(WP_USER, WP_PASSWORD)
)
if resp.status_code == 200:
    new_token = resp.json().get('token', '')
    # Écrire dans un fichier .env ou mettre à jour la config
    print(f"✅ Nouveau token: {new_token[:20]}...")
```

---

## Troubleshooting

| Problème | Solution |
|---|---|
| `WP_SITE_URL non configuré` | Ajouter la variable d'env PythonAnywhere |
| `HTTP 401` | JWT expiré ou App Password incorrect |
| `HTTP 403` | Plugin non activé ou permissions insuffisantes |
| `HTTP 404` | URL WordPress incorrecte ou plugin non installé |
| `MCP non disponible` | JWT Token requis (App Password ne fonctionne pas avec MCP) |
| Articles vides | Vérifier que WP REST API n'est pas bloqué par un plugin sécurité |

---

## Prochaines étapes suggérées

1. **SEO automatique** : Générer les meta tags pour tous les produits k-Ni et les pousser sur WordPress
2. **Blog k-Ni** : Créer un blog WordPress lié à la boutique avec articles générés par IA
3. **WooCommerce** : Sync complète k-Ni Store → WooCommerce pour avoir deux storefronts
4. **Sitemap auto** : Générer le sitemap WordPress automatiquement via l'IA
5. **Cron SEO** : Audit SEO automatique chaque semaine avec rapport dans k-Ni Admin

---

*Guide créé pour k-Ni Finance — Kengni Fabrice · Yaoundé, Cameroun*
