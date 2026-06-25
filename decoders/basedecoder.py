from abc import ABC, abstractmethod
from asyncio import Protocol, ReadTransport
from pynput.mouse import Controller
from typing import ClassVar, TypedDict, NotRequired, final


class SerialOptions(TypedDict):
    baudrate: int
    bytesize: int
    parity: str
    stopbits: int


class MouseState(TypedDict):
    left: bool
    right: bool
    middle: NotRequired[bool]


class BaseDecoder[T:ReadTransport](Protocol, ABC):
    options: ClassVar[SerialOptions]
    transport: T
    mouse: Controller
    _state: MouseState
    _packet: bytearray

    @final
    def connection_made(self, transport: T):
        self.transport = transport
        self.mouse = Controller()

        self._state = {
            'left': False,
            'right': False
        }
        self._packet = bytearray()

    @abstractmethod
    def data_received(self, data): ...

    def _debug(self):
        print('packet received', ' '.join('{:02x}'.format(c) for c in self._packet))
