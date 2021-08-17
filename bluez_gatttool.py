from __future__ import print_function

import binascii
from os import read
import pygatt
import logging
from pprint import pprint
import struct

logging.basicConfig()
logging.getLogger('pygatt').setLevel(logging.DEBUG)

device_addr = "80:6F:B0:F0:2B:95"
adapter = pygatt.GATTToolBackend()
adapter.start()
device = adapter.connect(device_addr)

char_keys = device.discover_characteristics().keys()
num_keys = len(char_keys)

read_chars = {}

logging.info(f"There are {num_keys} characteristics to read")

for uuid in char_keys:
    attempt = 1
    while True:
        try:
            read_char = device.char_read(uuid)
            print("Read UUID %s: %s" % (uuid, struct.unpack("<f", read_char)))
            read_chars[uuid] = binascii.hexlify(read_char)
            num_keys -= 1
            logging.info(f"{num_keys} characteristics left to read")
        except:
            if attempt < 3:
                logging.warning(f"Attempt {attempt} failed. Trying again...")
            else:
                num_keys -= 1
                logging.warning(f"Attempt {attempt} failed. Moving on...\n{num_keys} characteristic(s) left to read")
                break

            try:
                device = adapter.connect(device_addr)
            except:
                pass    

            attempt += 1
            continue

        break

pprint(read_chars)