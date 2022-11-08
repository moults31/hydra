# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

"""
Configuration file for HAL. User must set values that match the physical setup.
"""
import sys
IS_LINUX = (sys.platform == 'linux')

# Mapping for unique hydras to identify themeselves
HYDRA_NAME_MAP = {
    '28:cd:c1:05:07:c3': 'Derpy Hydra',
    '28:cd:c1:05:3a:d1': 'Dino Hydra',
    '28:cd:c1:05:03:d0': 'Snake Hydra',
    'unix': 'Hydra-unix',
}

if IS_LINUX:
    # Mock configs for developing on linux
    NAME = HYDRA_NAME_MAP['unix']
    TEMP_SENSOR = 'mock'
    AMBIENT_LIGHT_SENSOR = 'mock'

else:
    # Determine global unique hydra name based on mac address
    import mpy.networking.wifi as wifi
    mac = wifi.Wifi().mac
    NAME = HYDRA_NAME_MAP[mac]

    # Declare hardware configuration per physical hydra instance
    if NAME == 'Derpy Hydra':
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

    elif  NAME == 'Dino Hydra':
        # Temperature sensor hardware config
        TEMP_SENSOR = 'tmp102'
        TEMP_SENSOR_I2C_ID = 0
        TEMP_SENSOR_I2C_SDA_PIN = 16
        TEMP_SENSOR_I2C_SCL_PIN = 17
        TEMP_SENSOR_I2C_FREQ = 400_000

        # Ambient light sensor mock
        # Supply chain is no joke :(
        AMBIENT_LIGHT_SENSOR = 'mock'

    elif NAME == 'Snake Hydra':
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