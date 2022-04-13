import asyncio
import json
import os
import threading
import time

import serial
import websockets


class Lock:

    def __init__(self) -> None:
        self.status = True
        self.thread_ref = threading.Thread(target=self.controller)
        self.thread_ref.start()

    def controller(self) -> None:
        while True:
            self.status = False
            time.sleep(2)
            self.status = True
            time.sleep(0.5)


async def subscriber(host='localhost', port=80) -> None:
    serial_port = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    serial_port.flush()

    serial_port.write(bytes('0/0', 'utf-8'))
    time.sleep(1)
    serial_port.write(bytes('180/180', 'utf-8'))
    time.sleep(1)
    serial_port.write(bytes('0/0', 'utf-8'))
    time.sleep(1)

    lock = Lock()

    async with websockets.connect(f'ws://{host}:{port}') as broker:
        await broker.send('''{"type": "subscribe"}''')

        while True:
            try:
                signal = list()
                data_set = json.loads(await broker.recv())

                if lock.status:
                    for port in data_set.keys():
                        sum = 0
                        for value in list(data_set[port].values()):
                            if '.' in value:
                                sum += float(value)
                            else:
                                sum += int(value)

                        sum %= 180
                        signal.append(f'{int(sum)}')

                    actuation = '/'.join(signal)
                    print(actuation)
                    serial_port.write(bytes(actuation, 'utf-8'))

            except Exception as e:
                print(f'subscriber : {e}')


if __name__ == '__main__':

    PORT = 8080
    HOST = 'localhost'

    if 'PORT' in os.environ:
        PORT = int(os.environ["PORT"])
    if 'HOST' in os.environ:
        HOST = os.environ["HOST"]

    asyncio.run(subscriber(host=HOST, port=PORT))

    # import random

    # serial_port = serial.Serial('/dev/ttyACM2', 9600, timeout=1)
    # serial_port.flush()

    # while True:
    #     num = random.randint(0, 180)
    #     serial_port.write(bytes(f'{num}/{num}', 'utf-8'))

    #     print(serial_port.readline().decode('utf-8').rstrip())
