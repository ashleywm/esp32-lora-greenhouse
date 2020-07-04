lora_settings = {
    'frequency': 433E6,
    'frequency_offset': 0,
    'tx_power_level': 14,
    'signal_bandwidth': 125E3,
    'spreading_factor': 12,
    'coding_rate': 8,
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

onewire_pins = {
    'ds18b20': 25,
    'power': 26
}

csms_pins = {
    'adc': 36,
    'power': 26
}

battery_pins = {
    'adc': 39
}

bme280_settings = {
    'mode': 2
}


location_id = 1
sleep_minutes = 15
