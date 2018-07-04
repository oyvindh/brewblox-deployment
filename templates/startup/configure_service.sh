#! /bin/bash

sudo chown pi ./startup.sh
sudo chmod +x ./startup.sh

sudo cp ./compose_ui.service /etc/systemd/system/
sudo systemctl enable compose_ui.service
sudo systemctl start compose_ui.service
