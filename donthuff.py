#!/usr/bin/env python3

import argparse
import logging
import serial
import io
import datetime
import json

def _init_uart(devnode):
    """
    Set up the specified UART, to read in one line at a time
    """
    ser = serial.Serial(devnode, 9600, timeout=1, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, rtscts=0)
    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser), newline=None)
    return sio

def _line_to_dict(line):
    """
    Convert a single line coming from the sensor unit into a more self-describing form
    """
    elems = line.split(' ')
    logging.debug('Got {} elements: {}'.format(len(elems), elems))
    if len(elems) < 17:
        raise Exception('Incomplete line, skipping')

    timestamp_ms = int(datetime.datetime.now().timestamp() * 1000)

    return {
        'timestamp' : timestamp_ms,
        'tempC' : float(elems[0]),
        'humidity' : float(elems[1]),
        'pm1_0': int(elems[2]),
        'pm2_5': int(elems[3]),
        'pm10_0': int(elems[4]),
        'pm1_0UsStd': int(elems[5]),
        'pm2_5UsStd': int(elems[6]),
        'pm10_0UsStd': int(elems[7]),
        'counts': {
            'gt0_3um': int(elems[8]),
            'gt0_5um': int(elems[9]),
            'gt1_0um': int(elems[10]),
            'gt2_5um': int(elems[11]),
            'gt5_0um': int(elems[12]),
            'gt10_0um': int(elems[13]),
        },
        'co2PPM': int(elems[14]),
        'hcho': float(elems[15]),
        'tvoc': float(elems[16]),
    }

def _setup_logging(verbose):
    """
    Set logging verbosity, 
    """
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

def main():
    parser = argparse.ArgumentParser(description='Log data from a wclh atmosphere monitoring device')
    parser.add_argument('-u', '--uart', required=True, dest='uart',
            help='UART to open for communicating with rommon')
    parser.add_argument('-v', '--verbose', help='verbose output', action='store_true')
    args = parser.parse_args()

    _setup_logging(args.verbose)

    logging.info('Using serial port {}'.format(args.uart))

    sio = _init_uart(args.uart)

    blanks = 0

    while True:
        # Read a single line from the UART
        line = sio.readline().strip()
        if not line:
            # Catch if we haven't seen a line in a bit; if so, throw up a warning
            blanks += 1
            if blanks >= 10 and blanks % 10 == 0:
                logging.warn('No output from device in {} seconds -- is it misbehaving?'.format(blanks))
            continue

        # We got a line
        blanks = 0

        try:
            # Try to convert the line into a dict
            result = _line_to_dict(line)
            logging.debug('{}'.format(result))
            print(json.dumps(result))
        except Exception as e:
            # If we connect while the device is operating, we can have very busted records; skip that
            logging.debug('{}'.format(e))

if __name__ == '__main__':
    main()
