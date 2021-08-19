from os import write
from gattlib import GATTRequester, GATTResponse
import time
import struct

req = GATTRequester("DB:88:84:FD:CE:20", False)
response = GATTResponse()

req.connect(True, channel_type='random')

print("Checking device availability...")

for i in range(10):
    status_char = req.read_by_uuid("e3290004-8862-42ae-9d81-e6e9ec0f5fdf")
    busy_flag = bin(status_char[-1])[-1]
    
    if busy_flag == '0':
        print("OK!")
        break

    if i == 9:
        raise TimeoutError("Device is busy.")

    time.sleep(1)

now = round(time.time())

param1 = struct.pack("<L", now - 15)
param2 = struct.pack("<L", now + 15)
param3 = b"\xff\xff\xff\xff"
param4 = b"\x00\x00\x00\x00"

req.write_cmd("e3290003-8862-42ae-9d81-e6e9ec0f5fdf",
    b'\x00\x03' + param1 + param2 + param3 + param4
)

req.read_by_uuid_async("e3290002-8862-42ae-9d81-e6e9ec0f5fdf", response)

print("Awaiting response")
while not response.received():
    time.sleep(0.1)

steps = response.received()[0]