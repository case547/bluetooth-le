import sys

from bluetooth.ble import GATTRequester


class Reader:

    def __init__(self, address):
        self.requester = GATTRequester(address, False)
        self.connect()
        self.request_data()

    def connect(self):
        print("Connecting...", end=" ")
        sys.stdout.flush()

        self.requester.connect(True)
        print("OK.")

    def request_data(self, uuid):
        data = self.requester.read_by_uuid(uuid)[0]
        try:
            print("Device name:", data.decode("utf-8"))
        except AttributeError:
            print("Device name:", data)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <addr>".format(sys.argv[0]))
        sys.exit(1)

    Reader(sys.argv[1])
    print("Done.")