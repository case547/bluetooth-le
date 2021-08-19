from gattlib import GATTRequester, GATTResponse
import time

req = GATTRequester("DB:88:84:FD:CE:20", False)
response = GATTResponse()

req.connect(True, channel_type='random')
req.read_by_uuid_async("e3290004-8862-42ae-9d81-e6e9ec0f5fdf", response)

print("Awaiting response")
while not response.received():
    time.sleep(0.1)

steps = response.received()[0]