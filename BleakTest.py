# https://pypi.org/project/bleak/
# BleakClient The operation was canceled by the user

# 80:C3:BA:4E:F1:9D: HD 450BT
# ---------------------------
# AdvertisementData(local_name='HD 450BT', service_uuids=['0000180f-0000-1000-8000-00805f9b34fb', '0000180a-0000-1000-8000-00805f9b34fb', '0000fdce-0000-1000-8000-00805f9b34fb'], rssi=-43)

import asyncio
from types import NoneType


from bleak import BleakScanner, BleakError, BaseBleakClient
from bleak import BleakClient
from bleak.exc import BleakDeviceNotFoundError

# Renpho
# MAC: str = 'ED:67:39:4E:3D:DE'
# TYPE = 'ES-CS20M'
# CODE = '0000800008ED67394E3DDE'

# MAC = '94:24:B8:0D:79:7B' # GR-AC_10001_09_797b_SC
# UUID_DEVICE_NAME = '00002a00-0000-1000-8000-00805f9b34fb'

# SENNHEISER HD 450BT
MAC: str = '80:C3:BA:4E:F1:9D'

# Pixel 7a
# MAC: str = '74:74:46:AB:84:7D'

# Samsug
# MAC: str = '6C:00:6B27:02:60'

UUID_BATTERY_LEVEL_CHARACTERISTIC = '00002a19-0000-1000-8000-00805f9b34fb'


async def main1():
    devices = await BleakScanner.discover()
    for device in devices:
        # if device.name != NoneType:
        print(f'address={str(device.address)}, name={device.name}, rssi={device._rssi}, metadata={device._metadata}, details={device.details}')
        if str(device.address) == MAC:
            print('-------------------------')


async def main2():
    # while True:
    try:
        device = await BleakScanner.find_device_by_address(MAC)
        if device is None:
            print('Not found')
            return
        else:
            print(f'Found: {device}')
            client = BleakClient(device)
            await client.connect()
            # async with BleakClient(device, winrt={"use_cached_services": False}) as client:

                # print(f'Pair: {await client.pair()}')

            temperature = await client.read_gatt_char(UUID_BATTERY_LEVEL_CHARACTERISTIC)
            print("Temperature: {0} Celsius".format(int.from_bytes(temperature, byteorder='little', signed=True) / 100))

            print(f'Address={client.address}')
            if client.is_connected:
                for service in client.services:
                    print(f'Service uuid={service.uuid}, handle={service.handle}, description={service.description}')
                    for characteristic in service.characteristics:
                        print(f'\tcharacteristic=uuid:{characteristic.uuid}, description:{characteristic.description}, properties:{characteristic.properties}')
                        try:
                            gatt_char = await client.read_gatt_char(characteristic.uuid)
                            print(f'\t{characteristic.description}={gatt_char}')
                            # client.connect()
                        except Exception as e:
                            print(f'\t\t{e}')
                            await client.connect()
                        # for descriptor in characteristic.descriptors:
                        #     print(f'\t\tdescriptor:{descriptor}')
                        if 'read' in characteristic.properties:
                            try:
                                gatt_char = await client.read_gatt_char(characteristic.uuid)
                                print(f'\t{characteristic.description}={gatt_char}')
                                # client.connect()
                            except Exception as e:
                                print(f'\t\t{e}')
                                await client.connect()

                            for descriptor in characteristic.descriptors:
                                print(f'\t\tdescriptor:{descriptor}')
                        else:
                            print('\t\tNot read')
                        # # if characteristic.uuid == UUID_BATTERY_LEVEL_CHARACTERISTIC:
                        #     try:
                        #         value = await client.read_gatt_char(characteristic.uuid)
                        #         print(f'\t\tvalue: {str(value)}, {int.from_bytes(value)}')
                        #     except BleakError as ex:
                        #         print(ex)

            print('--------------------')

        # async with BleakClient(MAC) as client:
        #     await client.connect()
            # data = await client.read_gatt_char(UUID_BATTERY_LEVEL_CHARACTERISTIC)
            # print(f"received: {data}")
            # print(client.address)
            # if client.is_connected:
            #     for service in client.services:
            #         print(f'uuid={service.uuid}')
            #         print(f'handle={service.handle}')
            #         print(f'description={service.description}')
            #         for characteristic in service.characteristics:
            #             print(f'\tcharacteristic=uuid:{characteristic.uuid}, description:{characteristic.description}, properties:{characteristic.properties}')
            #             for descriptor in characteristic.descriptors:
            #                 print(f'\t\tdescriptor:{descriptor}')
            #             # if 'read' in characteristic.properties:
            #             #     print('toto')
            #             # # if characteristic.uuid == UUID_BATTERY_LEVEL_CHARACTERISTIC:
            #             #     try:
            #             #         value = await client.read_gatt_char(characteristic.uuid)
            #             #         print(f'\t\tvalue: {str(value)}, {int.from_bytes(value)}')
            #             #     except BleakError as ex:
            #             #         print(ex)
            #
            #     print('--------------------')
                # battery_level = await client.read_gatt_char(UUID_BATTERY_LEVEL_CHARACTERISTIC)
                # print(f'Battery level: {int.from_bytes(battery_level)}%')
                # print()
    except Exception as e:
        print(e)


asyncio.run(main2())
