# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

"""
Dummy app for running tests against nrf8001.py
"""

import mpy.hal.driver.nrf8001 as bt

class Bluetooth_tester:
    def __init__(self):
        bt.init()
