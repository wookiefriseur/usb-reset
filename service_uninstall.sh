#!/bin/bash

sudo systemctl disable usb-reset
sudo systemctl stop usb-reset
sudo systemctl daemon-reload

sudo rm -f /usr/local/bin/usb-reset
sudo rm -f  /etc/systemd/system/usb-reset.service

