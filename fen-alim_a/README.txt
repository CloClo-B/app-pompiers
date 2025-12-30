Bien vérifier que les trois conteneurs sont bien dans le réseau:
- docker inspect fenalim_db | grep -A10 Networks
Et changer le db par api et pgadmin pour vérifier tout le monde.
Si un n'est pas dans le réseau:
- docker compose down
- docker network prune -f
- docker compose up -d --build

Si port en cours d'utilisation:
- sudo systemctl stop postgresql


