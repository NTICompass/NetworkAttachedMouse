from sermouse.decoder import Decoder
import asyncio
import serial
import serial_asyncio

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    port = serial_asyncio.create_serial_connection(
        loop,
        Decoder,
        'COM7',
        baudrate=1200,
        bytesize=serial.SEVENBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
    )

    transport, protocol = loop.run_until_complete(port)
    loop.run_forever()
    loop.close()
