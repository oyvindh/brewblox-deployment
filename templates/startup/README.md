# Running Docker Compose UI on startup in Raspberry

Source: https://raspberrypi.stackexchange.com/questions/78991/running-a-script-after-an-internet-connection-is-established

## Installation

* Copy files in this directory to `~/startup/` on the Raspberry Pi
* In the `startup/` directory, run `configure_service.sh`
* Reboot the Raspberry Pi

## SSH commands

Run these commands from the current directory.
Replace `raspberrypi` with its actual IP address.

```
scp -r . pi@raspberrypi:~/ && \
ssh pi@raspberrypi "cd startup && bash configure_service.sh && sudo reboot"
```
