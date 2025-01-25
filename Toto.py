import asyncio
from types import NoneType


from bleak import BleakScanner, BleakError
from bleak import BleakClient
from bleak.exc import BleakDeviceNotFoundError

# Renpho
# MAC: str = 'ED:67:39:4E:3D:DE'
UUID_BATTERY_LEVEL_CHARACTERISTIC = '00002a19-0000-1000-8000-00805f9b34fb'

# SENNHEISER HD 450BT
# MAC: str = '80:C3:BA:4E:F1:9D'

# Pixel 7a
MAC: str = '74:74:46:AB:84:7D'

async def scan_and_connect():
    device = await BleakScanner.find_device_by_address(MAC)
    if not device:
        print("Device not found")
        return

    async with BleakClient(device) as client:
        temperature = await client.read_gatt_char(UUID_BATTERY_LEVEL_CHARACTERISTIC)
        print("Temperature: {0} Celsius".format(int.from_bytes(temperature, byteorder='little', signed=True) / 100))

# Do have one async main function that does everything.
async def main():
    while True:
        await scan_and_connect()
        # Do use asyncio.sleep() in an asyncio program.
        await asyncio.sleep(5)

asyncio.run(main())