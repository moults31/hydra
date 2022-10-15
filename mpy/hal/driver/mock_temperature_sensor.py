# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

"""
Software mock for adapter/temperature_sensor.py
"""

import random

import mpy.hal.adapter.temp_sensor
import mpy.hal.config as cfg

class Temperature_sensor_driver(mpy.hal.adapter.temp_sensor.Temp_sensor):
    def __init__(self):
        pass

    def read(self):
        """
        Mock temperature value
        """
        return 10.0 + random.randrange(17)

