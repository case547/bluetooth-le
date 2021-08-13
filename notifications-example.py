import pygatt
from binascii import hexlify
import time

adapter = pygatt.GATTToolBackend()

def handle_data(handle, value):
    """
    handle -- integer, characteristic read handle the data was received on
    value -- bytearray, the data returned in the notification
    """
    print("Received data: %s" % hexlify(value))

while True:
    try:
        adapter.start()
        device = adapter.connect('80:6F:B0:F0:2B:95')

        device.subscribe("f000aa01-0451-4000-b000-000000000000",
                        callback=handle_data)

        # The subscription runs on a background thread. You must stop this main
        # thread from exiting, otherwise you will not receive any messages, and
        # the program will exit. Sleeping in a while loop like this is a simple
        # solution that won't eat up unnecessary CPU, but there are many other
        # ways to handle this in more complicated program. Multi-threaded
        # programming is outside the scope of this README.
        print("Running")
        time.sleep(5)
    finally:
        adapter.stop()
        break