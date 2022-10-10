# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

"""
App for tracking coldcrash temperature, and reporting as soon as it's complete
"""

import sys
import time

import mpy.hal.adapter.temp_sensor

IS_LINUX = (sys.platform == 'linux')

if not IS_LINUX:
    from machine import Pin

class Coldcrash_tracker:
    """
    App for tracking coldcrash temperature, and reporting as soon as it's complete
    """
    # Tracked variables. Initialize to worst case
    temp = 100.0
    target_temp = 0.0

    def __init__(self, sample_period_sec=1):
        # Store user specified settings
        self.sample_period_sec = sample_period_sec

        # Grab hardware resources
        if not IS_LINUX:
            self.pin = Pin("LED", Pin.OUT)
        self.temp_sensor = mpy.hal.adapter.temp_sensor.Temp_sensor()

    def fetch_target_temp(self):
        """
        Fetch the desired final temperature from Asana
        """
        # TODO
        pass

    def run_blocking(self):
        """
        Run steps on the specified period until we meet our target temp
        """
        print("Starting coldcrash tracker")
        while self.temp > self.target_temp:
            self.step()
            time.sleep(self.sample_period_sec)

        # Upload final log
        # TODO

    def step(self):
        """
        Toggle the LED and grab and log a sensor sample
        """
        # Toggle LED
        if not IS_LINUX:
            self.pin.toggle()

        # Read sensor
        self.temp = self.temp_sensor.read()

        # Log this sample
        # TODO log to csv with timestamps
