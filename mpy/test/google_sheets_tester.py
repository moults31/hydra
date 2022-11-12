# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

"""
Dummy app for running tests against simple_google_sheets_handler
"""

import sys

import mpy.util.simple_google_sheets_handler as simple_google_sheets_handler
import mpy.secrets

IS_LINUX = (sys.platform == 'linux')

if not IS_LINUX:
    import mpy.networking.wifi as wifi
    from machine import Pin

class Google_sheets_tester:
    def __init__(self):
        # Connect to wifi
        if not IS_LINUX:
            self.pin = Pin("LED", Pin.OUT)
            self.pin.toggle()
            wifi.connect_with_retry()
            self.pin.toggle()

        self.secrets = mpy.secrets.get_secrets()
        self.google_sheets = simple_google_sheets_handler.Simple_google_handler()
        self.google_sheets.get_jwt()

        self.test_upload_list()

    def test_upload_list(self):
        # Arbitrary list of values
        values = [
            ['Landeskog', 'MacKinnon', 'Rantanen'],
            ['Nichushkin', 'Kadri', 'Lehkonen'],
            ['Newhook', 'Compher', 'Burakovsky'],
            ['Cogliano', 'Helm', "O'Connor"]
        ]
        self.google_sheets.upload_list(values)

    def test_create_spreadsheet(self):
        sheetid = self.google_sheets.create_spreadsheet('Test_sheet')
        return

    def test_duplicate_spreadsheet(self):
        old_id = self.secrets['gsheet_id_hydra_template']
        new_title = 'Tug_tester'
        sheetid = self.google_sheets.duplicate_spreadsheet(old_id, new_title)
        return

    def test_request_permissions_update(self):
        self.google_sheets.request_permissions_update()
