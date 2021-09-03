"""
Notifications
-------------
Add notifications to a characteristic and handle the responses.
"""

import sys
import logging
import asyncio
import platform

from bleak import BleakClient
from bleak import _logger as logger

sensor_ids = {
    "temp": "f000aa01-0451-4000-b000-000000000000",
    "humidity": "f000aa21-0451-4000-b000-000000000000",
    "lux": "f000aa71-0451-4000-b000-000000000000",
}

CHARACTERISTIC_UUID = sensor_ids["lux"]
ADDRESS = "80:6F:B0:F0:2B:95"

if len(sys.argv) == 3:
    ADDRESS = sys.argv[1]
    CHARACTERISTIC_UUID = sys.argv[2]


def notification_handler(sender, data):
    """Simple notification handler that prints the data received."""
    print(f"{sender}: {data}")


async def run(address, debug=False):
    if debug:
        import sys

        l = logging.getLogger("asyncio")
        l.setLevel(logging.DEBUG)
        h = logging.StreamHandler(sys.stdout)
        h.setLevel(logging.DEBUG)
        l.addHandler(h)
        logger.addHandler(h)

    async with BleakClient(address) as client:
        logger.info(f"Connected: {client.is_connected}")

        await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
        await asyncio.sleep(5.0)
        await client.stop_notify(CHARACTERISTIC_UUID)


if __name__ == "__main__":
    import os

    os.environ["PYTHONASYNCIODEBUG"] = str(1)
    loop = asyncio.get_event_loop()
    # loop.set_debug(True)
    loop.run_until_complete(run(ADDRESS, True))