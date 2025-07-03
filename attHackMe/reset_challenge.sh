#!/bin/bash

# Vérifie qu’un argument est passé
if [ -z "$1" ]; then
    echo "❌ Usage : ./reset_challenge.sh <nom_du_service>"
    echo "Exemple : ./reset_challenge.sh win-auth-challenge1"
    exit 1
fi

SERVICE=$1

echo "🔁 Réinitialisation du service : $SERVICE"

# Arrêter et supprimer le conteneur
docker compose stop $SERVICE
docker compose rm -f $SERVICE

# Rebuild sans toucher au cache global
docker compose build $SERVICE

# Relancer le conteneur uniquement
docker compose up -d $SERVICE

echo "✅ $SERVICE a été réinitialisé."
