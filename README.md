# Padel

## Run

    sudo docker-compose --env-file .env up -d padel-web-dev; sudo docker logs --follow padel-padel-web-dev-1
    sudo docker-compose --env-file .env up -d padel-web-prod
    
    sudo docker-compose --env-file .env down -v; sudo docker image prune -af