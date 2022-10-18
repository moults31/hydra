# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

"""
App for tracking and reporting fermentation stats, including warnings
"""

import sys
import time
import picosleep

import mpy.hal.adapter.temp_sensor
import mpy.hal.adapter.ambient_light_sensor

import mpy.util.simple_asana_handler
import mpy.util.simple_google_sheets_handler

import mpy.networking.wifi as wifi

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
    n = 0

    # Warning state
    warning_state_is_active_temp = False
    warning_state_is_active_lux = False

    def __init__(self, 
        sample_period_sec=10,
        upload_buf_quota=10,
        warning_thresh_temp=25.0,
        warning_thresh_lux=15.0
        ):
        # Store user specified settings
        self.sample_period_sec = sample_period_sec
        self.upload_buf_quota = upload_buf_quota
        self.warning_thresh_temp = warning_thresh_temp
        self.warning_thresh_lux = warning_thresh_lux

        # TODO: Grab timezone dynamically from secrets instead
        self.UTC_OFFSET = -7 * 60 * 60

        # Connect to wifi
        if not IS_LINUX:
            self.pin = Pin("LED", Pin.OUT)
            self.pin.toggle()
            self.wifi_cnxn = wifi.Wifi()
            self.wifi_cnxn.connect_with_retry()
            self.pin.toggle()

        # Grab resources
        self.temp_sensor = mpy.hal.adapter.temp_sensor.Temp_sensor()
        self.ambient_light_sensor = mpy.hal.adapter.ambient_light_sensor.Ambient_light_sensor()
        self.asana_handler = mpy.util.simple_asana_handler.Simple_asana_handler()
        self.gsheets_handler = mpy.util.simple_google_sheets_handler.Simple_google_handler()

        # Sensor value logging buffer
        self.buf = []

    def run_blocking(self):
        """
        Run steps on the specified sample period, forever
        """
        print("Starting fermentation tracker")
        while True:
            # Wake
            if not IS_LINUX:
                print("Waking")
                self.pin.on()
                self.wifi_cnxn.connect_with_retry()

            # Do work
            self.step()

            # Prepare for sleep
            if not IS_LINUX:
                print("Preparing to sleep")
                self.wifi_cnxn.disconnect()
                time.sleep(15)
                self.pin.off()

            # Sleep
            print("Entering sleep")
            if IS_LINUX:
                time.sleep(self.sample_period_sec)
            else:
                picosleep.seconds(self.sample_period_sec)

        # Upload final log
        # TODO Figure out condition for when fermentation tracking ends

    def step(self):
        """
        Toggle the LED and grab and log a sample from each sensor.
        Warn if necessary.
        """
        # Read sensors
        self.temp = self.temp_sensor.read()
        self.lux = self.ambient_light_sensor.read_lux()

        # Warn if necessary
        self.report_warning()

        # Log this sample
        timestamp = time.time() + self.UTC_OFFSET
        self.buf.append([timestamp, self.temp, self.lux])

        self.n += 1
        print(f'Done {self.n} samples')

        # Upload log if our buffer is full enough
        # TODO Implement logic for making sure we don't run out of space for buffer!
        if len(self.buf) >= self.upload_buf_quota:
            self.upload_and_clear_log()


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

    def upload_and_clear_log(self):
        """
        Upload buffer log to gsheets, then clear local buffer
        """
        print("Uploading")
        self.gsheets_handler.upload_list(self.buf)
        self.buf = []
        print("Done uploading")