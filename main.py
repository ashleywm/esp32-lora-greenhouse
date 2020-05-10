from machine import Pin, I2C, deepsleep

from config import sleep_minutes

from transports.lora import Lora
from sensors.bme280 import BME280
from sensors.bh1750 import BH1750
from sensors.ds18b20 import DS18B20
from sensors.csms import CSMS

# SETUP TRANSPORT MEDIUM
lora = Lora()
lora.sleep()

# Setup and read from BME280
bme280 = BME280(transport=lora)
bme280.read()

# Setup and read from BH1750
bh1750 = BH1750(transport=lora)
bh1750.read()

ds18b20 = DS18B20(transport=lora)
ds18b20.read()

csms = CSMS(transport=lora)
csms.read()


# If sleep_minutes is set then deep sleep for X minutes
if sleep_minutes > 0:
    sleep_for = sleep_minutes * 60000
    deepsleep(sleep_for)
