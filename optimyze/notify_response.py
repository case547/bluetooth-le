from gattlib import GATTRequester, GATTResponse
import time

class NotifyStatus(GATTResponse):
    def on_response(self, status):
        print(f"Status: {status}")

response = NotifyStatus()
req = GATTRequester("DB:88:84:FD:CE:20")
req.connect(False, channel_type='random')
req.read_by_uuid_async("e3290004-8862-42ae-9d81-e6e9ec0f5fdf", response)

while True:
    # here, do other interesting things
    time.sleep(1)