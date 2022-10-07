# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

# import ..config

# if config.TEMP_SENSOR == 'tmp102':
#     import ..driver.tmp102 as temp_sensor_driver
# else:
#     raise Exception("No valid temperature sensor selected")

class Temp_sensor:
    """
    HAL Adapter for temperature sensors to be used in hydra
    """
    _sensor = None

    def __init__(self):
        # _sensor = temp_sensor_driver()
        print("temp sensor init")