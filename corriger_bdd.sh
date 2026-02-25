#!/bin/bash
# ══════════════════════════════════════════════════════════════
# Correction automatique de la base de données
# ══════════════════════════════════════════════════════════════

GREEN='\033[0;32m'; RED='\033[0;31m'; CYAN='\033[0;36m'; NC='\033[0m'

echo -e "${CYAN}╔════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║  🔧 Correction Base de Données         ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════╝${NC}"
echo ""

DB_FILE="kengni_finance.db"

if [ ! -f "$DB_FILE" ]; then
    echo -e "${RED}❌ $DB_FILE introuvable${NC}"
    echo "Placez ce script dans le dossier de l'application"
    exit 1
fi

# Backup
BACKUP="kengni_finance_backup_$(date +%Y%m%d_%H%M%S).db"
cp "$DB_FILE" "$BACKUP"
echo -e "${GREEN}✅ Backup créé: $BACKUP${NC}"

# Appliquer le correctif SQL
sqlite3 "$DB_FILE" < fix_base_donnees.sql
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Base de données corrigée!${NC}"
    echo -e "${CYAN}   Le type 'epargne' est maintenant accepté${NC}"
else
    echo -e "${RED}❌ Erreur lors de la correction${NC}"
    echo -e "${CYAN}Restauration du backup...${NC}"
    mv "$BACKUP" "$DB_FILE"
    exit 1
fi

echo ""
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✅ Correction terminée!                ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo "Vous pouvez maintenant enregistrer des transactions"
echo "de type 'epargne' sans erreur."
echo ""
