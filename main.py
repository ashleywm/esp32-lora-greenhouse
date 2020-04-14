from machine import Pin, SPI, I2C, deepsleep

from lib.sx127x import SX127x
from lib import BME280

"""
SETTINGS 
"""
sleep_minutes = 15

lora_settings = {
    'frequency': 433E6,
    'frequency_offset': 0,
    'tx_power_level': 14,
    'signal_bandwidth': 125E3,
    'spreading_factor': 9,
    'coding_rate': 5,
    'preamble_length': 8,
    'implicitHeader': False,
    'sync_word': 0x12,
    'enable_CRC': False,
    'invert_IQ': False,
    'debug': False,
}

lora_pins = {
    'dio_0': 2,
    'ss': 5,
    'reset': 14,
    'sck': 18,
    'miso': 19,
    'mosi': 23,
}

i2c_pins = {
    'scl': 22,
    'sda': 21
} 

power_pins = {
    'lora': 27,
    'bme280': 26,
    'led': 2
}

# Enable onboard status LED

status_led = Pin(power_pins['led'], Pin.OUT)
status_led.on()

"""
START READING SENSORS
"""

# Setup BME280 pins and power on
bme280_power = Pin(power_pins['bme280'], Pin.OUT)
bme280_power.on()

i2c = I2C(scl=Pin(i2c_pins['scl']), sda=Pin(i2c_pins['sda']), freq=10000)

bme280 = BME280.BME280(mode=1, i2c=i2c)

# Set reading from sensor
bme280_reading = {
    'temperature': bme280.temperature,
    'pressure': bme280.pressure,
    'humidity': bme280.humidity
}

# Power off the sensor to save power
bme280_power.off()


"""
START TRANSMISSION
Transmit sensor readings over LoRa to MQTT-Gateway 
"""

# Power on module
lora_power = Pin(power_pins['lora'], Pin.OUT)
lora_power.on()

# Setup pins
lora_spi = SPI(
    baudrate=10000000, polarity=0, phase=0,
    bits=8, firstbit=SPI.MSB,
    sck=Pin(lora_pins['sck'], Pin.OUT, Pin.PULL_DOWN),
    mosi=Pin(lora_pins['mosi'], Pin.OUT, Pin.PULL_UP),
    miso=Pin(lora_pins['miso'], Pin.IN, Pin.PULL_UP),
)

lora = SX127x(lora_spi, pins=lora_pins, parameters=lora_settings)

# Format payload
payload = "0,{},{},{}".format(bme280_reading['temperature'], bme280_reading['pressure'], bme280_reading['humidity'])

print('Sending Payload: {}'.format(payload))

# Transmit
lora.println(payload)

# Power off the module
lora_power.off()

# Turn off LED, if LED stays lit then something went wrong
status_led.off()

# If a sleep time has been set then it's time to sleep
if sleep_minutes > 0:
    sleep_for = sleep_minutes * 60000
    deepsleep(sleep_for)