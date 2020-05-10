from config import lora_pins, lora_settings
from machine import Pin, SPI
from lib.sx127x import SX127x


class Lora:

    def __init__(self):
        self.spi = SPI(
            baudrate=10000000, polarity=0, phase=0,
            bits=8, firstbit=SPI.MSB,
            sck=Pin(lora_pins['sck'], Pin.OUT, Pin.PULL_DOWN),
            mosi=Pin(lora_pins['mosi'], Pin.OUT, Pin.PULL_UP),
            miso=Pin(lora_pins['miso'], Pin.IN, Pin.PULL_UP),
        )
        self.lora = None
        self._setup()

    def _setup(self):
        self.lora = SX127x(self.spi, pins=lora_pins, parameters=lora_settings)

    def sleep(self):
        if self.lora is None:
            return

        self.lora.sleep()

    def broadcast(self, payload):
        if self.lora is None:
            return

        print('Sending Payload: {}'.format(payload))
        self.lora.println(payload)
        self.sleep()
