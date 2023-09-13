# Padel

## Run

    sudo docker-compose --env-file .env up -d padel-web-dev; sudo docker-compose logs --follow
    sudo docker-compose --env-file .env up -d padel-web-prod
    
    sudo docker-compose --env-file .env down -v; sudo docker image prune -af

    sudo docker-compose restart consumer-app

## DB

    sudo docker exec -it padel-mysql-db-1 mysql -u root -p
    mysql -h 0.0.0.0 -P 3306 -u root -p