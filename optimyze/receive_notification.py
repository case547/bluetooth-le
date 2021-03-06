from __future__ import print_function

import sys
from threading import Event
from gattlib import GATTRequester


class Requester(GATTRequester):
    def __init__(self, wakeup, *args):
        GATTRequester.__init__(self, *args)
        self.wakeup = wakeup

    def on_notification(self, handle, data):
        print(f"- notification on handle: {handle}\n")
        self.wakeup.set()


class ReceiveNotification(object):
    def __init__(self, address):
        self.received = Event()
        self.requester = Requester(self.received, address, False)

        self.connect()
        self.wait_notification()

    def connect(self):
        print("Connecting...", end=' ')
        sys.stdout.flush()

        self.requester.connect(True, channel_type='random')
        print("OK!")

    def wait_notification(self):
        print("\nThis is a bit tricky. You need to make your device to send\n"
              "some notification. I'll wait...")
        self.received.wait()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: {} <addr>".format(sys.argv[0]))
        sys.exit(1)

    ReceiveNotification(sys.argv[1])
    print("Done.")