#!/bin/bash

echo "=========================================="
echo "🚀 Démarrage de Kengni Finance"
echo "=========================================="
echo ""

# Déterminer la commande Python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Python n'est pas installé!"
    exit 1
fi

# Activer l'environnement virtuel si disponible
if [ -d "venv" ]; then
    echo "🔄 Activation de l'environnement virtuel..."
    source venv/bin/activate
    echo "✅ Environnement virtuel activé"
else
    echo "⚠️  Pas d'environnement virtuel détecté"
    echo "   L'application utilisera Python système"
fi
echo ""

# Lancer l'application
echo "🌐 Lancement de l'application..."
echo "   URL: http://localhost:5001"
echo "   Email: fabrice.kengni@icloud.com"
echo "   Password: kengni"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter"
echo "=========================================="
echo ""

$PYTHON_CMD app.py
