from machine import Pin, I2C, deepsleep

from config import sleep_minutes

from transports.lora import Lora
from sensors.bme280 import BME280
from sensors.bh1750 import BH1750
from sensors.ds18b20 import DS18B20
from sensors.csms import CSMS
from sensors.batt import Battery

# SETUP TRANSPORT MEDIUM
lora = Lora()
lora.sleep()

# Setup and read from BME280
try:
    bme280 = BME280(transport=lora)
    bme280.read()
except:
    print('Failed to read BME280')

# Setup and read from BH1750
try:
    bh1750 = BH1750(transport=lora)
    bh1750.read()
except:
    print("Failed to read BH1750")

try:
    ds18b20 = DS18B20(transport=lora)
    ds18b20.read()
except:
    print("Failed to read DS18B20")

try:
    csms = CSMS(transport=lora)
    csms.read()
except:
    print("Failed to read CSMS")

try:
    batt = Battery(transport=lora)
    batt.read()
except:
    print("Failed to read battery")

# If sleep_minutes is set then deep sleep for X minutes
if sleep_minutes > 0:
    sleep_for = sleep_minutes * 60000
    deepsleep(sleep_for)
