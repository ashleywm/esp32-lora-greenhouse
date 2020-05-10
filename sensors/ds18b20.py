from config import onewire_pins, location_id
from machine import Pin
import onewire
import ds18x20
import time


class DS18B20:

    def __init__(self, transport=None):
        self.ID = 3
        self.transport = transport
        self.ow = None
        self.sensor = None
        self._setup()

    def _setup(self):
        self.ow = onewire.OneWire(Pin(onewire_pins['ds18b20']))
        self.sensor = ds18x20.DS18X20(self.ow)

    def _format(self, reading):
        return "{},{},{:.2f}".format(
            location_id,
            self.ID,
            reading
        )

    def _send(self, payload):
        # If has transnport then send
        if self.transport is None:
            print('Cannot send DS18B20 reading without a defined transport')
            return

        self.transport.broadcast(payload)

    def read(self, autosend=True):

        roms = self.sensor.scan()
        self.sensor.convert_temp()
        time.sleep_ms(750)
        raw_reading = self.sensor.read_temp(roms[0])

        print(raw_reading)

        if autosend:
            payload = self._format(raw_reading)
            self._send(payload)

        return raw_reading
