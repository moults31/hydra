# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

"""
App for tracking and reporting fermentation stats, including warnings
"""

from machine import Pin
import time

import mpy.hal.adapter.temp_sensor
import mpy.hal.adapter.ambient_light_sensor

class Fermentation_tracker:
    """
    App for tracking and reporting fermentation stats, including warnings
    """
    # Tracked variables
    temp = 0.0
    lux = 0.0

    # Warning state
    warning_state_is_active_temp = False
    warning_state_is_active_lux = False

    def __init__(self, 
        sample_period_sec=10,
        upload_period_min=10,
        warning_thresh_temp=25.0,
        warning_thresh_lux=15.0
        ):
        # Store user specified settings
        self.sample_period_sec = sample_period_sec
        self.warning_thresh_temp = warning_thresh_temp
        self.warning_thresh_lux = warning_thresh_lux

        # Grab hardware resources
        self.pin = Pin("LED", Pin.OUT)
        self.temp_sensor = mpy.hal.adapter.temp_sensor.Temp_sensor()
        self.ambient_light_sensor = mpy.hal.adapter.ambient_light_sensor.Ambient_light_sensor()

    def run_blocking(self):
        """
        Run steps on the specified sample period, forever
        """
        print("Starting fermentation tracker")
        while True:
            self.step()
            time.sleep(self.sample_period_sec)

        # Upload final log
        # TODO

    def step(self):
        """
        Toggle the LED and grab and log a sample from each sensor.
        Warn if necessary.
        """
        # Toggle LED
        self.pin.toggle()

        # Read sensors
        self.temp = self.temp_sensor.read()
        self.lux = self.ambient_light_sensor.read_lux()

        # Warn if necessary
        self.report_warning()

        # Log this sample
        # TODO log to csv with timestamps

        # Upload log if upload_period_min has elapsed
        # TODO upload log

    def report_warning(self):
        """
        Warn if the most recently read values exceed their warning thresholds.
        """
        if (self.temp > self.warning_thresh_temp) and not self.warning_state_is_active_temp:
            self.warning_state_is_active_temp = True
            print(f"WARNING: Temp {self.temp} > thresh {self.warning_thresh_temp}")
            # TODO: send warning to Asana
        else:
            # Reset warning state
            self.warning_state_is_active_temp = False

        if (self.lux > self.warning_thresh_lux) and not self.warning_state_is_active_lux:
            self.warning_state_is_active_lux = True
            print(f"WARNING: Lux {self.lux} > thresh {self.warning_thresh_lux}")
            # TODO: send warning to Asana
        else:
            # Reset warning state
            self.warning_state_is_active_lux = False