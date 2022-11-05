# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

"""
Dummy app for running tests against watchdog timer (WDT)
"""
import sys
import time

from machine import WDT, Pin

class WDT_tester:
    def __init__(self, timeout=2000):
        self.pin = Pin("LED", Pin.OUT)

        # Enable wdt with specified timeout (default 2sec)
        self.timeout = timeout
        self.wdt = WDT(timeout=timeout)

        # self.test_feed()
        self.test_never_feed()

    def test_feed(self):
        # Turn LED on. Test is successful if it stays on forever.
        self.pin.on()
        while True:
            self.wdt.feed()
            time.sleep(self.timeout / (2000))

    def test_never_feed(self):
        # Turn LED on. Test is successful if user sees it turn
        # off periodically due to WDT system reset.
        # (or turn off entirely if auto_run not enabled)
        while True:
            pass