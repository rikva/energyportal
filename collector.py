# coding: utf-8

import serial
import time
import json
import db

SEPARATOR_LINE = b'\r\n'

ser = serial.Serial()
ser.baudrate = 115200
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.xonxoff = 0
ser.rtscts = 0
ser.timeout = 20
ser.port = "/dev/ttyUSB0"

ser.open()


converters = [
    {
        'prefix': b'0-1:24.2.1',
        'name': 'gas_m3_total',
        'method': lambda x: float(x.split(b')(')[1].split(b'*m3)\r\n')[0])
    },
    {
        'prefix': b'1-0:1.7.0',
        'name': 'kw_current',
        'method': lambda x: float(x.lstrip(b'(').rstrip(b'*kW)\r\n'))
    },
    {
        'prefix': b'1-0:1.8.2',
        'name': 'kwh_high_total',
        'method': lambda x: float(x.lstrip(b'(').rstrip(b'*kWh)\r\n'))
    },
    {
        'prefix': b'1-0:1.8.1',
        'name': 'kwh_low_total',
        'method': lambda x: float(x.lstrip(b'(').rstrip(b'*kWh)\r\n'))
    },
    {
        'prefix': b'1-0:2.7.0',
        'name': 'kw_produced',
        'method': lambda x: float(x.lstrip(b'(').rstrip(b'*kWh)\r\n'))
    },
]


def yield_data():
    stack = []
    while True:
        line = ser.readline()
        if line == SEPARATOR_LINE and not stack:
            stack.append(line)
        elif line == SEPARATOR_LINE and stack:
            yield stack
            stack = []
            time.sleep(10)
        else:
            stack.append(line)


if __name__ == '__main__':
    db.create_db()

    with open("energy.txt", "a") as output:
        for data in yield_data():
            tstamp = time.time()
            d = {'timestamp': tstamp}
            for line in data:
                try:
                    for conv in converters:
                        if line.startswith(conv['prefix']):
                            value = conv['method'](line.lstrip(conv['prefix']))
                            d[conv['name']] = value
                except (ValueError, IndexError):
                    print("Ignoring unexpected data for line", line)
                    continue

            print(d)
            output.write(json.dumps(d))
            output.write('\n')

            if len(d) != (len(converters) + 1):
                # Missing data
                continue

            db.insert_datapoint(
                d['timestamp'],
                d['kwh_high_total'],
                d['kwh_low_total'],
                d['kw_current'],
                d['gas_m3_total'],
                d['kw_produced'],
            )
