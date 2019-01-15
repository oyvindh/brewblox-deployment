#!/usr/bin/env bash

prompt() {
    while true; do
        read -p "$1 [Y/n]" yn
        case "$yn" in
            "" ) ;&
            [Yy]* ) echo "yes"; break;;
            [Nn]* ) echo "no"; break;;
            * ) echo "Please answer yes or no.";;
        esac
    done
}

do_script() {
    if [ $(prompt "Do you want to generate an SSL certificate?") = yes ]; then
        sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout traefik/brewblox.key -out traefik/brewblox.crt
        sudo chmod 644 traefik/brewblox.crt
        sudo chmod 600 traefik/brewblox.key
    fi

    if [ $(prompt "Do you want to update the Docker containers?") = yes ]; then
        docker-compose pull
    fi

    if [ $(prompt "Do you want to create default dashboards?") = yes ]; then
        HOST=https://localhost/datastore
        DATABASES="services dashboards dashboard-items"

        docker-compose up -d
        curl -sk -X GET --retry 5 ${HOST}
        curl -sk -X PUT ${HOST}/_users

        for db in ${DATABASES}; do
            curl -sk -X PUT ${HOST}/${db}
            cat presets/${db}.json \
            | curl \
                -sk \
                -X POST \
                --header 'Content-Type: application/json' \
                --header 'Accept: application/json' \
                --data "@-" "${HOST}/${db}/_bulk_docs"
        done
        docker-compose down
    fi

    echo "Done"
}

do_script
