from __future__ import print_function

import binascii
import pygatt
import logging

logging.basicConfig()
logging.getLogger('pygatt').setLevel(logging.DEBUG)

device_addr = "80:6F:B0:F0:2B:95"
adapter = pygatt.GATTToolBackend()
adapter.start()
device = adapter.connect(device_addr)

# reads_left = len(device.discover_characteristics())
# logging.info(f"There are {reads_left} characteristics to read")

for uuid in device.discover_characteristics().keys():
    attempt = 1
    while True:
        try:
            device = adapter.connect(device_addr)
            print("Read UUID %s: %s" % (uuid, binascii.hexlify(device.char_read(uuid))))
            # reads_left -= 1
            # logging.info(f"{reads_left} characteristics left to read")
        except:
            logging.warning(f"Attempt {attempt} failed. Trying again...")

            if attempt >= 3:
                # reads_left -= 1
                logging.warning(f"Attempt {attempt} failed. Moving on... \n  characteristics left to read")
                break

            attempt += 1
            continue
        
        break

print("Done")