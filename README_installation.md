# Guide d'installation — k-Ni Store Image Library + Performance
## 3 fichiers de patch à appliquer

---

## PATCH 1 → `app.py`
**Fichier : `patch_1_app_py.py`**

Ouvrir `app.py`, aller à la **toute fin du fichier**, juste AVANT :
```python
if __name__ == '__main__':
```
Copier-coller **tout le contenu** de `patch_1_app_py.py` à cet endroit.

**Ce que ça ajoute :**
- ✅ Compression gzip automatique (réponses JSON/HTML 60-80% plus légères)
- ✅ Cache in-memory 15s pour la bibliothèque d'images
- ✅ Pool de connexions SQLite (4 connexions réutilisées)
- ✅ Index SQLite manquants créés au démarrage
- ✅ Table `shop_image_library` créée automatiquement
- ✅ Routes bibliothèque : GET/POST/DELETE/PATCH/SYNC
- ✅ Routes produit : `/attach-image` et `/detach-image`

---

## PATCH 2 → `shop_admin.html` (Section Bibliothèque)
**Fichier : `patch_2_shop_admin_imglib.html`**

### Étape 2A — Bouton nav gauche
Chercher (~ligne 1027) :
```html
<button class="sa-nb" id="nb-posters" onclick="go('posters')">
```
Insérer JUSTE AVANT :
```html
<button class="sa-nb" id="nb-imglib" onclick="go('imglib')" style="border-left:3px solid #f59e0b"><i class="fas fa-photo-video" style="color:#f59e0b"></i> Bibliothèque images <span id="imgLibCount" style="margin-left:auto;font-size:.65rem;color:var(--text-secondary)"></span></button>
```

### Étape 2B — Tableau SECS (~ligne 3456)
```javascript
// Avant :
const SECS=['dash','prod','new','ord','inv','stock','analytics','staff','banners','posters','perf',...

// Après (ajouter 'imglib' après 'banners') :
const SECS=['dash','prod','new','ord','inv','stock','analytics','staff','banners','imglib','posters','perf',...
```

### Étape 2C — Fonction go() (~ligne 3488)
```javascript
// Après : if(n==='apropos') loadAproposAdmin();
// Ajouter :
if(n==='imglib') loadImageLibrary();
```

### Étape 2D — Section HTML
Chercher :
```html
<div class="sec" id="sec-posters">
```
Insérer JUSTE AVANT la section entière `<div class="sec" id="sec-imglib">...</div>`
et le `<script>` du fichier `patch_2_shop_admin_imglib.html`.

---

## PATCH 3 → `shop_admin.html` (Fixes + Performance)
**Fichier : `patch_3_shop_admin_fixes.html`**

Copier-coller tout le contenu du fichier juste AVANT la balise `</body>` de `shop_admin.html`.

**Ce que ça ajoute/corrige :**
- ✅ **FIX** : Suppression d'image d'un produit en ligne (slot galerie × → appel API immédiat)
- ✅ Modal "Gérer images" sur chaque produit de la liste
- ✅ Onglet "Bibliothèque" dans ce modal (choisir depuis les images existantes)
- ✅ Lazy loading des images
- ✅ Timeout automatique 15s sur tous les fetch
- ✅ Préfetch des produits au survol du menu

---

## Résumé des nouvelles routes API

| Route | Méthode | Description |
|-------|---------|-------------|
| `/shop/api/image-library` | GET | Liste paginée + usage par produit |
| `/shop/api/image-library/upload` | POST | Upload vers la bibliothèque |
| `/shop/api/image-library/<id>` | DELETE | Supprime + retire des produits |
| `/shop/api/image-library/<id>` | PATCH | Met à jour label/tags |
| `/shop/api/image-library/sync` | POST | Importe images des produits |
| `/shop/api/product/<pid>/attach-image` | POST | Attache une image à un produit |
| `/shop/api/product/<pid>/detach-image` | POST | Retire une image d'un produit |

---

## Après application

1. **Redémarrer** l'application (les nouveaux PRAGMA et index sont appliqués au démarrage)
2. Aller dans **Admin Boutique → Bibliothèque images**
3. Cliquer sur **Sync** pour importer les images déjà sur vos produits
4. Vérifier que la compression gzip est active (DevTools → Network → réponses JSON)
