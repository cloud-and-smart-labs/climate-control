import asyncio
import json
import os
import threading

import serial
import websockets


class Generator:
    """
    Port name Generator
    Example port name: /dev/ttyACM0
    """

    def __init__(self) -> None:
        self.prefix = '/dev/ttyACM'
        self.index = -1

    def generator(self):
        "Create Generator object"

        while True:
            self.index += 1
            yield f'{self.prefix}{self.index}'


def data_collect(port: str, data_collection: list) -> None:
    "Data collection method"

    serial_port = serial.Serial(port, 9600, timeout=1)
    serial_port.flush()
    data_set = dict()

    while True:
        try:
            # Read the data from serial port
            data = serial_port.readline().decode('utf-8').rstrip()

            # Convert to JSON format
            for row in data.split('\n'):
                if len(row):
                    key, value = tuple(row.split(':'))
                    data_set[key] = value

            packet = dict()
            packet[port] = data_set

            # Add into the shared list
            data_collection.append(json.dumps(packet))
            print(json.dumps(packet, indent=4))

        except Exception as e:
            print(str(e))
            exit()


async def publisher(data: list, host='localhost', port=80) -> None:
    # Connect broker
    async with websockets.connect(f'ws://{host}:{port}') as broker:
        await broker.send('''{"type": "publish"}''')

        while True:
            # Keep publishing
            while len(data):
                await broker.send(data.pop(0))


if __name__ == '__main__':

    # Default values
    TOTAL_PORT = 2
    PORT = 8080
    HOST = 'localhost'

    # Set values passed by env varibales
    if 'PORTS' in os.environ:
        TOTAL_PORT = int(os.environ['PORTS'])
    if 'PORT' in os.environ:
        PORT = int(os.environ["PORT"])
    if 'HOST' in os.environ:
        HOST = os.environ["HOST"]

    # Serial ports connected to arduino nano 33 ble sense
    serial_ports = set()
    collection_threads = list()

    # Shared data list B/W threads
    data_collection = list()

    # Port name generator
    port_name = Generator().generator()
    for _ in range(TOTAL_PORT):
        serial_ports.add(next(port_name))

    print(serial_ports)

    # Starting one thread per port
    for serial_port in serial_ports:
        t = threading.Thread(target=data_collect, args=(
            serial_port, data_collection), name=serial_port)
        t.start()
        collection_threads.append(t)

    # Start publisher
    asyncio.run(publisher(data_collection, host=HOST, port=PORT))
