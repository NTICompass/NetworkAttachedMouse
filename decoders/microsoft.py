from decoders.basedecoder import BaseDecoder
from pynput.mouse import Button
from typing import override
import serial

start_marker = 0b01000000
left_button = 0b00100000
right_button = 0b00010000


def twos_comp(val: int, bits: int) -> int:
    """
    Compute the 2's complement of int value val

    From: https://stackoverflow.com/a/9147327
    """
    if (val & (1 << (bits - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)  # compute negative value
    return val  # return positive value as is


class Microsoft(BaseDecoder):
    """
    Microsoft serial decoders packet decoder

    With thanks to: https://roborooter.com/post/serial-mice/ and https://roborooter.com/post/serial-mouse-project/

    Also see: https://www.ardent-tool.com/mouse/How_They_Run.html
    """
    options = {
        'baudrate': 1200,
        'bytesize': serial.SEVENBITS,
        'parity': serial.PARITY_NONE,
        'stopbits': serial.STOPBITS_ONE,
    }

    @override
    def data_received(self, data):
        for byte in data:
            if (byte & start_marker) == start_marker and len(self._packet) > 0:
                self._process()
                self._packet.clear()

            self._packet.append(byte)

            if len(self._packet) == 3:
                self._process()
                self._packet.clear()

    def _process(self):
        if len(self._packet) != 3:
            return

        self._debug()

        left = (self._packet[0] & left_button) == left_button
        right = (self._packet[0] & right_button) == right_button
        #print(left, right)

        if self._state['left'] != left:
            if left:
                self.mouse.press(Button['left'])
            else:
                self.mouse.release(Button['left'])

            self._state['left'] = left

        if self._state['right'] != right:
            if right:
                self.mouse.press(Button['right'])
            else:
                self.mouse.release(Button['right'])

            self._state['right'] = right

        x = twos_comp((self._packet[0] & 0b0000011) << 6 | (self._packet[1] & 0b00111111), 8)
        y = twos_comp((self._packet[0] & 0b0001100) << 4 | (self._packet[2] & 0b00111111), 8)

        if x != 0 or y != 0:
            #print('move', x, y)
            self.mouse.move(x, y)
