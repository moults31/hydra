# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

"""
Dummy app for running tests against simple_google_sheets_handler
"""

import mpy.util.simple_google_sheets_handler as simple_google_sheets_handler

class Google_sheets_tester:
    def __init__(self):
        google_sheets = simple_google_sheets_handler.Simple_google_handler()
        google_sheets.get_jwt()

        # Arbitrary list of values
        values = [
            ['Landeskog', 'MacKinnon', 'Rantanen'],
            ['Nichushkin', 'Kadri', 'Lehkonen'],
            ['Newhook', 'Compher', 'Burakovsky'],
            ['Cogliano', 'Helm', "O'Connor"]
        ]
        google_sheets.upload_list(values)