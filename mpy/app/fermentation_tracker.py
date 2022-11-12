# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

"""
App for tracking and reporting fermentation stats, including warnings
"""

import sys
import time
import io
import gc
import random
import micropython

import mpy.hal.adapter.temp_sensor
import mpy.hal.adapter.ambient_light_sensor

import mpy.util.simple_asana_handler
import mpy.util.simple_google_sheets_handler
import mpy.util.util as util

IS_LINUX = (sys.platform == 'linux')

if not IS_LINUX:
    from machine import Pin
    import mpy.networking.wifi as wifi
    # from machine import Pin, WDT

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

    # WDT offset, set to maximum for RP2040
    WDT_OFFSET_MAX = 8388

    # Save exceptions thrown from within step, so we can report them in asana
    step_exception_msg = None

    # Error log file name
    ERROR_LOG_FILE_NAME = 'ferm_track_error_log.txt'

    def __init__(self,
        mode='Primary',
        active_task_gid=None,
        active_subtask_gid=None,
        active_parent_task_name=None,
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

        # Watchdog timer with timeout tailored to fermentation tracker.
        # Sample period plus an offset to accommodate wifi connecting/disconnecting
        # wdt_timeout = (sample_period_sec * 1000) + self.WDT_OFFSET_MS
        # print(f"{wdt_timeout=}")

        # TODO: Grab timezone dynamically from secrets instead
        self.UTC_OFFSET = -8 * 60 * 60

        # Get LED pin if running on mpy hardware
        if not IS_LINUX:
            self.pin = Pin("LED", Pin.OUT)

        # Connect to wifi and init resources.
        # If anything fails, just sleep and try again.
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
                self.ambient_light_sensor = mpy.hal.adapter.ambient_light_sensor.Ambient_light_sensor()
                self.asana_handler = mpy.util.simple_asana_handler.Simple_asana_handler(active_task=active_task_gid, active_subtask=active_subtask_gid)

                active_task_description = self.asana_handler.get_active_task_description()
                self.gsheets_handler = mpy.util.simple_google_sheets_handler.Simple_google_handler(
                    new_sheet_name=active_parent_task_name,
                    existing_sheet_name=active_task_description,
                    subsheet=mode
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

        # Sensor value logging buffer
        self.buf = []

        # Init mem tracking
        gc.collect()
        self.mem_free_after_gc_prev = gc.mem_free()

    def run_blocking(self):
        """
        Run steps on the specified sample period, forever
        """
        print("Starting fermentation tracker")
        while True:
            print('\n\n')
            # Wake
            if not IS_LINUX:
                print("Waking")
                self.pin.on()
            # Do work
            try:
                self.step()
            # except BaseException as e:
            #     # Capture exception message and traceback so we can report it later, but don't re-raise.
            #     with io.StringIO() as buf:
            #         sys.print_exception(e, buf)
            #         self.step_exception_msg = buf.getvalue()
                
            #     # Print the exception
            #     print(f"\nWARNING: Ignoring exception in step. Details:")
            #     print(self.step_exception_msg)

            #     # Log the exception
            #     with open(self.ERROR_LOG_FILE_NAME, 'w') as f:
            #         f.write(self.step_exception_msg)
            # except:
            except BaseException as e:
            #     # TODO: blink pattern
            #     self.pin.on()
                print("Hit exception in step. Continuing.")
                sys.print_exception(e)

            # Sleep till next step
            if not IS_LINUX:
                self.pin.off()
            util.prepare_and_sleep(duration=self.sample_period_sec)

        # Upload final log
        # TODO Figure out condition for when fermentation tracking ends

    def step(self):
        """
        Toggle the LED and grab and log a sample from each sensor.
        Warn if necessary.
        """
        mem_free_before_gc = gc.mem_free()
        mem_info = f'free: {mem_free_before_gc}\nused: {gc.mem_alloc()}'
        print(mem_info)
        with open('mem_info_before_gc.txt', 'w') as f:
            f.write(mem_info)

        gc.collect()
        mem_free_after_gc = gc.mem_free()
        mem_info = f'free: {mem_free_after_gc}\nused: {gc.mem_alloc()}'
        print(mem_info)
        with open('mem_info_after_gc.txt', 'w') as f:
            f.write(mem_info)

        # self.wdt.feed()
        if not IS_LINUX:
            # if not wifi.connect_with_retry():
            #     # print("Couldn't connect_with_retry to wifi. Skipping this step")
            #     # return
            #     print("Couldn't connect_with_retry to wifi. Retrying once")
            #     wifi.disconnect()
            #     for _ in range(8):
            #         time.sleep(2)
            #         self.pin.toggle()
            #     self.pin.on()
            #     wifi = None
            #     wifi = wifi.Wifi()
            #     if not wifi.connect_with_retry():
            #         print("Couldn't connect_with_retry on second try. Skipping this step.")
            #         return

            wifi.disconnect()
            for i in range(8):
                time.sleep(2)
                self.pin.toggle()
            if not wifi.connect_with_retry():
                print("Couldn't connect_with_retry to wifi. Skipping this step")
                return

            # print(wifi.WLAN.ifconfig()[0])

        # Report previous exception if applicable, and clear if reporting was successful
        # if self.step_exception_msg != None:
        #     print("Reporting previous exception in asana")
            # report_success = self.asana_handler.update_exception_log(self.step_exception_msg)
            # if report_success:
            #     self.step_exception_msg = None
            # else:
            #     print("Failed to report exception, will retry next round")

        # Read sensors
        self.temp = self.temp_sensor.read()
        self.lux = self.ambient_light_sensor.read_lux()

        # Log this sample
        timestamp = time.time() + self.UTC_OFFSET
        self.buf.append([timestamp, self.temp, self.lux, mem_free_before_gc, mem_free_after_gc])

        # Warn if necessary
        isconnected = True
        if not IS_LINUX:
            isconnected = wifi.WLAN.isconnected()
        if isconnected:
            util.blink(n_periods=5, n_blinks_per_period=2, period=0.5, blink_interval=0.2)
            self.report_warning()
        else:
            util.blink(n_periods=5, n_blinks_per_period=3, period=0.5, blink_interval=0.2)

        self.n += 1
        print(f'Done {self.n} samples')

        # Upload log if our buffer is full enough
        # TODO Implement logic for making sure we don't run out of space for buffer!
        if len(self.buf) >= self.upload_buf_quota:
            if not IS_LINUX:
                isconnected = wifi.WLAN.isconnected()
            if isconnected:
                util.blink(n_periods=5, n_blinks_per_period=4, period=0.5, blink_interval=0.2)
                self.upload_and_clear_log()
            else:
                util.blink(n_periods=5, n_blinks_per_period=5, period=0.5, blink_interval=0.2)


    def report_warning(self):
        """
        Warn if the most recently read values exceed their warning thresholds.
        Will only warn once for each violation.
        TODO: Add hysteresis
        """
        # Temperature warning
        if (self.temp > self.warning_thresh_temp):
            if not self.warning_state_is_active_temp:
                warn_str = f"WARNING: Temp {self.temp} > thresh {self.warning_thresh_temp}"
                print(warn_str)

                try:
                    # Send warning to Asana
                    print("Trying to send above warning string to Asana")
                    self.asana_handler.add_comment_on_active_subtask(warn_str)
                    self.warning_state_is_active_temp = True
                    util.blink(n_periods=4, n_blinks_per_period=4, period=0.2, blink_interval=0.1)

                except:
                    # TODO: Set a flag to warn on the next wake
                    print("Failed to send warning, warning_state_is_active_temp not set.")
                    util.blink(n_periods=4, n_blinks_per_period=3, period=0.2, blink_interval=0.1)
        else:
            # Reset warning state
            self.warning_state_is_active_temp = False

        # Ambient light warning
        if (self.lux > self.warning_thresh_lux):
            if not self.warning_state_is_active_lux:
                warn_str = f"WARNING: Lux {self.lux} > thresh {self.warning_thresh_lux}"
                print(warn_str)

                try:
                    # Send warning to Asana
                    self.asana_handler.add_comment_on_active_subtask(warn_str)
                    self.warning_state_is_active_lux = True
                    util.blink(n_periods=4, n_blinks_per_period=4, period=0.2, blink_interval=0.1)
                except:
                    # TODO: Set a flag to warn on the next wake
                    print("Failed to send warning, warning_state_is_active_lux not set.")
                    util.blink(n_periods=4, n_blinks_per_period=3, period=0.2, blink_interval=0.1)
        else:
            # Reset warning state
            self.warning_state_is_active_lux = False

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
                util.blink(n_periods=4, n_blinks_per_period=6, period=0.2, blink_interval=0.1)
            else:
                print("Upload returned false. Will keep buffer intact and try again next sample.")
                util.blink(n_periods=4, n_blinks_per_period=5, period=0.2, blink_interval=0.1)
        # except:
        #     print("Upload threw exception. Will keep buffer intact and try again next sample.")
        #     util.blink(n_periods=4, n_blinks_per_period=5, period=0.2, blink_interval=0.1)

        except BaseException as e:
            #     # TODO: blink pattern
            #     self.pin.on()
                print("Hit exception in step. Continuing.")
                sys.print_exception(e)