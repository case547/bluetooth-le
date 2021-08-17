import pygatt
import struct
import time

import logging

logging.basicConfig()
logging.getLogger('pygatt').setLevel(logging.DEBUG)

adapter = pygatt.GATTToolBackend()

sensor_ids = {
    "temp_data": "f000aa01-0451-4000-b000-000000000000",
    "humidity_data": "f000aa21-0451-4000-b000-000000000000",
    "lux_data": "f000aa71-0451-4000-b000-000000000000",
}

try:
    adapter.start()
    device = adapter.connect('80:6F:B0:F0:2B:95')   # target MAC address
    device.char_write("f000aa72-0451-4000-b000-000000000000", 0)
    device.char_write("f000aa72-0451-4000-b000-000000000000", 1)
    while True:
        value = device.char_read(sensor_ids["lux_data"])
        print(struct.unpack("<f", value))
        time.sleep(1)
finally:
    adapter.stop()