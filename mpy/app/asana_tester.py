# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

"""
Dummy app for running tests against simple_asana.py
"""

import mpy.util.simple_asana as simple_asana

class Asana_tester:
    def __init__(self):
        sa = simple_asana.Simple_asana()