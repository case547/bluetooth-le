import sys
from bluetooth.ble import GATTRequester


class Reader:
    def __init__(self, address):
        self.requester = GATTRequester(address, False)
        self.connect()
        self.request_name()

    def connect(self):
        print("Connecting...", end=" ")
        sys.stdout.flush()

        self.requester.connect(True)
        print("OK.")

    def request_name(self):
        name = self.requester.read_by_uuid(
            "00002a00-0000-1000-8000-00805f9b34fb")[0]
        try:
            print("Device name:", name.decode("utf-8"))
        except AttributeError:
            print("Device name:", name)

    def request_data(self):
        print("Requesting data...")
        
        for _ in range(10):
            data = self.requester.read_by_uuid(sys.argv[2])[0]
            try:
                print(f"  {data.decode('utf-8')}")
            except AttributeError:
                print(f"  {data}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <addr> <uuid>")
        sys.exit(1)

    Reader(sys.argv[1])
    print("Done.")