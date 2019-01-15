#! /bin/bash
set -e

pushd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )" > /dev/null

sudo apt update
sudo apt install -y qemu qemu-user-static qemu-user binfmt-support
cp $(which qemu-arm-static) .

python3 ./enable_experimental.py

NODE_TAGS="10 10-slim 11 11-slim"

for tag in ${NODE_TAGS}; do
    echo "
    FROM arm32v7/node:${tag}
    COPY ./qemu-arm-static /usr/bin/qemu-arm-static
    " > ./Dockerfile

    docker pull --platform=linux/arm arm32v7/node:${tag}
    docker build --platform=linux/arm --no-cache -t brewblox/rpi-node:${tag} .
    docker push brewblox/rpi-node:${tag}
done

echo "
FROM arm32v6/alpine
COPY ./qemu-arm-static /usr/bin/qemu-arm-static
RUN apk add --no-cache nodejs npm
" > ./Dockerfile

docker pull --platform=linux/arm arm32v6/alpine
docker build --platform=linux/arm --no-cache -t brewblox/rpi-node:10-alpine .
docker push brewblox/rpi-node:10-alpine

rm ./Dockerfile
rm ./qemu-arm-static

popd > /dev/null
