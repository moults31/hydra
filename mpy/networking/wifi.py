# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

"""
File containing methods for handling wifi connection.
All methods are idempotent.

Depends on secrets.py being properly populated
"""

import time
import ntptime
import network
import ubinascii

from machine import Pin

import mpy.secrets

class Wifi:
    def __init__(self):
        """
        Establish context for wifi connection
        """
        # Grab ssid and password from user-populated secrets
        self.secrets = mpy.secrets.get_secrets()
        self.ssid = self.secrets['ssid']
        self.password = self.secrets['password']
        self.wlan = network.WLAN(network.STA_IF)
        self.UTC_OFFSET = -7 * 60 * 60
        self.pin = Pin("LED", Pin.OUT)
        self.mac = ubinascii.hexlify(self.wlan.config('mac'),':').decode()
        # self.connected = False

    def connect_with_retry(self):
        max_retries = 5
        retry = 0

        while retry < max_retries:
            try:
                self.connect()
                return True
            except:
                retry += 1
                self.disconnect()
            for i in range(30):
                self.pin.toggle()
                time.sleep(0.5)
            self.pin.on()

        return False

    def connect(self):
        """
        Connect to wifi.
        """
        # if self.connected:
        #     print(f"Already connected to {self.ssid}")
        #     return

        print(f"Trying to connect to {self.ssid}")

        if self.wlan.isconnected():
            return

        self.wlan.active(True)
        self.wlan.connect(self.ssid, self.password)
        time.sleep(5)

        # Wait for connect or fail
        max_wait = 10
        while max_wait > 0:
            print('.')
            if self.wlan.status() < 0 or self.wlan.status() >= 3:
                break
            max_wait -= 1
            # self.pin.toggle()
            time.sleep(1)

        # Handle connection error
        if self.wlan.status() != 3:
            raise RuntimeError('network connection failed')
        else:
            print(f'Connected to {self.ssid}')
            # self.connected = True
            for i in range(100):
                time.sleep(0.1)
                self.pin.toggle()
            self.pin.on()
            self.ntp_sync()

    def disconnect(self):
        """
        Disconnect from wifi
        """
        # if self.connected:
        self.wlan.disconnect()
        self.wlan.active(False)
            # self.connected = False

    def ntp_sync(self):
        """
        Sync up to current time in Pacific timezone
        """
        ntptime.settime()
        actual_time = time.localtime(time.time() + self.UTC_OFFSET)
        print("NTP synced. Actual time:")
        print(actual_time)
