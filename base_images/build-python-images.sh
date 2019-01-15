#! /bin/bash
set -e

pushd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )" > /dev/null

sudo apt update
sudo apt install -y qemu qemu-user-static qemu-user binfmt-support
cp $(which qemu-arm-static) .

python3 ./enable_experimental.py

PYTHON_TAGS="3.7 3.7-slim"

for tag in ${PYTHON_TAGS}; do
    echo "
    FROM arm32v7/python:${tag}
    COPY ./qemu-arm-static /usr/bin/qemu-arm-static
    " > ./Dockerfile

    docker pull --platform=linux/arm arm32v7/python:${tag}
    docker build --platform=linux/arm --no-cache -t brewblox/rpi-python:${tag} .
    docker push brewblox/rpi-python:${tag}
done

rm ./Dockerfile
rm ./qemu-arm-static

popd > /dev/null
