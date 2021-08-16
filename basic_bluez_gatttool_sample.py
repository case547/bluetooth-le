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

num_keys = len(device.discover_characteristics().keys())
logging.info(f"There are {num_keys} characteristics to read")

for uuid in device.discover_characteristics().keys():
    attempt = 1
    while True:
        try:
            device = adapter.connect(device_addr)
            print("Read UUID %s: %s" % (uuid, binascii.hexlify(device.char_read(uuid))))
            num_keys -= 1
            logging.info(f"{num_keys} characteristics left to read")
        except:
            logging.warning(f"Attempt {attempt} failed. Trying again...")

            if attempt >= 3:
                num_keys -= 1
                logging.warning(f"Attempt {attempt} failed. Moving on... \n {num_keys} characteristics left to read")
                break

            attempt += 1
            continue
        
        break

print("Done")