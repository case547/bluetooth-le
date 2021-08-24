"""
Async callbacks with a queue and external consumer
--------------------------------------------------
How async notification callbacks can be used to send data received
through notifications to some external consumer of that data.
"""
import sys
import time
import platform
import asyncio
import logging

from bleak import BleakClient

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
h = logging.StreamHandler(sys.stdout)
h.setLevel(logging.DEBUG)
log.addHandler(h)

sensor_ids = {
    "temp": "f000aa01-0451-4000-b000-000000000000",
    "humidity": "f000aa21-0451-4000-b000-000000000000",
    "lux": "f000aa71-0451-4000-b000-000000000000",
}

ADDRESS = "80:6F:B0:F0:2B:95"
NOTIFICATION_UUID = sensor_ids["lux"]
if len(sys.argv) == 3:
    ADDRESS = sys.argv[1]
    NOTIFICATION_UUID = sys.argv[2]


async def run_ble_client(address: str, queue: asyncio.Queue):
    async def callback_handler(sender, data):
        await queue.put((time.time(), data))

    async with BleakClient(address) as client:
        log.info(f"Connected: {client.is_connected}")
        await client.start_notify(NOTIFICATION_UUID, callback_handler)
        await asyncio.sleep(10.0)
        await client.stop_notify(NOTIFICATION_UUID)
        # Send an "exit command to the consumer"
        await queue.put((time.time(), None))


async def run_queue_consumer(queue: asyncio.Queue):
    while True:
        # Use await asyncio.wait_for(queue.get(), timeout=1.0) if you want a timeout for getting data.
        epoch, data = await queue.get()
        if data is None:
            log.info(
                "Got message from client about disconnection. Exiting consumer loop..."
            )
            break
        else:
            log.info(f"Received callback data via async queue at {epoch}: {data}")


async def main(address: str):
    queue = asyncio.Queue()
    client_task = run_ble_client(address, queue)
    consumer_task = run_queue_consumer(queue)
    await asyncio.gather(client_task, consumer_task)
    log.info("Main method done.")


if __name__ == "__main__":
    asyncio.run(main(ADDRESS))