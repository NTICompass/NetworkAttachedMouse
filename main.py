from collections.abc import Coroutine
from typing import Any
from serial_asyncio import SerialTransport
from sermouse.decoder import Decoder
import asyncio
import serial
import serial_asyncio
from asyncio import Protocol

def init[T:Protocol](factory: type[T]) -> Coroutine[Any, Any, tuple[SerialTransport, T]]:
    opts = {
        'baudrate':1200,
        'bytesize':serial.SEVENBITS,
        'parity':serial.PARITY_NONE,
        'stopbits': serial.STOPBITS_ONE,
    }

    # 'COM7', **opts
    return serial_asyncio.create_serial_connection(loop, factory, 'socket://192.168.1.123:3008')

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    transport, protocol = loop.run_until_complete(init(Decoder))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('Exit')
    finally:
        loop.close()
