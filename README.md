# BrewBlox Deployment

This repository contains integration tests for BrewBlox, and example configurations for getting started.

# Getting Started

### Requirements

- Desktop / laptop computer
- Raspberry Pi or Linux desktop computer / laptop
- BrewPi Spark controller
- Git
- Docker
- Docker-compose


## Firmware

Note: While the services can be run on a Raspberry Pi, building and flashing the firmware must be done on an AMD64 / x86_64 system.

### Clone the firmware repository

In your terminal, run

```
git clone https://github.com/BrewPi/firmware.git
cd firmware
git checkout feature/brewblox
cd docker
```

### Put the Spark in DFU mode

- Connect the spark to your computer using the usb cable
- Unplug the spark usb cable
- There are two sunken buttons on the right side of the spark. Press and hold the top one (you'll need something pointy)
- Reconnect the usb cable while still holding the button
- Release the button: the led light should be blinking purple

### Flash the firmware

In your terminal (still in the firmware/docker directory), run

```
docker-compose up -d compiler
docker-compose exec compiler bash compile-proto.sh
sudo docker-compose exec compiler make APP=brewblox PLATFORM=p1 program-dfu
```

## Services

### Clone the deployment repository

In your terminal, run

```
git clone https://github.com/BrewBlox/brewblox-deployment.git
```

### Select a configuration

There are two sets of configurations available: `amd64`, and `armhf`.

If you're installing BrewBlox on a desktop computer, choose `brewblox-deployment/amd64`. <br>
If you're installing Brewblox on a Raspberry Pi, choose `brewblox-deployment/armhf`.

### Set Spark address

If you're connecting through USB, you do not need to make any changes. The Spark Service will autodetect the controller.

If you're connecting to a Spark Controller using WiFi, you must add its IP address to the configuration.
In your configuration's directory, open `docker-compose.yml`, and edit the following lines:

```yml
    # command: >
    #   --device-host=192.168.0.2
```

Remove the `#` to uncomment, and replace `192.168.0.2` with the IP address of your Spark Controller.

### Install

In your terminal, navigate to your chosen configuration, and run

```
docker-compose pull
```

This may take a few minutes.

### Start

In your terminal, run

```
docker-compose up -d
```

In your browser, visit the IP address of your computer or Raspberry Pi to open the UI.
