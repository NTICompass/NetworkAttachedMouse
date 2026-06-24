from collections.abc import Coroutine
from typing import Any
from serial_asyncio import SerialTransport
from sermouse.decoder import Decoder
import asyncio
import serial
import serial_asyncio
from asyncio import Protocol

def init[T:Protocol](factory: type[T]) -> Coroutine[Any, Any, tuple[SerialTransport, T]]:
    return serial_asyncio.create_serial_connection(
        loop,
        factory,
        'COM7',
        baudrate=1200,
        bytesize=serial.SEVENBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
    )

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    transport, protocol = loop.run_until_complete(init(Decoder))
    loop.run_forever()
    loop.close()
