import asyncio
import functools
from bleak import BleakClient, BleakScanner, BleakError

connected_devices = set()
notify_uuid = "00002A37-0000-1000-8000-00805F9B34FB"

def callback(client, characteristic, data):
    print(client.address, characteristic, data)

def disconnected_callback(client):
    connected_devices.remove(client.address)
    print("disconnect from", client.address)

def match_device(device, adv_data):
    return adv_data.local_name.startswith('BLE') and device.address not in connected_devices

async def scan_and_connect():
    while True:
        device = await BleakScanner.find_device_by_filter(match_device)

        if device is None:
            continue

        client = BleakClient(device, disconnected_callback=disconnected_callback)
        try:
            await client.connect()
            print("connected to", device.address)
            await client.start_notify(functools.partial(callback, client))
            connected_devices.add(device.address)

        except BleakError:
            await client.disconnect()
            disconnected_callback(client)

if __name__ == "__main__":
    asyncio.run(scan_and_connect())