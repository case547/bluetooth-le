from bluetooth.ble import DiscoveryService

service = DiscoveryService()
devices = service.discover(2)

for addr, name in devices.items():
    try:
        print(f"   {addr} - {name}")
    except UnicodeEncodeError:
        print(f"   {addr} - {name.encode('utf-8', 'replace')}")