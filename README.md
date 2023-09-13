# Padel

## Run

Start in developement mode:

    sudo docker-compose --env-file .env up -d padel-web-dev; sudo docker-compose logs --follow

Start in production mode:

    sudo docker-compose --env-file .env up -d padel-web-prod
    
Start in stop:

    sudo docker-compose --env-file .env down -v; sudo docker image prune -af

Restart the consumer service:

    sudo docker-compose restart consumer-app

## DB

    sudo docker exec -it padel-mysql-db-1 mysql -u root -p
    mysql -h 0.0.0.0 -P 3306 -u root -p