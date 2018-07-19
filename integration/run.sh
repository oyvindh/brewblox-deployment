docker run \
    --rm \
    -t \
    --network host \
    -v $(pwd)/test:/app/test \
    -v $(pwd)/logs:/app/logs \
    -v /var/run/docker.sock:/var/run/docker.sock \
    brewblox/integration