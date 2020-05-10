from config import i2c_pins, location_id
from machine import I2C, Pin
import time

OP_SINGLE_HRES1 = 0x20
OP_SINGLE_HRES2 = 0x21
OP_SINGLE_LRES = 0x23

DELAY_HMODE = 180  # 180ms in H-mode
DELAY_LMODE = 24  # 24ms in L-mode


class BH1750:

    def __init__(self, transport=None, address=0x23, mode=OP_SINGLE_HRES1):
        self.ID = 2
        self.transport = transport
        self.address = address
        self.mode = mode
        self.sensor = I2C(scl=Pin(i2c_pins['scl']),
                          sda=Pin(i2c_pins['sda']), freq=10000)
        self._setup()

    def _setup(self):
        # make sure device is in a clean state
        self.sensor.writeto(self.address, b"\x00")

    def _format(self, reading):
        return "{},{},{}".format(
            location_id,
            self.ID,
            reading
        )

    def _send(self, payload):
        # If has transnport then send
        if self.transport is None:
            print('Cannot send BH1750 reading without a defined transport')
            return

        self.transport.broadcast(payload)

    def sleep(self):
        if self.sensor is None:
            return

        self.sensor.writeto(self.address, b"\x00")

    def read(self, autosend=True, autosleep=True):
        self.sensor.writeto(self.address, b"\x01")  # power up
        self.sensor.writeto(self.address, bytes(
            [self.mode]))  # set measurement mode

        time.sleep_ms(DELAY_LMODE if self.mode ==
                      OP_SINGLE_LRES else DELAY_HMODE)

        raw = self.sensor.readfrom(self.address, 2)
        self.sensor.writeto(self.address, b"\x00")  # power down again

        raw_reading = ((raw[0] << 24) | (raw[1] << 16)) // 78642

        if autosend:
            payload = self._format(raw_reading)
            self._send(payload)

        if autosleep:
            self.sleep()

        return raw_reading
