"""PyBluez simple example inquiry.py

Performs a simple device inquiry followed by a remote name request of each discovered device
"""

import bluetooth

print("Performing inquiry...")

nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True,
                                            flush_cache=True, lookup_class=False)

print(f"Found {len(nearby_devices)} devices.")

for addr, name in nearby_devices:
    try:
        print(f"   {addr} - {name}")
    except UnicodeEncodeError:
        print(f"   {addr} - {name.encode('utf-8', 'replace')}")