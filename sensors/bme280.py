from config import i2c_pins, bme280_settings, location_id
from machine import I2C, Pin
from lib.bme280 import BME280 as lib


class BME280:

    def __init__(self, transport=None):
        self.ID = 1
        self.transport = transport
        self.i2c = I2C(scl=Pin(i2c_pins['scl']),
                       sda=Pin(i2c_pins['sda']), freq=10000)
        self.sensor = None
        self._setup()

    def _setup(self):
        self.sensor = lib(mode=bme280_settings['mode'], i2c=self.i2c)

    def _format(self, reading):
        return "{},{},{},{},{}".format(
            location_id,
            self.ID,
            reading['temperature'],
            reading['pressure'],
            reading['humidity']
        )

    def _send(self, payload):
        # If has transnport then send
        if self.transport is None:
            print('Cannot send BME280 reading without a defined transport')
            return

        self.transport.broadcast(payload)

    def sleep(self):
        if self.sensor is None:
            return

        # self.sensor.sleep()

    def read(self, autosend=True, autosleep=True):
        raw_reading = self.sensor.values

        if autosend:
            payload = self._format(raw_reading)
            self._send(payload)

        if autosleep:
            self.sleep()

        return raw_reading
