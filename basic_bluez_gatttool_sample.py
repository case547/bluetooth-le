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

char_keys = device.discover_characteristics().keys()
num_keys = len(char_keys)
logging.info(f"There are {num_keys} characteristics to read")

for uuid in char_keys:
    attempt = 1
    while True:
        try:
            print("Read UUID %s: %s" % (uuid, binascii.hexlify(device.char_read(uuid))))
            num_keys -= 1
            logging.info(f"{num_keys} characteristics left to read")
        except:
            logging.warning(f"Attempt {attempt} failed. Trying again...")

            try:
                device = adapter.connect(device_addr)
            except:
                pass

            if attempt >= 3:
                num_keys -= 1
                logging.warning(f"Attempt {attempt} failed. Moving on... \n {num_keys} characteristics left to read")
                break

            attempt += 1
            continue
        
        break

print("Done")