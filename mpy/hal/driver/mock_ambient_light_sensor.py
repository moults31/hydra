# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

"""
Software mock for adapter/ambient_light_sensor.py
"""

import random

import mpy.hal.adapter.ambient_light_sensor
import mpy.hal.config as cfg

class Ambient_light_sensor_driver(mpy.hal.adapter.ambient_light_sensor.Ambient_light_sensor):
    def __init__(self):
        pass

    def read_light(self):
        """
        Mock raw light value from ALS
        """

        return 200.0 + random.randrange(100)

    def read_lux(self):
        """
        Mock converted lux value
        """
        return 0.0 + random.randrange(16)
