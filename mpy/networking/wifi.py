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

"""
Establish context for wifi connection
"""
# Grab ssid and PASSWORD from user-populated secrets
SECRETS = mpy.secrets.get_secrets()
SSID = SECRETS['ssid']
PASSWORD = SECRETS['password']
WLAN = network.WLAN(network.STA_IF)
UTC_OFFSET = -7 * 60 * 60
PIN = Pin("LED", Pin.OUT)
MAC = ubinascii.hexlify(WLAN.config('mac'),':').decode()

def connect_with_retry():
    max_retries = 5
    retry = 0

    while retry < max_retries:
        try:
            connect()
            return True
        except:
            retry += 1
            disconnect()
        for i in range(30):
            PIN.toggle()
            time.sleep(0.5)
        PIN.on()

    return False

def connect():
    """
    Connect to wifi.
    """
    print(f"Trying to connect to {SSID}")

    if WLAN.isconnected():
        print("Success - Already connected")
        return

    WLAN.active(True)
    WLAN.connect(SSID, PASSWORD)
    time.sleep(5)

    # Wait for connect or fail
    max_wait = 10
    while max_wait > 0:
        print('.')
        if WLAN.status() < 0 or WLAN.status() >= 3:
            break
        max_wait -= 1
        time.sleep(1)

    # Handle connection error
    if WLAN.status() != 3:
        raise RuntimeError('network connection failed')
    else:
        print(f'Connected to {SSID}')
        for i in range(100):
            time.sleep(0.1)
            PIN.toggle()
        PIN.on()
        ntp_sync()

def disconnect():
    """
    Disconnect from wifi
    """
    # if connected:
    WLAN.disconnect()
    WLAN.active(False)

def ntp_sync():
    """
    Sync up to current time in Pacific timezone
    """
    ntptime.settime()
    actual_time = time.localtime(time.time() + UTC_OFFSET)
    print("NTP synced. Actual time:")
    print(actual_time)
