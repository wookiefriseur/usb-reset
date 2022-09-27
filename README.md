# USB Reset

## Purpose

I have an old laptop which USB hubs crash from time to time, disabling external mouse and keyboard.

Until the issue is identified I'm using the following script to rebind:
```sh
echo -n "<ID>" > /sys/bus/pci/drivers/xhci_hcd/unbind
echo -n "<ID>" > /sys/bus/pci/drivers/xhci_hcd/bind
```

## Requirements

* `dmesg`
* `echo`
* running as superuser
