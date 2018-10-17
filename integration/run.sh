#!/usr/bin/env bash

LOGGED_SERVICES="history publisher sparksimulator spark sparktwo"

rm logs/*
docker-compose down
docker-compose up -d

pipenv run pytest "$@"

RESULT=$?

for svc in ${LOGGED_SERVICES}; do
    docker-compose logs --no-color ${svc} > logs/${svc}_service_log.txt
done

docker-compose down

exit ${RESULT}
