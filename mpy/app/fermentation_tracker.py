# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

"""
App for tracking and reporting fermentation stats, including warnings
"""

import sys
import time

import mpy.hal.adapter.temp_sensor
import mpy.hal.adapter.ambient_light_sensor

import mpy.util.simple_asana_handler

IS_LINUX = (sys.platform == 'linux')

if not IS_LINUX:
    from machine import Pin

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

        # Grab resources
        if not IS_LINUX:
            self.pin = Pin("LED", Pin.OUT)
        self.temp_sensor = mpy.hal.adapter.temp_sensor.Temp_sensor()
        self.ambient_light_sensor = mpy.hal.adapter.ambient_light_sensor.Ambient_light_sensor()
        self.asana_handler = mpy.util.simple_asana_handler.Simple_asana_handler()

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
        if not IS_LINUX:
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
        Will only warn once for each violation.
        TODO: Add hysteresis
        """
        # Temperature warning
        if (self.temp > self.warning_thresh_temp):
            if not self.warning_state_is_active_temp:
                self.warning_state_is_active_temp = True
                warn_str = f"WARNING: Temp {self.temp} > thresh {self.warning_thresh_temp}"
                print(warn_str)

                # Send warning to Asana
                self.asana_handler.add_comment_on_active_task(warn_str)
        else:
            # Reset warning state
            self.warning_state_is_active_temp = False

        # Ambient light warning
        if (self.lux > self.warning_thresh_lux):
            if not self.warning_state_is_active_lux:
                self.warning_state_is_active_lux = True
                warn_str = f"WARNING: Lux {self.lux} > thresh {self.warning_thresh_lux}"
                print(warn_str)

                # Send warning to Asana
                self.asana_handler.add_comment_on_active_task(warn_str)
        else:
            # Reset warning state
            self.warning_state_is_active_lux = False