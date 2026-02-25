#!/bin/bash

echo "=========================================="
echo "🔧 Diagnostic et Correction Kengni Finance"
echo "=========================================="
echo ""

# Vérifier Python3
echo "1️⃣ Vérification de Python..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    echo "✅ Python3 trouvé: $(python3 --version)"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    echo "✅ Python trouvé: $(python --version)"
else
    echo "❌ Python n'est pas installé!"
    echo "   Installez Python avec: sudo apt install python3"
    exit 1
fi
echo ""

# Vérifier pip
echo "2️⃣ Vérification de pip..."
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
    echo "✅ pip3 trouvé"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
    echo "✅ pip trouvé"
else
    echo "❌ pip n'est pas installé!"
    echo "   Installez pip avec: sudo apt install python3-pip"
    exit 1
fi
echo ""

# Créer le dossier templates s'il n'existe pas
echo "3️⃣ Création du dossier templates..."
mkdir -p templates
echo "✅ Dossier templates créé/vérifié"
echo ""

# Exécuter le script de correction
echo "4️⃣ Création des templates HTML..."
if [ -f "fix_templates.py" ]; then
    $PYTHON_CMD fix_templates.py
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "=========================================="
        echo "✅ SUCCÈS! Tous les templates sont créés"
        echo "=========================================="
        echo ""
        echo "Vous pouvez maintenant lancer l'application:"
        echo "  $PYTHON_CMD app.py"
        echo ""
    else
        echo ""
        echo "❌ Erreur lors de la création des templates"
        echo "   Essayez manuellement: $PYTHON_CMD fix_templates.py"
        exit 1
    fi
else
    echo "❌ Le fichier fix_templates.py est introuvable!"
    echo "   Assurez-vous d'être dans le bon dossier"
    exit 1
fi

# Vérifier l'installation des dépendances
echo "5️⃣ Vérification des dépendances Python..."
if [ -f "requirements.txt" ]; then
    echo "📦 Installation des dépendances..."
    $PIP_CMD install -r requirements.txt --quiet 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "✅ Dépendances installées"
    else
        echo "⚠️  Certaines dépendances n'ont pas pu être installées"
        echo "   Essayez: $PIP_CMD install flask werkzeug pandas yfinance numpy pillow"
    fi
else
    echo "⚠️  requirements.txt introuvable"
fi
echo ""

echo "=========================================="
echo "✅ Configuration terminée!"
echo "=========================================="
echo ""
echo "Pour lancer l'application:"
echo "  $PYTHON_CMD app.py"
echo ""
echo "Ou utilisez le script de lancement:"
echo "  chmod +x start.sh"
echo "  ./start.sh"
echo ""
