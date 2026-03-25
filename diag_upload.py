#!/usr/bin/env python3
"""
diag_upload.py — Diagnostic d'upload images pour k-Ni Store (PythonAnywhere)
Usage : python3 diag_upload.py
"""
import os, sys, stat, json

BASE = os.path.dirname(os.path.abspath(__file__))
UPLOAD_BASE = os.path.join(BASE, 'static', 'uploads')
SHOP_DIR    = os.path.join(UPLOAD_BASE, 'shop')
AVATARS_DIR = os.path.join(UPLOAD_BASE, 'avatars')

OK  = "✅"; WARN = "⚠️ "; ERR = "❌"
results = []

def chk(label, ok, detail=""):
    sym = OK if ok else ERR
    print(f"  {sym} {label}" + (f" — {detail}" if detail else ""))
    results.append(ok)

print("\n══════════════════════════════════════════")
print(" DIAGNOSTIC UPLOAD k-Ni Store")
print("══════════════════════════════════════════\n")

# 1. Dossiers
print("📁 Dossiers uploads :")
for path, name in [(UPLOAD_BASE,'uploads'), (SHOP_DIR,'uploads/shop'), (AVATARS_DIR,'uploads/avatars')]:
    exists = os.path.isdir(path)
    if exists:
        try:
            mode = oct(stat.S_IMODE(os.stat(path).st_mode))
            writable = os.access(path, os.W_OK)
            chk(name, writable, f"mode={mode}, writable={writable}")
        except Exception as e:
            chk(name, False, str(e))
    else:
        chk(name, False, "MANQUANT — créer avec mkdir -p")
        try:
            os.makedirs(path, exist_ok=True)
            print(f"       → Créé automatiquement : {path}")
        except Exception as e:
            print(f"       → Impossible de créer : {e}")

# 2. PIL
print("\n📦 Pillow (PIL) :")
try:
    from PIL import Image
    chk("Pillow importé", True, Image.__version__ if hasattr(Image,'__version__') else "ok")
    # Test compression
    import io
    img_test = Image.new('RGB', (200,200), color=(0,192,118))
    buf = io.BytesIO()
    img_test.thumbnail((100,100), Image.LANCZOS)
    img_test.save(buf, format='JPEG', quality=80, optimize=True)
    chk("Compression JPEG", True, f"{len(buf.getvalue())} bytes")
except Exception as e:
    chk("Pillow", False, str(e))

# 3. Espace disque
print("\n💾 Espace disque :")
try:
    st = os.statvfs(UPLOAD_BASE if os.path.exists(UPLOAD_BASE) else BASE)
    free_mb = (st.f_bavail * st.f_frsize) / 1024 / 1024
    chk("Espace libre", free_mb > 50, f"{free_mb:.1f} MB libres")
except Exception as e:
    chk("Espace disque", False, str(e))

# 4. Ecriture test
print("\n✏️  Test écriture :")
try:
    test_path = os.path.join(SHOP_DIR, '_diag_test_.txt')
    with open(test_path, 'w') as f:
        f.write("test")
    os.remove(test_path)
    chk("Ecriture dans shop/", True)
except Exception as e:
    chk("Ecriture dans shop/", False, str(e))

# 5. app.py clés
print("\n🔧 Vérification app.py :")
app_path = os.path.join(BASE, 'app.py')
if os.path.exists(app_path):
    with open(app_path, 'r', encoding='utf-8', errors='ignore') as f:
        src = f.read()
    chk("MAX_CONTENT_LENGTH configuré", 'MAX_CONTENT_LENGTH' in src)
    chk("Route /shop/api/product/upload-image", '/shop/api/product/upload-image' in src)
    chk("Compression PIL (patch 3a)", 'PATCH: compression automatique' in src)
    chk("SSE lifetime 45s (patch 1)", '_SSE_MAX_LIFETIME = 45' in src)
    chk("pbkdf2 100k (patch 2)", 'iterations=100000' in src)
else:
    print(f"  {WARN} app.py non trouvé dans {BASE}")

# Résumé
total = len(results)
passed = sum(results)
print(f"\n══════════════════════════════════════════")
print(f" Résultat : {passed}/{total} checks passés")
if passed == total:
    print(f" {OK} Tout est OK — l'upload devrait fonctionner")
else:
    print(f" {ERR} {total-passed} problème(s) détecté(s) — voir ci-dessus")
print("══════════════════════════════════════════\n")
