"""read_data.py

Connects to given BLE device and fetches one of either temperature, humidity, or luxometer data.
Invoke by: $ python3 read_data.py <MAC address> <sensor(s): temp/humidity/lux>

Multi-Sensor MAC address: 80:6F:B0:F0:2B:95
"""

import sys
from bluetooth.ble import GATTRequester
import struct
import time
import signal


sensor_ids = {
    "temp": "f000aa01-0451-4000-b000-000000000000",
    "humidity": "f000aa21-0451-4000-b000-000000000000",
    "lux": "f000aa71-0451-4000-b000-000000000000",
}

class Reader:
    def __init__(self, address):
        self.requester = GATTRequester(address, False)
        self.connect()
        self.request_name()
        self.activate()
        self.request_data()

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
        self.requester.write_by_handle(51, b'\x01')     # IR temp config
        self.requester.write_by_handle(62, b'\x01')     # humidity config
        self.requester.write_by_handle(73, b'\x01')     # luxometer config

    def request_data(self):
        print("Requesting data...")
        
        interrupt_handler = InterruptHandler()

        while not interrupt_handler.got_signal:
            for i in range(2, len(sys.argv)):
                data = self.requester.read_by_uuid(sensor_ids[sys.argv[i]])[0]
                print(f"  {sys.argv[i]}: {struct.unpack('f', data)}")
            
            time.sleep(0.5)

class InterruptHandler:
    def __init__(self):
        self._signal_count = 0
        signal.signal(signal.SIGINT, self.interrupt_handler)

    @property
    def got_signal(self):
        return self._signal_count > 0

    def interrupt_handler(self, signum, frame):
        self._signal_count += 1
        if self._signal_count >= 3:
            raise KeyboardInterrupt

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <addr> <sensor(s)>")
        sys.exit(1)

    Reader(sys.argv[1])
    print("\nDone.")
