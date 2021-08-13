import pygatt

adapter = pygatt.GATTToolBackend()

try:
    adapter.start()
    device = adapter.connect('80:6F:B0:F0:2B:95')   # target MAC address
    value = device.char_read("f000aa01-0451-4000-b000-000000000000")    # temperature data UUID
    print(value)
finally:
    adapter.stop()
