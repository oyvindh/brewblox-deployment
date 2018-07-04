#! /bin/bash

docker run \
    --rm \
    --detach \
    --name docker-compose-ui \
    --volume /home/${USER}:/home/${USER} \
    --workdir /home/${USER} \
    --publish 5000:5000 \
    --volume /var/run/docker.sock:/var/run/docker.sock \
    brewblox/docker-compose-ui
