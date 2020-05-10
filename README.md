# ESP32 LoRa Greenhouse

This project uses a solar powered ESP32 running MicroPython to read sensors installed in a Greenhouse and then transmit the readings using LoRa. The [LoRa MQTT Gateway](https://github.com/ashleywm/esp32-lora-mqtt-gateway/) will then parse the incoming message, map it to a JSON schema and publish it to the MQTT Broker.

## Sensors Implemented

- BME280 - For greenhouse temperature, pressure and relative humidity
- BH1750 GY-30 - Grennhouse luminosity
- DS18B20 - Soil temperature
- CSMS (Capcitive Soil Moisture Sensor) - Greenhouse soil moisture
