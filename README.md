# USB Reset

Status: Work in progress

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

* make [install.sh](service_install.sh) executable
* make [uninstall.sh](service_uninstall.sh) executable
* run [install.sh](service_install.sh) (will ask for sudo)


## Requirements

* `python3`
* `dmesg`
* `echo`
* running as superuser
