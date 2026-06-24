from asyncio import Protocol, ReadTransport
from pynput.mouse import Controller
from typing import ClassVar


class BaseDecoder(Protocol):
    options: ClassVar[dict[str, int | str]]
    transport: ReadTransport
    mouse = Controller()
    _state = {
        'left': False,
        'right': False
    }
    _packet = bytearray()

    def connection_made(self, transport: ReadTransport):
        self.transport = transport

    def data_received(self, data):
        raise NotImplementedError

    def _debug(self):
        print('packet received', ' '.join('{:02x}'.format(c) for c in self._packet))
