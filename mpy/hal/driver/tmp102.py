# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

"""
Micropython driver for Texas Instruments tmp102 I2C temperature sensor
"""
import struct

import mpy.hal.adapter.temp_sensor
import mpy.hal.config as cfg

from machine import Pin, I2C

class Temp_sensor_driver(mpy.hal.adapter.temp_sensor.Temp_sensor):
    """
    Temperature sensor driver for tmp102.py to be used in hydra
    """
    # Device address
    DEV_ADDR = 0x48

    # Register addresses
    REG_ADDR_TEMP = 0x0
    REG_ADDR_CONF = 0x01
    REG_ADDR_T_LOW = 0x02
    REG_ADDR_T_HIGH = 0x03

    # Constants
    RESOLUTION = 0.0625
    MASK = 0xFFF0
    BIT_OFFSET = 4

    # I2C bus object
    _i2c = None

    def __init__(self):
        """
        Initialize driver based on setting in config.py
        """
        # Init i2c object, as configured in config.py
        self._i2c = I2C(
            cfg.TEMP_SENSOR_I2C_ID,
            scl=Pin(cfg.TEMP_SENSOR_I2C_SCL_PIN),
            sda=Pin(cfg.TEMP_SENSOR_I2C_SDA_PIN),
            freq=cfg.TEMP_SENSOR_I2C_FREQ)

    def read(self):
        """
        Read temperature sensor and convert to degrees celsius
        NB: Does not handle negative numbers, refer to datasheet if needed
        """
        # Get raw temp from sensor
        temp_raw = self._i2c.readfrom_mem(self.DEV_ADDR, self.REG_ADDR_TEMP, 2)

        # Parse bytes as big endian, 2-byte int
        temp_int = struct.unpack('>H', temp_raw)[0]

        # Chop off the least significant nibble, and multiply by resolution to get final temp
        temp_float = (temp_int >> self.BIT_OFFSET) * self.RESOLUTION
        return temp_float
