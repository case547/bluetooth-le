import asyncio
from bleak import BleakClient

address = "80:6F:B0:F0:2B:95"
DEV_NAME_UUID = "00002a00-0000-1000-8000-00805f9b34fb"

async def run(address):
    async with BleakClient(address) as client:
        device_name = await client.read_gatt_char(DEV_NAME_UUID)
        print("Device name:", device_name.decode("utf-8"))

loop = asyncio.get_event_loop()
loop.run_until_complete(run(address))
