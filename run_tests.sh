#!/bin/bash

echo "Lancement des tests FenAlim..."
echo "=================================="

# Nettoyer les conteneurs existants
docker-compose -f docker-compose.test.yml down -v

# Lancer les tests (sans -d pour voir la sortie)
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit

# Récupérer le code de sortie
EXIT_CODE=$?

# Nettoyer
docker-compose -f docker-compose.test.yml down

if [ $EXIT_CODE -eq 0 ]; then
    echo "Tous les tests sont passés !"
else
    echo "Des tests ont échoué (code: $EXIT_CODE)"
fi

exit $EXIT_CODE
