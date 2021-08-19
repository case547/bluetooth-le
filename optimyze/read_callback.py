from __future__ import print_function

import sys
import time
from gattlib import GATTRequester, GATTResponse


class NotifyStatus(GATTResponse):
    def __init__(self):
        super(NotifyStatus, self).__init__()
        self.done = False

    def on_response(self, data):
        print("bytes received:", end=' ')
        for b in data:
            print(hex(ord(b)), end=' ')
        print("")

        self.done = True


class AsyncReader(object):
    def __init__(self, address):
        self.requester = GATTRequester(address, False)
        self.response = NotifyStatus()

        self.connect()
        self.request_data()
        self.loop()

    def connect(self):
        print("Connecting...", end=' ')
        sys.stdout.flush()

        self.requester.connect(True)
        print("OK!")

    def request_data(self):
        self.requester.read_by_uuid_async("e3290004-8862-42ae-9d81-e6e9ec0f5fdf", self.response)
        print("Data requested.")

    def loop(self):
        print("Awaiting response...")
        while not self.response.done:
            time.sleep(0.1)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: {} <addr>".format(sys.argv[0]))
        sys.exit(1)

    AsyncReader(sys.argv[1])