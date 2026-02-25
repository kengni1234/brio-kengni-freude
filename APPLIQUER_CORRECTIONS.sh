#!/bin/bash
# Script pour appliquer toutes les corrections
echo "🔧 Application des corrections..."
DEST=$(dirname "$0")/../

cp "$DEST/templates_fixes/app.py" "$DEST/app.py"
cp "$DEST/templates_fixes/templates/"*.html "$DEST/templates/"
echo "✅ Toutes les corrections appliquées!"
echo "Lancez: python3 app.py"
