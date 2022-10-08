# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

import mpy.hal.config

class Ambient_light_sensor:
    """
    HAL Adapter for ambient light sensors to be used in hydra
    """
    _sensor_driver = None

    def __init__(self):
        """
        Initialize with driver chosen in config.py
        """
        if mpy.hal.config.AMBIENT_LIGHT_SENSOR == 'veml7700':
            self._sensor_driver = veml7700.Ambient_light_sensor_driver()
        else:
            raise Exception("No valid ambient light sensor selected")

    def read_light(self):
        """
        Read light. Driver is responsible for conversion.
        """
        if hasattr(self._sensor_driver, 'read_light'):
            return self._sensor_driver.read_light()
        else:
            raise NotImplementedError(f"This method must be implemented by driver for {mpy.hal.config.AMBIENT_LIGHT_SENSOR}")

    def read_lux(self):
        """
        Read lux. Driver is responsible for conversion.
        """
        if hasattr(self._sensor_driver, 'read_lux'):
            return self._sensor_driver.read_lux()
        else:
            raise NotImplementedError(f"This method must be implemented by driver for {mpy.hal.config.AMBIENT_LIGHT_SENSOR}")

# Import drivers. Must be done after class def so that they can inherit from Ambient_light_sensor.
import mpy.hal.driver.veml7700 as veml7700