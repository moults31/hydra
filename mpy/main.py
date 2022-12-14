# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

import sys
import os
import micropython

import mpy.app.fermentation_tracker as fermentation_tracker
import mpy.app.coldcrash_tracker as coldcrash_tracker

import mpy.util.simple_asana_handler as asana_handler
import mpy.util.util as util


import mpy.test.asana_tester as asana_tester
import mpy.test.google_sheets_tester as google_sheets_tester
import mpy.test.sensor_tester as sensor_tester

IS_LINUX = (sys.platform == 'linux')

if not IS_LINUX:
    import mpy.networking.wifi as wifi

    from machine import Pin
    pin = Pin("LED", Pin.OUT)


def main():
    print(micropython.mem_info())

    FORCE_APP = False
    if FORCE_APP:
        pass
        # app = 'fermentation_tracker'
        # app = 'coldcrash_tracker'
        # app = 'asana_tester'
        app = 'google_sheets_tester'
        # app = 'sensor_tester'
        mode = None
        subtask_gid = None
        task_name = None
    else:
        backoff_duration_min = 1
        while True:
            try:
                if not IS_LINUX:
                    wifi.connect_with_retry()
                print("Trying to decide on app...")
                app, mode, subtask_gid, task_gid, task_name = decide_on_app()
                print("Breaking out from decision loop")
                break

            except ValueError as e:
                print("Error deciding on app. Details:")
                print(e)
                print(f"Sleeping for {backoff_duration_min} minutes before retrying")
                util.prepare_and_sleep(backoff_duration_min)
                # Exponentially increase backoff duration
                backoff_duration_min *= 2

    print("Starting", app)

    if app == 'fermentation_tracker':
        ft = fermentation_tracker.Fermentation_tracker(
            mode=mode,
            active_task_gid=task_gid,
            active_subtask_gid=subtask_gid,
            active_parent_task_name=task_name,
            warning_thresh_lux=50.0,
            warning_thresh_temp=26.0,
            sample_period_sec=3000,
            upload_buf_quota=1
        )
        ft.run_blocking()

    elif app == 'coldcrash_tracker':
        ct = coldcrash_tracker.Coldcrash_tracker(
            active_task_gid=task_gid,
            active_subtask_gid=subtask_gid,
            active_parent_task_name=task_name,
            sample_period_sec=1,
            target_temp=20
        )
        ct.run_blocking()

    elif app == 'asana_tester':
        at = asana_tester.Asana_tester()

    elif app == 'google_sheets_tester':
        gst = google_sheets_tester.Google_sheets_tester()

    elif app == 'sensor_tester':
        at = sensor_tester.Sensor_tester()

    else:
        raise Exception("No app selected!")

def decide_on_app():
    asana = asana_handler.Simple_asana_handler()
    r = asana.decide_on_app()
    return r

if __name__ == '__main__':
    """
    Main entry point to micropython program.
    """
    main()
