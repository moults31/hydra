# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

class Ambient_light_sensor:
    """
    HAL Adapter for ambient light sensors to be used in hydra
    """
    _sensor = None

    def __init__(self):
        # _sensor = ambient_light_sensor_driver()
        print("ambient light sensor init")