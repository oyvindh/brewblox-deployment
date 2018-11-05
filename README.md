# BrewBlox Deployment

This repository contains integration tests for BrewBlox, and example configurations for getting started.

# Getting Started

### Requirements

- Raspberry Pi or Linux desktop computer
- BrewPi Spark controller
- Git
- Docker
- Docker-compose

### Clone the repository

In your terminal, run

```
git clone https://github.com/BrewBlox/brewblox-deployment.git
```

### Select a configuration

There are two sets of configurations, AMD, and ARM.

If you're installing BrewBlox on a desktop computer, choose `brewblox-deployment/amd`. <br>
If you're installing Brewblox on a Raspberry Pi, choose `brewblox-deployment/arm`.

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
