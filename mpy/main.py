# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

import sys
import micropython

import mpy.app.fermentation_tracker as fermentation_tracker
import mpy.app.coldcrash_tracker as coldcrash_tracker

import mpy.test.asana_tester as asana_tester
import mpy.test.google_sheets_tester as google_sheets_tester
import mpy.test.sensor_tester as sensor_tester

IS_LINUX = (sys.platform == 'linux')

if not IS_LINUX:
    from machine import Pin
    pin = Pin("LED", Pin.OUT)


def main():
    print(micropython.mem_info())

    # TODO: Read switch or something to decide which app to run.
    # For now hardcode it.
    app = 'fermentation_tracker'
    # app = 'coldcrash_tracker'
    # app = 'asana_tester'
    # app = 'google_sheets_tester'
    # app = 'sensor_tester'

    print("Starting ", app)

    if app == 'fermentation_tracker':
        ft = fermentation_tracker.Fermentation_tracker(
            warning_thresh_lux=50.0,
            warning_thresh_temp=26.0,
            sample_period_sec=180,
            upload_buf_quota=2
        )
        ft.run_blocking()
    elif app == 'coldcrash_tracker':
        ct = coldcrash_tracker.Coldcrash_tracker()
        ct.run_blocking()
    elif app == 'asana_tester':
        at = asana_tester.Asana_tester()
    elif app == 'google_sheets_tester':
        gst = google_sheets_tester.Google_sheets_tester()
    elif app == 'sensor_tester':
        at = sensor_tester.Sensor_tester()
    else:
        raise Exception("No app selected!")

if __name__ == '__main__':
    """
    Main entry point to micropython program.
    """
    main()
