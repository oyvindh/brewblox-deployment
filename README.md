# BrewBlox Deployment

This repository contains integration tests for BrewBlox, and example configurations for getting started.

# Getting Started

### Requirements

- Raspberry Pi or Linux desktop computer / laptop
- BrewPi Spark controller

## Install

On the machine where you want to run BrewBlox, open your terminal, and navigate to the directory where you want to place the configuration files. A `./brewblox/` subdirectory will be automatically created.

Download and run the install script. This will install Docker, docker-compose, and the default BrewBlox configuration.

```
curl -sSL https://brewblox.netlify.com/install > install.sh
bash ./install.sh
```

## Flash the firmware

### Desktop computer

Connect the Spark to the computer using USB, and run the following commands:

```
docker pull brewblox/firmware-flasher:develop
docker run -it --rm --privileged brewblox/firmware-flasher:develop trigger-dfu
docker run -it --rm --privileged brewblox/firmware-flasher:develop flash
docker run -it --rm --privileged brewblox/firmware-flasher:develop flash-bootloader
```

### Raspberry Pi

Connect the Spark to the Raspberry Pi using USB, and run the following commands:

```
docker pull brewblox/firmware-flasher:rpi-develop
docker run -it --rm --privileged brewblox/firmware-flasher:rpi-develop trigger-dfu
docker run -it --rm --privileged brewblox/firmware-flasher:rpi-develop flash
docker run -it --rm --privileged brewblox/firmware-flasher:rpi-develop flash-bootloader
```

## Services

### Install

Pull the docker images. This may take a few minutes.

```
cd brewblox
docker-compose pull

# Run the first-time setup script
bash ./first-time.sh
```

### Start

In your terminal (in the `brewblox/` directory), run

```
docker-compose up -d
```

In your browser, visit the IP address of your computer or Raspberry Pi to open the UI.
