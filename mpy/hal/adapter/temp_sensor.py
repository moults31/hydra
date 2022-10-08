# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

import mpy.hal.config

class Temp_sensor:
    """
    HAL Adapter for temperature sensors to be used in hydra
    """
    # Driver object, populated on init
    _sensor_driver = None

    def __init__(self):
        """
        Initialize with driver chosen in config.py
        """
        if mpy.hal.config.TEMP_SENSOR == 'tmp102':
            self._sensor_driver = tmp102.Temp_sensor_driver()
        else:
            raise Exception("No valid temperature sensor selected")

    def read(self):
        """
        Read temperature in degrees Celsius. Driver is responsible for conversion.
        """
        if hasattr(self._sensor_driver, 'read'):
            return self._sensor_driver.read()
        else:
            raise NotImplementedError(f"This method must be implemented by driver for {mpy.hal.config.TEMP_SENSOR}")

# Import drivers. Must be done after class def so that they can inherit from Temp_sensor.
import mpy.hal.driver.tmp102 as tmp102
