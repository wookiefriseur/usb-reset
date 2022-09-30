#!/bin/bash

chmod +x usbreset.py
sudo cp usbreset.py /usr/local/bin/usb-reset
sudo cp usb-reset.service  /etc/systemd/system/usb-reset.service

sudo systemctl enable usb-reset
sudo systemctl daemon-reload
sudo systemctl start usb-reset
