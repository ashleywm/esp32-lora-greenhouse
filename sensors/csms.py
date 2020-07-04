from config import csms_pins, location_id
from machine import Pin, ADC
from lib.csms import CSMS as lib
import time


class CSMS:

    def __init__(self, transport=None):
        self.ID = 4
        self.transport = transport
        self.adc = None
        self.sensor = None
        self.power = Pin(csms_pins['power'], Pin.OUT)
        self._setup()

    def _setup(self):
        self.power.value(1)
        self.adc = ADC(Pin(csms_pins['adc']))
        self.adc.atten(ADC.ATTN_11DB)
        self.sensor = lib(adc=self.adc, min_value=4095, max_value=0)

    def _format(self, reading):
        return "{},{},{:.2f}".format(
            location_id,
            self.ID,
            reading
        )

    def _send(self, payload):
        # If has transnport then send
        if self.transport is None:
            print('Cannot send CSMS reading without a defined transport')
            return

        self.transport.broadcast(payload)

    def sleep(self):
        self.power.value(0)

    def read(self, autosend=True, autosleep=True):
        raw_reading = self.sensor.read(25)

        if autosend:
            payload = self._format(raw_reading)
            self._send(payload)

        if autosleep:
            self.sleep()

        return raw_reading
