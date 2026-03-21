# 📱 Guide d'intégration PWA — k-Ni Store Flask

## Ce que tu as reçu

```
manifest.json        → /static/manifest.json
sw.js                → /static/sw.js
icons/
  icon-72.png        → /static/icons/icon-72.png
  icon-96.png        → /static/icons/icon-96.png
  icon-128.png       → /static/icons/icon-128.png
  icon-144.png       → /static/icons/icon-144.png
  icon-152.png       → /static/icons/icon-152.png
  icon-192.png       → /static/icons/icon-192.png
  icon-384.png       → /static/icons/icon-384.png
  icon-512.png       → /static/icons/icon-512.png
shop.html            → templates/shop.html     (balises PWA + bannière + SW ajoutés)
shop_admin.html      → templates/shop_admin.html  (nav agrandi + guide deals)
```

---

## Étapes d'intégration (5 minutes)

### 1 — Copier les fichiers statiques

```bash
# Depuis ce dossier, copier vers ton projet Flask :
cp manifest.json    ton_projet/static/manifest.json
cp sw.js            ton_projet/static/sw.js
cp icons/*.png      ton_projet/static/icons/
```

### 2 — Ajouter la route `/static/sw.js` dans Flask

Le service worker **doit être servi depuis la racine** du site (ou `/static/`).
Flask sert `/static/sw.js` automatiquement, mais le scope sera `/static/`.

Pour qu'il couvre toute l'app, ajoute cette route dans ton `app.py` :

```python
from flask import send_from_directory

@app.route('/sw.js')
def service_worker():
    """Sert le service worker depuis la racine pour un scope global."""
    return send_from_directory('static', 'sw.js',
                               mimetype='application/javascript')

@app.route('/manifest.json')
def manifest():
    """Sert le manifest depuis la racine."""
    return send_from_directory('static', 'manifest.json',
                               mimetype='application/manifest+json')
```

> ⚠️ Si tu gardes les URLs `/static/sw.js` et `/static/manifest.json` (sans les routes ci-dessus),
> le service worker ne couvrira que `/static/` — les pages shop ne seront pas en cache.
> **Les routes Flask ci-dessus sont recommandées.**

### 3 — Mettre à jour shop.html

Remplace ton `templates/shop.html` par le fichier `shop.html` fourni.
*(Les modifications sont dans le `<head>` et juste avant `</body>`)*

### 4 — Mettre à jour shop_admin.html

Remplace ton `templates/shop_admin.html` par le fichier `shop_admin.html` fourni.

### 5 — Tester l'installation

1. Déployer sur ton serveur (la PWA ne fonctionne **pas** sur `http://localhost` sans HTTPS)
2. Ouvrir Chrome Android sur `https://ton-domaine.cm/shop`
3. Chrome affiche automatiquement la **bannière d'installation** en bas de l'écran
4. Cliquer **"Installer"** → l'app apparaît sur l'écran d'accueil

---

## Comment ça marche pour tes utilisateurs

```
Première visite (avec réseau)
        ↓
Service Worker s'installe en arrière-plan
        ↓
Shop, CSS, JS, images → mis en cache
        ↓
Visite suivante (même sans réseau)
        ↓
La boutique s'ouvre en < 1 seconde depuis le cache
```

---

## Checklist de validation

- [ ] `https://ton-domaine.cm/manifest.json` répond 200
- [ ] `https://ton-domaine.cm/sw.js` répond 200
- [ ] Chrome DevTools → Application → Manifest → Aucune erreur
- [ ] Chrome DevTools → Application → Service Workers → Status = "activated and running"
- [ ] Score Lighthouse PWA ≥ 90
- [ ] Icône visible sur écran d'accueil Android

---

## Dépannage courant

| Problème | Solution |
|---|---|
| "Add to home screen" ne s'affiche pas | Vérifier HTTPS, manifest valide, SW enregistré |
| SW scope trop limité | Ajouter les routes Flask `/sw.js` et `/manifest.json` |
| Icônes manquantes | Vérifier que `/static/icons/*.png` existent et sont accessibles |
| Cache obsolète après mise à jour | Changer `CACHE_VERSION` dans `sw.js` (ex: `kni-v1.0.1`) |
