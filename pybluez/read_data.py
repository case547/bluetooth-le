import sys
from bluetooth.ble import GATTRequester


class Reader:
    def __init__(self, address):
        self.requester = GATTRequester(address, False)
        self.connect()
        self.request_name()
        self.activate()

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

    def activate(self):
        self.requester.write_by_uuid(
            "f000aa02-0451-4000-b000-000000000000", b'\x01')
        self.requester.write_by_uuid(
            "f000aa22-0451-4000-b000-000000000000", b'\x01')
        self.requester.write_by_uuid(
            "f000aa72-0451-4000-b000-000000000000", b'\x01')

    def request_data(self, uuid):
        print("Requesting data...")
        
        for _ in range(10):
            data = self.requester.read_by_uuid(uuid)[0]
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