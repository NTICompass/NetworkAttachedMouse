from collections.abc import Coroutine
from decoders.basedecoder import BaseDecoder
from decoders.microsoft import Microsoft
from pynput.keyboard import Listener, Key
from serial.serialutil import SerialException
from serial_asyncio import SerialTransport
from typing import Any
import argparse
import asyncio
import serial_asyncio
import sys

def init[T: BaseDecoder](factory: type[T], conn: str) -> Coroutine[Any, Any, tuple[SerialTransport, T]]:
    opts = {
        'timeout': 5
    } if conn.startswith('socket://') else factory.options

    return serial_asyncio.create_serial_connection(loop, factory, conn, **opts)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    connection = parser.add_argument_group(title='Connection Type')
    decoder_type = parser.add_mutually_exclusive_group(required=True)

    connection.add_argument('--ip', dest='ip', action='store')
    connection.add_argument('--port', dest='port', action='store')
    connection.add_argument('--com', dest='com', action='store')

    decoder_type.add_argument('--microsoft', dest='microsoft', action='store_true')
    #decoder_type.add_argument('--mouse-systems', dest='mouse_systems', action='store_true')

    args = parser.parse_args()
    conn_port: str

    if (args.ip is not None and args.com is not None) or (args.port is not None and args.com is not None):
        print('Use either ip/port or com, not both')
        sys.exit()
    elif args.ip is not None and args.port is not None:
        conn_port = f'socket://{args.ip}:{args.port}'
    elif args.com is not None:
        conn_port = str(args.com).upper()
    else:
        parser.print_help()
        sys.exit()

    loop = asyncio.new_event_loop()

    try:
        print('Connecting to serial mouse...')
        transport, protocol = loop.run_until_complete(init(Microsoft, conn_port))
    except SerialException as e:
        print(e)
        loop.stop()
    else:
        try:
            print('Connected!')
            print('Press ESC to exit')
            Listener(
                on_press=lambda key: loop.stop() if key == Key.esc else None
            ).start()
            loop.run_forever()
        except KeyboardInterrupt:
            loop.stop()
    finally:
        print('Exiting')
        loop.close()
