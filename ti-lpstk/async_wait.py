from gattlib import GATTRequester, GATTResponse
import time

sensor_hnds = {"temp": 0x002f, "humidity": 0x003a, "lux": 0x0045}

class Notify(GATTResponse):
    def on_response(self, name):
        print("Requested data: {}".format(name))

response = Notify()
req = GATTRequester("80:6F:B0:F0:2B:95")
req.read_by_handle_async(sensor_hnds["temp"], response)

while True:
    # here, do other interesting things
    time.sleep(1)
