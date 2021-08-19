from __future__ import print_function

import sys
import time
from gattlib import GATTRequester, GATTResponse


class AsyncReader(object):
    def __init__(self, address):
        self.requester = GATTRequester(address, False)
        self.response = GATTResponse()

        self.connect()
        self.request_data()
        self.wait_response()

    def connect(self):
        print("Connecting...", end=' ')
        sys.stdout.flush()

        self.requester.connect(True, channel_type='random')
        print("OK!")

    def request_data(self):
        self.requester.read_by_uuid_async(
            "e3290004-8862-42ae-9d81-e6e9ec0f5fdf", self.response)

    def wait_response(self):
        while not self.response.received():
            time.sleep(0.1)

        data = self.response.received()[0]

        print("bytes received:", end=' ')
        for b in data:
            print(hex(ord(b)), end=' ')
        print("")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: {} <addr>".format(sys.argv[0]))
        sys.exit(1)

    AsyncReader(sys.argv[1])
    print("Done.")