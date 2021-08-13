from __future__ import print_function

import binascii
import pygatt

device_addr = "80:6F:B0:F0:2B:95"
adapter = pygatt.GATTToolBackend()
adapter.start()
device = adapter.connect(device_addr)

for uuid in device.discover_characteristics().keys():
    attempt = 1
    while True:
        try:
            print("Read UUID %s: %s" % (uuid, binascii.hexlify(device.char_read(uuid))))
        except:
            device = adapter.connect(device_addr)

            if attempt >= 3:
                break

            attempt += 1
            continue
        
        break

print("Done")