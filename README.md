# USB Reset

## Purpose

I have an old laptop of which the USB hubs crash from time to time, disabling my peripherals.

Until the issue is identified I'm using the following script to rebind:
```sh
echo -n "<ID>" > /sys/bus/pci/drivers/xhci_hcd/unbind
echo -n "<ID>" > /sys/bus/pci/drivers/xhci_hcd/bind
```

The tool's purpose is to automate this process by:
* looking for USB hub crashes
* resetting hubs after a crash


## Setup

* make [dmesg-watcher.py](dmesg-watcher.py) executable
* add [dmesg-watcher.py](dmesg-watcher.py) as a background service
* set the service to autostart


## Requirements

* `python3`
* `dmesg`
* `echo`
* running as superuser
