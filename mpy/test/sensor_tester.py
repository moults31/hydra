# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

"""
Dummy app for running tests against sensors
"""

import time

import mpy.hal.adapter.temp_sensor
import mpy.hal.adapter.ambient_light_sensor

class Sensor_tester:
    def __init__(self, period_sec=1):
        self.temp_sensor = mpy.hal.adapter.temp_sensor.Temp_sensor()
        self.ambient_light_sensor = mpy.hal.adapter.ambient_light_sensor.Ambient_light_sensor()

        while True:
            temp = self.temp_sensor.read()
            lux = self.ambient_light_sensor.read_lux()
            print(f"{temp=}")
            print(f"{lux=}")
            time.sleep(period_sec)