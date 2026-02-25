#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kengni Finance v2.1 - Quick Fix Script
Corrige l'erreur d'indentation dans app.py
"""

import re
import os
import sys

def fix_app_py():
    """Corrige l'erreur d'indentation dans app.py"""
    
    print("=" * 70)
    print("🔧 KENGNI FINANCE v2.1 - CORRECTION RAPIDE")
    print("=" * 70)
    print()
    
    # Vérifier que app.py existe
    if not os.path.exists('app.py'):
        print("❌ Erreur: app.py non trouvé!")
        print("   Assurez-vous d'être dans le bon dossier:")
        print("   cd ~/Documents/Afin/.../kengni_finance_v2_complete")
        sys.exit(1)
    
    print("📖 Lecture de app.py...")
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Erreur de lecture: {e}")
        sys.exit(1)
    
    print("🔧 Correction des erreurs d'indentation...")
    
    # Correction 1: @login_required après un return
    content = re.sub(
        r'(\n    return render_template\([^)]+\))\n    (@login_required)',
        r'\1\n\n\2',
        content
    )
    
    # Correction 2: @app.route après un return
    content = re.sub(
        r'(\n    return render_template\([^)]+\))\n    (@app\.route)',
        r'\1\n\n\2',
        content
    )
    
    # Correction 3: Problème spécifique ligne 2345
    content = re.sub(
        r'(def history\(\):.*?return render_template\(\'history\.html\', transactions=transactions\))\n    (@app\.route\(\'/delete-journal-entry)',
        r'\1\n\n\2',
        content,
        flags=re.DOTALL
    )
    
    # Correction 4: Assurer espacement entre fonctions
    content = re.sub(
        r'(\n@app\.route\([^)]+\))\n(@login_required)',
        r'\1\n\2',
        content
    )
    
    print("💾 Sauvegarde du fichier corrigé...")
    
    # Créer une sauvegarde
    try:
        with open('app.py.backup', 'w', encoding='utf-8') as f:
            with open('app.py', 'r', encoding='utf-8') as orig:
                f.write(orig.read())
        print("✅ Sauvegarde créée: app.py.backup")
    except Exception as e:
        print(f"⚠️  Impossible de créer la sauvegarde: {e}")
    
    # Écrire le fichier corrigé
    try:
        with open('app.py', 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Fichier app.py corrigé")
    except Exception as e:
        print(f"❌ Erreur d'écriture: {e}")
        sys.exit(1)
    
    # Vérifier la syntaxe
    print("🔍 Vérification de la syntaxe Python...")
    
    import py_compile
    try:
        py_compile.compile('app.py', doraise=True)
        print("✅ Syntaxe Python valide!")
    except py_compile.PyCompileError as e:
        print(f"❌ Erreur de syntaxe détectée:")
        print(f"   {e}")
        print()
        print("⚠️  Le fichier a été corrigé mais contient encore des erreurs.")
        print("   Une sauvegarde a été créée: app.py.backup")
        sys.exit(1)
    
    print()
    print("=" * 70)
    print("✅ CORRECTION TERMINÉE AVEC SUCCÈS!")
    print("=" * 70)
    print()
    print("Vous pouvez maintenant lancer l'application:")
    print("  python3 app.py")
    print()
    print("Ou:")
    print("  ./start_kengni_finance.sh")
    print()

if __name__ == '__main__':
    fix_app_py()
