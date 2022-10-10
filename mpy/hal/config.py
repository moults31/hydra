# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

"""
Configuration file for HAL. User must set values that match the physical setup.
"""
import sys
IS_LINUX = (sys.platform == 'linux')

if IS_LINUX:
    # Mock configs for developing on linux
    TEMP_SENSOR = 'mock'
    AMBIENT_LIGHT_SENSOR = 'mock'

else:
    # Temperature sensor hardware config
    TEMP_SENSOR = 'tmp102'
    TEMP_SENSOR_I2C_ID = 0
    TEMP_SENSOR_I2C_SDA_PIN = 16
    TEMP_SENSOR_I2C_SCL_PIN = 17
    TEMP_SENSOR_I2C_FREQ = 400_000

    # Ambient light sensor hardware config
    AMBIENT_LIGHT_SENSOR = 'veml7700'
    AMBIENT_LIGHT_SENSOR_I2C_ID = 0
    AMBIENT_LIGHT_SENSOR_I2C_SDA_PIN = 16
    AMBIENT_LIGHT_SENSOR_I2C_SCL_PIN = 17
    AMBIENT_LIGHT_SENSOR_I2C_FREQ = 400_000