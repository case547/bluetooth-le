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
        except:
            if attempt < 3:
                logging.warning(f"Attempt {attempt} failed. Trying again...")
            else:
                num_keys -= 1
                logging.warning(f"Attempt {attempt} failed. Moving on... \n {num_keys} characteristics left to read")
                break

            try:
                device = adapter.connect(device_addr)
            except:
                pass    

            attempt += 1
            continue
        
        logging.info(f"{num_keys} characteristics left to read")

        break

print("Done")