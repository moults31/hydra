# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

from machine import Pin
import time

import mpy.hal.adapter.temp_sensor
import mpy.hal.adapter.ambient_light_sensor

if __name__ == '__main__':
    pin = Pin("LED", Pin.OUT)

    print("Creating temp sensor")
    temp_sensor = mpy.hal.adapter.temp_sensor.Temp_sensor()
    print("Done Creating temp sensor")

    print("Creating ambient light sensor")
    ambient_light_sensor = mpy.hal.adapter.ambient_light_sensor.Ambient_light_sensor()
    print("Done Creating ambient light sensor")

    while True:
        pin.toggle()
        temp = temp_sensor.read()
        print(f"{temp=}")
        time.sleep(1)