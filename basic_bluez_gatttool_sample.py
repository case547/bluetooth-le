from __future__ import print_function

import binascii
import pygatt

YOUR_DEVICE_ADDRESS = "80:6F:B0:F0:2B:95"
# Many devices use random addressing - this is required to connect
ADDRESS_TYPE = pygatt.BLEAddressType.random

adapter = pygatt.GATTToolBackend()
adapter.start()
device = adapter.connect(YOUR_DEVICE_ADDRESS, address_type=ADDRESS_TYPE)

for uuid in device.discover_characteristics().keys():
    print("Read UUID %s: %s" % (uuid, binascii.hexlify(device.char_read(uuid))))