# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

"""
App for tracking coldcrash temperature, and reporting as soon as it's complete
"""

import sys
import time
import gc

import mpy.hal.adapter.temp_sensor

import mpy.util.simple_asana_handler
import mpy.util.simple_google_sheets_handler
import mpy.util.util as util

IS_LINUX = (sys.platform == 'linux')

if not IS_LINUX:
    from machine import Pin
    import mpy.networking.wifi as wifi

class Coldcrash_tracker:
    """
    App for tracking coldcrash temperature, and reporting as soon as it's complete
    """
    # Tracked variables. Initialize to below start thresh
    temp = 0.0
    target_temp = 0.0
    start_thresh_temp = 40
    start_thresh_met = False

    def __init__(self,
        active_task_gid=None,
        active_subtask_gid=None,
        active_parent_task_name=None,
        sample_period_sec=1,
        target_temp=30
        ):
        # Store user specified settings
        self.sample_period_sec = sample_period_sec
        self.target_temp = target_temp

        # Sensor value logging buffer
        self.buf = []

        # TODO: Grab timezone dynamically from secrets instead
        self.UTC_OFFSET = -8 * 60 * 60

        # Grab resources
        if not IS_LINUX:
            self.pin = Pin("LED", Pin.OUT)
        n_init_retries = 0
        while True:
            print("Trying to connect and init")
            try:
                # Connect to wifi if running on mpy hardware, and turn on LED to indicate trying to connect
                if not IS_LINUX:
                    self.pin.on()
                    wifi.connect_with_retry()

                # Grab resources
                self.temp_sensor = mpy.hal.adapter.temp_sensor.Temp_sensor()
                self.asana_handler = mpy.util.simple_asana_handler.Simple_asana_handler(active_task=active_task_gid, active_subtask=active_subtask_gid)

                active_task_description = self.asana_handler.get_active_task_description()
                self.gsheets_handler = mpy.util.simple_google_sheets_handler.Simple_google_handler(
                    new_sheet_name=active_parent_task_name,
                    existing_sheet_name=active_task_description,
                    subsheet='Coldcrash'
                )

                # Update the active Asana task with the new Google Sheet URL
                self.asana_handler.update_active_task_description(
                    self.gsheets_handler.get_active_sheet_url()
                )

                # Turn off LED to indicate connection and init success
                if not IS_LINUX:
                    self.pin.off()
                break

            except:
                n_init_retries += 1
                print(f"Init retry #{n_init_retries}")
                print("Sleeping for 1 sample period before next retry")
                util.prepare_and_sleep(duration=self.sample_period_sec)

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
        while (self.temp > self.target_temp) or not self.start_thresh_met:
            self.step()
            time.sleep(self.sample_period_sec)

        print("All done! Target temperature met. Exiting.")

    def step(self):
        """
        Toggle the LED and grab and log a sensor sample
        """
        # Toggle LED
        if not IS_LINUX:
            self.pin.toggle()

        # Force garbage collection just in case
        gc.collect()

        # Read sensor
        self.temp = self.temp_sensor.read()

        # Flip start_thresh_met the first time we exceed it
        if not self.start_thresh_met:
            if self.temp > self.start_thresh_temp:
                self.start_thresh_met = True

        # Log this sample
        timestamp = time.time() + self.UTC_OFFSET
        self.buf.append([timestamp, self.temp])

        # Upload it
        self.upload_and_clear_log()

    def upload_and_clear_log(self):
        """
        Upload buffer log to gsheets, then clear local buffer
        """
        print("Uploading")
        try:

            # a = random.randint(0,1)
            # if a == 1:
            #     raise RuntimeError("Is this your card?")

            upload_success = self.gsheets_handler.upload_list(self.buf)
            # upload_success = self.asana_handler.update_exception_log(str(self.buf[0]))
            # if upload_success:
            if upload_success != False:
                self.buf = []
                print("Done uploading")
            else:
                print("Upload returned false. Will keep buffer intact and try again next sample.")
        # except:
        #     print("Upload threw exception. Will keep buffer intact and try again next sample.")
        #     util.blink(n_periods=4, n_blinks_per_period=5, period=0.2, blink_interval=0.1)

        except BaseException as e:
            #     # TODO: blink pattern
            #     self.pin.on()
                print("Hit exception in step. Continuing.")
                sys.print_exception(e)