from config import battery_pins, location_id
from machine import Pin, ADC
import time


class Battery:

    def __init__(self, transport=None):
        self.ID = 5
        self.transport = transport
        self.adc = None
        self._setup()

    def _setup(self):
        self.adc = ADC(Pin(battery_pins['adc']))
        self.adc.atten(ADC.ATTN_11DB)

    def _format(self, reading):
        return "{},{},{:.2f}".format(
            location_id,
            self.ID,
            self._convert_to_percentage(reading)
        )

    def _send(self, payload):
        # If has transnport then send
        if self.transport is None:
            print('Cannot send battery reading without a defined transport')
            return

        self.transport.broadcast(payload)

    def _convert_to_percentage(self, reading):
        percent = int((reading - 0) * (100 - 0) /
                      (4095 - 0) + 0)

        if percent < 0:
            return 0

        if percent > 100:
            return 100

        return percent

    def read(self, autosend=True, autosleep=True):
        raw_reading = self.adc.read()

        if autosend:
            payload = self._format(raw_reading)
            self._send(payload)

        return raw_reading
