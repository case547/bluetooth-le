import pygatt
from binascii import hexlify

adapter = pygatt.GATTToolBackend()

try:
    adapter.start()
    device = adapter.connect('80:6F:B0:F0:2B:95')   # target MAC address
    while True:
        value = device.char_read("f000aa71-0451-4000-b000-000000000000")    # luxometer data UUID
        print(f"Received data: {hexlify(value)}")
finally:
    adapter.stop()
