# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

"""
Dummy app for running tests against sensors
"""

import time

import mpy.hal.adapter.temp_sensor
import mpy.hal.adapter.ambient_light_sensor

from machine import Pin

class Sensor_tester:
    def __init__(self, period_sec=1):
        self.pin = Pin("LED", Pin.OUT)
        self.pin.toggle()
        print("Initing temp sensor")
        self.temp_sensor = mpy.hal.adapter.temp_sensor.Temp_sensor()
        print("Initing light sensor")
        self.ambient_light_sensor = mpy.hal.adapter.ambient_light_sensor.Ambient_light_sensor()
        print("Done init")

        while True:
            self.pin.toggle()

            print("Trying temp read")
            temp = self.temp_sensor.read()
            print("Done temp read")
            print(f"{temp=}")

            print("Trying light read")
            lux = self.ambient_light_sensor.read_lux()
            print("Done light read")
            print(f"{lux=}")
            print('')

            time.sleep(period_sec)