# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

"""
Dummy app for running tests against simple_asana.py
"""
import sys

import mpy.util.simple_asana_handler as simple_asana_handler

IS_LINUX = (sys.platform == 'linux')

if not IS_LINUX:
    from machine import Pin
    import mpy.networking.wifi as wifi

class Asana_tester:
    def __init__(self):
        # Connect to wifi
        if not IS_LINUX:
            self.pin = Pin("LED", Pin.OUT)
            self.pin.toggle()
            self.wifi_cnxn = wifi.Wifi()
            self.wifi_cnxn.connect()
            self.pin.toggle()

        asana = simple_asana_handler.Simple_asana_handler()

        # Arbitrary task description for testing
        desc = "Ahoy from Micropython!"
        r = asana.update_active_task_description(desc=desc)
        print(r)

        # Arbitrary comment text for testing
        comment_text = "I DRAW"
        r = asana.add_comment_on_active_task(text=comment_text, is_pinned=True)
        print(r)

        assigned_task = asana.find_assigned_subtask_in_section('In Primary')
        print(assigned_task)