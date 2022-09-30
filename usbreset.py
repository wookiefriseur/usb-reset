#! /usr/bin/python3

import os
import re
import sys
import time

from threading import Thread

class USBReset:
    SERVICE_NAME = 'USBReset'

    LOG_LVL_NONE = 0
    LOG_LVL_ERR = 1
    LOG_LVL_WARN = 2
    LOG_LVL_INFO = 3
    LOG_LVL_DEBUG = 4

    #[ 8964.807279] xhci_hcd 0000:04:00.3: WARNING: Host System Error
    #[35873.575441] xhci_hcd 0000:04:00.3: xHCI host not responding to stop endpoint command
    #[35873.575473] xhci_hcd 0000:04:00.3: xHCI host controller not responding, assume dead
    #[35873.575488] xhci_hcd 0000:04:00.3: HC died; cleaning up

    ERRORS = ['WARNING: Host System Error']
    PATTERN = re.compile('^\[\s*(?P<time>\d+\.\d+)\]\s+(?P<device>[\w_]+)\s+(?P<id>\d{4}:\d{2}:\d{2}\.\d)(?P<msg>.+)\n?$', re.IGNORECASE)

    def __init__(self, loglvl: int = LOG_LVL_INFO) -> None:
        self.loglvl = loglvl
        self.request_stack = []
        self.latest_request = dict()

        self.log('Starting USB-Reset service')
        t = Thread(target=self.reset_request_listener)
        try:
            t.start()
        except InterruptedError:
            # ToDo: shut down gracefully, handle SIGTERM etc
            self.log('Stopping USB-Reset service')


    def reset_request_listener(self) -> None:
        """Listens to and processes incoming reset requests
        """
        self.log('Starting listener for incoming reset requests')
        time.sleep(5) # initial delay to let dmesg run, if started late

        while True:
            time.sleep(2)
            num_requests = len(self.request_stack)
            
            self.log(f"Reset requests: {num_requests}", self.LOG_LVL_DEBUG)
            if num_requests > 0:
                for _ in range(num_requests):
                    request = self.request_stack.pop()
                    
                    if request == None:
                        continue # "Es ist besser, nicht zu resetten, als falsch zu resetten."

                    if request['id'] in self.latest_request:
                        last_reset = self.latest_request[request['id']]
                        if request['time'] < last_reset:
                            continue # skip old requests
                    else:
                        self.latest_request[request['id']] = request['time']

                    # ToDo: reset keyboard and mouse up/down events as well?
                    last_reset = request['time'] + 10 # allow some time for reset to finish
                    self.log(f"{request['id']} down, trying to rebind", self.LOG_LVL_INFO)
                    os.system(f"echo -n \"{request['id']}\" > /sys/bus/pci/drivers/{request['device']}/unbind")
                    time.sleep(1.5)
                    os.system(f"echo -n \"{request['id']}\" > /sys/bus/pci/drivers/{request['device']}/bind")
                    self.latest_request[request['id']] = last_reset


    def request_reset(self,request: dict) -> None:
        self.request_stack.append(request)


    def log(self, msg: str, loglvl: int = LOG_LVL_INFO):
        """Custom format/channel for messages

        Args:
            msg (str): Message
        """
        if loglvl <= self.loglvl:
            sys.stdout.write(f"{self.SERVICE_NAME} {msg}\n")

    @classmethod
    def parse(cls,text: str) -> dict:
        """Parses a dmesg line and returns its content 

        Args:
            text (str): Line (with or without NL)

        Raises:
            Exception: If there is no match

        Returns:
            dict: named groups like `time`, `device`, `id`, `msg`
        """

        match = cls.PATTERN.match(text)
        if match == None or not(hasattr(match, 'groupdict')): 
            raise Exception("No match, not a host error.")

        result = dict(time=int(float(match['time'])), device=match['device'],id=match['id'], msg=match['msg'])

        return result

    @classmethod
    def is_error(cls, text: str) -> bool:
        """Check if text contains known error message
        """
        for error in cls.ERRORS:
            if text.__contains__(error): return True
        
        return False


def main():
    # ToDo: check for permission
    usbr = USBReset()

    with os.popen('dmesg --follow') as msg:
        for line in msg:
            try:
                match = usbr.parse(line)
                if usbr.is_error(match['msg']):
                    usbr.request_reset(match)
            except Exception:
                continue # no match, skip this line


# Entrypoint when executed directly
if __name__ == '__main__':
    main()
