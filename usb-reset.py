#! /usr/bin/python3

import os
import sys
import re

#ToDo: filter only crashes (got to wait for next crash to see what strings to filter)
#ToDo: add id capture group 'usb-(?P<id>\d{4}:\d{2}:\d{2}\.\d)'???
PATTERN = re.compile('^\[\s*(?P<time>\d+\.\d+)\]\s*(?P<msg>.+)\n$', re.IGNORECASE)

def parse(text: str) -> tuple[float,str]:
    match = PATTERN.match(text)
    if None or not(hasattr(match, 'groupdict')): 
        raise Exception("Invalid line format, could not match.")

    return (float(match.groupdict()['time']), match.groupdict()['msg'])

# ToDo: dummy for now, write directly to file or execute shell echo command
def usb_reset(device_type: str = 'xhci_hcd', device_id: str = '0000:04:00.3'):
    sys.stdout.write(f"ACTION:\techo -n \"{device_id}\" > /sys/bus/pci/drivers/{device_type}/unbind\n")
    sys.stdout.write(f"ACTION:\techo -n \"{device_id}\" > /sys/bus/pci/drivers/{device_type}/bind\n")
    return

def main():
    with os.popen('dmesg --follow') as msg:
        last_reset_time = 0.0
        for line in msg:
            try:
                time,msg = parse(line)
                sys.stdout.write(f"{time}:\t{msg}\n")

                # ToDo: reset device
                if time > last_reset_time:
                    usb_reset()
                    last_reset_time = time
            except Exception as ex:
                sys.stderr.write(f"ERROR: {ex}")


# Entrypoint when executed directly
if __name__ == '__main__':
    main()
