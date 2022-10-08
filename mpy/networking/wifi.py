# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

"""
File containing methods for connecting to wifi.

Depends on secrets.py being properly populated
"""

import time
import network

import mpy.secrets

class Wifi:
    secrets = mpy.secrets.get_secrets()

    ssid = secrets['ssid']
    password = secrets['password']

    def __init__(self):
        """
        Connect to wifi. Raise RuntimeError on failure to connect.
        """
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(self.ssid, self.password)

        # Wait for connect or fail
        max_wait = 10
        while max_wait > 0:
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            max_wait -= 1
            time.sleep(1)

        # Handle connection error
        if wlan.status() != 3:
            raise RuntimeError('network connection failed')
        else:
            print(f'Connected to {self.ssid}')
            status = wlan.ifconfig()