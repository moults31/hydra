# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

"""
Micropython driver for Vishay VEML7700 I2C ambient light sensor.

Some snippets adapted from https://github.com/adafruit/Adafruit_CircuitPython_VEML7700/
"""

import struct
import time

import mpy.hal.adapter.ambient_light_sensor
import mpy.hal.config as cfg

from machine import Pin, I2C

class Ambient_light_sensor_driver(mpy.hal.adapter.ambient_light_sensor.Ambient_light_sensor):
    """
    Driver for veml7700 to be used in hydra
    """
    # Device address
    DEV_ADDR = 0x10

    # Register addresses
    REG_ADDR_CONF_0 = 0x0
    REG_ADDR_WH = 0x1
    REG_ADDR_WL = 0x2
    REG_ADDR_PS = 0x3
    REG_ADDR_ALS = 0x4
    REG_ADDR_WHITE = 0x5
    REG_ADDR_ALS_INT = 0x6

    # Conf 0 register bit map
    REG_OFFSET_CONF_0_ALS_GAIN = 11
    REG_WIDTH_CONF_0_ALS_GAIN = 2
    REG_OFFSET_CONF_0_ALS_IT = 6
    REG_WIDTH_CONF_0_ALS_IT = 4
    REG_OFFSET_CONF_0_ALS_PERS = 4
    REG_WIDTH_CONF_0_ALS_PERS = 2
    REG_OFFSET_CONF_0_ALS_INT_N = 1
    REG_WIDTH_CONF_0_ALS_INT_N = 1
    REG_OFFSET_CONF_0_ALS_SD = 0
    REG_WIDTH_CONF_0_ALS_SD = 1

    # Gain options
    ALS_GAIN_1 = 0x0
    ALS_GAIN_2 = 0x1
    ALS_GAIN_1_8 = 0x2
    ALS_GAIN_1_4 = 0x3

    # Gain value integers
    gain_values = {
        ALS_GAIN_2: 2,
        ALS_GAIN_1: 1,
        ALS_GAIN_1_4: 0.25,
        ALS_GAIN_1_8: 0.125,
    }

    # Integration time options
    ALS_IT_25MS = 0xC
    ALS_IT_50MS = 0x8
    ALS_IT_100MS = 0x0
    ALS_IT_200MS = 0x1
    ALS_IT_400MS = 0x2
    ALS_IT_800MS = 0x3

    # Integration time value integers
    it_values = {
        ALS_IT_25MS: 25,
        ALS_IT_50MS: 50,
        ALS_IT_100MS: 100,
        ALS_IT_200MS: 200,
        ALS_IT_400MS: 400,
        ALS_IT_800MS: 800,
    }

    # Set defaults for gain and IT
    ALS_GAIN = ALS_GAIN_2
    ALS_IT = ALS_IT_50MS

    # I2C bus object
    _i2c = None
    
    def __init__(self, als_gain=ALS_GAIN_2, als_it=ALS_IT_50MS):
        """
        Initialize driver based on setting in config.py
        """
        # Store user-specified parameters or defaults
        self.ALS_GAIN = als_gain
        self.ALS_IT = als_it

        print("Instantiating i2c object")

        # Init i2c object, as configured in config.py
        self._i2c = I2C(
            cfg.AMBIENT_LIGHT_SENSOR_I2C_ID,
            scl=Pin(cfg.AMBIENT_LIGHT_SENSOR_I2C_SCL_PIN),
            sda=Pin(cfg.AMBIENT_LIGHT_SENSOR_I2C_SDA_PIN),
            freq=cfg.AMBIENT_LIGHT_SENSOR_I2C_FREQ)

        print("Done instantiating i2c object")

        # Build the value we will write to register CONF_0.
        # The most important thing here is writing 0 to SD, to "disable shutdown" and enable the ALS
        config_cmd_val = (
            self._apply_mask(0,             self.REG_WIDTH_CONF_0_ALS_SD,   self.REG_OFFSET_CONF_0_ALS_SD)    |
            self._apply_mask(0,             self.REG_WIDTH_CONF_0_ALS_INT_N,self.REG_OFFSET_CONF_0_ALS_INT_N) |
            self._apply_mask(0,             self.REG_WIDTH_CONF_0_ALS_PERS, self.REG_OFFSET_CONF_0_ALS_PERS)  |
            self._apply_mask(self.ALS_IT,   self.REG_WIDTH_CONF_0_ALS_IT,   self.REG_OFFSET_CONF_0_ALS_IT)    |
            self._apply_mask(self.ALS_GAIN, self.REG_WIDTH_CONF_0_ALS_GAIN, self.REG_OFFSET_CONF_0_ALS_GAIN)
        )

        print("Trying to write cfg to veml7700")

        time.sleep(10)
        # Write it.
        self._i2c.writeto_mem(self.DEV_ADDR, self.REG_ADDR_CONF_0, config_cmd_val.to_bytes(2, 'big'))
        print("Write success")

    def read_light(self):
        """
        Read raw light value from ALS
        """
        # Get raw light reading from sensor
        light_raw = self._i2c.readfrom_mem(self.DEV_ADDR, self.REG_ADDR_ALS, 2)

        # Parse bytes as little endian, 2-byte int
        light_int = struct.unpack('<H', light_raw)[0]
        return light_int

    def read_lux(self):
        """
        Read light value from ALS and convert to lux
        """
        return self._get_resolution() * self.read_light()

    def _apply_mask(self, val, width, offset):
        """
        Creates and applies mask with width width to val, then shifts left by offset bits
        """
        mask = ((1 << width) - 1)
        return (mask & val) << offset

    def _get_resolution(self):
        """
        Adapted from Adafruit driver.
        Calculates the resolution needed to convert light to lux
        """
        RES_MAX = 0.0036
        GAIN_MAX = 2
        IT_MAX = 800

        if (
            self.gain_values[self.ALS_GAIN] == GAIN_MAX
            and self.it_values[self.ALS_IT] == IT_MAX
        ):
            return RES_MAX
        else:
            return (
                RES_MAX
                * (IT_MAX / self.it_values[self.ALS_IT])
                * (GAIN_MAX / self.gain_values[self.ALS_GAIN])
            )
