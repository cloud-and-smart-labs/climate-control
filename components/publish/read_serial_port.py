import serial
import json
import threading
import os


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


def data_collect(port: str) -> None:
    "Data collection method"

    serial_port = serial.Serial(port, 9600, timeout=1)
    serial_port.flush()
    data_set = dict()
    data_set['port'] = port

    while True:
        try:
            data = serial_port.readline().decode('utf-8').rstrip()
            for row in data.split('\n'):
                if len(row):
                    key, value = tuple(row.split(':'))
                    data_set[key] = value

            json_string = json.dumps(data_set)

            print(json.dumps(data_set, indent=4))

        except Exception as e:
            print(str(e))
            exit()


TOTAL_PORT = 1
if 'PORTS' in os.environ:
    TOTAL_PORT = int(os.environ['PORTS'])

serial_ports = set()
data_collectors = list()
port_name = Generator().generator()

for _ in range(TOTAL_PORT):
    serial_ports.add(next(port_name))

print(serial_ports)
for serial_port in serial_ports:
    t = threading.Thread(target=data_collect, args=(
        serial_port,), name=serial_port)
    t.start()
    data_collectors.append(t)
