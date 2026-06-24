from asyncio import Protocol
from collections.abc import Coroutine
from pynput.keyboard import Listener, Key
from serial.serialutil import SerialException
from serial_asyncio import SerialTransport
from decoders.microsoft import Microsoft
from typing import Any
import asyncio
import serial_asyncio

def init[T:Protocol](factory: type[T]) -> Coroutine[Any, Any, tuple[SerialTransport, T]]:
    # 'COM7', **opts
    # 'socket://192.168.1.123:3008'
    return serial_asyncio.create_serial_connection(loop, factory, 'socket://192.168.1.123:3008', timeout=5, **factory.options)

if __name__ == '__main__':
    loop = asyncio.new_event_loop()

    try:
        print('Connecting to serial mouse...')
        transport, protocol = loop.run_until_complete(init(Microsoft))
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
