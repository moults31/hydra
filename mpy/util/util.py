# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

"""
Collection of misc util functions for use from anywhere in hydra
"""

import sys
import time

IS_LINUX = (sys.platform == 'linux')

if not IS_LINUX:
    import mpy.networking.wifi as wifi

    import picosleep

    from machine import Pin, mem32
    PIN = Pin("LED", Pin.OUT)

def blink(n_periods, n_blinks_per_period, period, blink_interval):
    if not IS_LINUX:
        og = PIN.value()
        for _ in range(n_periods):
            PIN.off()
            time.sleep(period)
            for _ in range(n_blinks_per_period):
                PIN.on()
                time.sleep(blink_interval)
                PIN.off()
                time.sleep(blink_interval)
        PIN.value(og)

def prepare_and_sleep(duration):
    """
    Prepare and sleep
    """
    # Prepare for sleep
    if not IS_LINUX:
        print("Preparing to sleep")
        wifi.disconnect()
        time.sleep(15)

    # Sleep
    if IS_LINUX or (not IS_LINUX and get_usb_connected()):
        print("Entering fake sleep")
        time.sleep(duration)
    else:
        print("Entering deep sleep")
        picosleep.seconds(duration)

def get_usb_connected():
    # Check if USB peripheral is connected. Credit: https://forum.micropython.org/viewtopic.php?t=10814
    SIE_STATUS=const(0x50110000+0x50)
    CONNECTED=const(1<<16)
    SUSPENDED=const(1<<4)
    return ((mem32[SIE_STATUS] & (CONNECTED | SUSPENDED)) == CONNECTED)