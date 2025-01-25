import asyncio
from bleak import BleakScanner, BleakClient
# from PyObjCTools import KeyValueCoding

uuid_battery_level_characteristic = '00002a19-0000-1000-8000-00805f9b34fb'


async def main():
    # devices = await BleakScanner.discover()
    # for d in devices:
    #     if KeyValueCoding.getKey(d.details, 'name') == 'awesomecoolphone':
    #         myDevice = d
    #         print('Found it')

    # address = str(KeyValueCoding.getKey(myDevice.details, 'identifier'))
    async with BleakClient('80:C3:BA:4E:F1:9D') as client:
        # print(client.get_services())
        battery_level = await client.read_gatt_char(uuid_battery_level_characteristic)
        print(f'Battery level: {int.from_bytes(battery_level)}%')


asyncio.run(main())