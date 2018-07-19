#!/bin/bash

LOGGED_SERVICES="history publisher sparksimulator spark"

rm logs/*
docker-compose down
docker-compose up -d

docker run --rm -t --network=host \
    -v $(pwd)/test:/app/test \
    -v $(pwd)/logs:/app/logs \
    -v /var/run/docker.sock:/var/run/docker.sock \
    brewblox/integration

RESULT=$?

for svc in ${LOGGED_SERVICES}; do
    docker-compose logs --no-color ${svc} > logs/${svc}_service_log.txt
done

docker-compose down

exit ${RESULT}
