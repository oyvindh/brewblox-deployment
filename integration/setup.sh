#!/usr/bin/env bash
set -e

docker-compose pull
docker build -t brewblox/integration .
