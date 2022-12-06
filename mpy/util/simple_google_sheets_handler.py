# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

"""
Simple handler for building application-specific Google requests
and sending them to the simple API
"""

import time
import gc

import urequests as requests

import mpy.secrets as secrets
import mpy.util.simple_google_sheets_api as api
import mpy.util.simple_asana_handler as asana

import sys
IS_LINUX = (sys.platform == 'linux')
if not IS_LINUX:
    from machine import Pin

class Simple_google_handler:
    """
    Simple wrapper for sending HTTP requests to Google API
    """

    HEADER = ['POSIX Time', 'Temp (C)', 'Light (Lux)']

    SHEET_URI = 'https://docs.google.com/spreadsheets/d'

    header_uploaded = False

    # Memory tracking
    mem_tracker = []
    mem_free_after_gc_prev = 0

    def __init__(self, new_sheet_name=None, existing_sheet_name='', subsheet='Sheet1'):
        self.sheet_name = subsheet
        self.asana = asana.Simple_asana_handler()
        self.jwt = self.asana.get_jwt()

        _secrets = secrets.get_secrets()

        self.permission_updater_url = _secrets['hydra_permission_updater_url']

        # If the existing sheet name is valid then use it
        if self.SHEET_URI in existing_sheet_name:
            self.sheet_id = existing_sheet_name.split(f'{self.SHEET_URI}/')[1]
            print(f'Using existing sheet {self.sheet_id}')

        # Otherwise create a new one with the specified name if provided
        elif new_sheet_name:
            new_sheet_name_sanitized = new_sheet_name.replace(' ', '_')
            print(f'Creating new sheet with name {new_sheet_name_sanitized} ...')
            self.sheet_id = self.duplicate_spreadsheet(_secrets['gsheet_id_hydra_template'], new_sheet_name_sanitized)
            print(f'Done, new id {self.sheet_id}')

        # If no new name provided then just use the default sandbox sheet
        else:
            self.sheet_id = _secrets['gsheet_id_default']
            print(f'Using default sheet {self.sheet_id}')

        # Init mem tracking
        gc.collect()
        self.mem_free_after_gc_prev = gc.mem_free()

        # Get LED pin if running on mpy hardware
        if not IS_LINUX:
            self.pin = Pin("LED", Pin.OUT)

    def _rowcol_to_a1(self, row, col):
        """
        Taken as-is from https://github.com/burnash/gspread/blob/master/gspread/utils.py
        Translates a row and column cell address to A1 notation.
        :param row: The row of the cell to be converted.
            Rows start at index 1.
        :type row: int, str
        :param col: The column of the cell to be converted.
            Columns start at index 1.
        :type row: int, str
        :returns: a string containing the cell's coordinates in A1 notation.
        Example:
        >>> rowcol_to_a1(1, 1)
        A1
        """
        row = int(row)
        col = int(col)

        if row < 1 or col < 1:
            raise Exception("({}, {})".format(row, col))

        div = col
        column_label = ""

        while div:
            (div, mod) = divmod(div, 26)
            if mod == 0:
                mod = 26
                div -= 1
            column_label = chr(mod + 64) + column_label

        label = "{}{}".format(column_label, row)

        return label

    def get_jwt(self):
        """
        Get a signed JWT come hell or high water
        """
        self.jwt = self.asana.get_jwt()

    def upload_header(self):
        """
        Upload the header line to the sheet
        """
        start = self._rowcol_to_a1(1,1)
        end = self._rowcol_to_a1(1,len(self.HEADER))
        range = f'{start}:{end}'
        r = api.update_range(self.jwt, self.sheet_id, self.sheet_name, cell_range=range, values=[self.HEADER])

        update_succeeded = False
        if r != False:
            if not 'error' in r.keys():
                update_succeeded = True

        return update_succeeded

    def upload_list(self, values):
        """
        Upload a 2D list of values to the sheet
        """
        print("Trying upload_list")

        # If mem_free dropped by a lot, log the mem_tracker from the previous iter
        mem_tracker = []
        gc.collect()
        mem_free_after_gc = gc.mem_free()
        if self.mem_free_after_gc_prev - mem_free_after_gc > 5000:
            print(f"Memory dropped from {self.mem_free_after_gc_prev} to {mem_free_after_gc}. Reporting to file.")
            with open(f'mem_free_{self.mem_free_after_gc_prev}_to_{mem_free_after_gc}.txt', 'w') as f:
                f.write(str(self.mem_tracker))

        # Remember mem_free_after_gc for next iteration
        self.mem_free_after_gc_prev = mem_free_after_gc

        # We will append after a dummy table at the first non-header cell
        start = self._rowcol_to_a1(2, 1)
        end = self._rowcol_to_a1(2, 1)
        cell_range = f'{start}:{end}'

        self.get_jwt()

        print("upload_list: about to append_range")
        r = api.append_range(self.jwt, self.sheet_id, self.sheet_name, cell_range=cell_range, values=values)
        print("upload_list: done append_range")

        update_succeeded = False
        if r != False:
            if not 'error' in r.keys():
                update_succeeded = True

        # Force garbage collection since r can take up a ton of RAM
        gc.collect()
        mem_tracker.append(gc.mem_free())

        rv = False

        # TODO: We shouldn't block sensor samples on these retries
        if update_succeeded != False:
            print('upload_list: Success!')
            rv = True

        self.mem_tracker = mem_tracker
        print(mem_tracker)

        return rv

    def create_spreadsheet(self, title):
        """
        Creates a spreadsheet with the given title.
        Returns new sheetId on success, False on failure.
        """
        # Create the spreadsheet
        sheet_id = api.create_spreadsheet(self.jwt, title)
        # Request a permission update to share it with human users
        self.request_permissions_update()
        # Return the new spreadsheet id
        return sheet_id

    def duplicate_spreadsheet(self, old_id, new_title):
        """
        Duplicates a spreadsheet with the given title.
        Returns new sheetId on success, False on failure.
        """
        new_id = self.create_spreadsheet(new_title)

        for gid in self.get_sheet_gids_in_spreadsheet(old_id):
            api.copy_sheet(self.jwt, old_id, new_id, gid)

        self.sanitize_new_sheet_names(new_id)

        return new_id

    def get_sheet_gids_in_spreadsheet(self, sheet_id):
        """
        Returns a list of sheet gids in the given spreadsheet
        """
        r = api.get_spreadsheet(self.jwt, sheet_id, fields='sheets.properties.sheetId')
        sheets = r['sheets']

        sheet_gids = []
        for sheet in sheets:
            sheet_gids.append(sheet['properties']['sheetId'])

        return sheet_gids

    def sanitize_new_sheet_names(self, sheet_id):
        """
        Cleans up sheet names in a newly created spreadsheet.
        Removes the default Sheet1.
        Strips "Copy of" from the names of any sheets that have that.
        """
        r = api.get_spreadsheet(self.jwt, sheet_id, fields='sheets.properties(sheetId,title)')
        sheets = r['sheets']

        # Build up list of batchUpdate requests
        requests_arr = []
        for sheet in sheets:
            title = sheet['properties']['title']
            id = sheet['properties']['sheetId']

            # Delete any sheets named SheetX
            if 'Sheet' in title:
                request = {
                    "deleteSheet": {
                        "sheetId": id
                    }
                }
                requests_arr.append(request)

            # Strip "Copy of " from any sheet names that have it
            elif 'Copy of' in title:
                new_title = title.split('Copy of ')[1]
                request = {
                    "updateSheetProperties": {
                        "properties": {
                            "title": new_title,
                            "sheetId": id,
                        },
                        "fields": "title"
                    }
                }
                requests_arr.append(request)

        if len(requests_arr):
            # Wrap list of requests in batchUpdate-compatible json body
            batch_update_body = {
                "requests": requests_arr,
                "includeSpreadsheetInResponse": False,
                "responseRanges": [
                    ""
                ],
                "responseIncludeGridData": False
            }

            # Send the request and return the response (which will likely be unused)
            api.batch_update(self.jwt, sheet_id, batch_update_body)

        return

    def get_active_sheet_url(self):
        """
        Returns a URL that a user could use to access the active sheet 
        """
        return f'{self.SHEET_URI}/{self.sheet_id}'

    def request_permissions_update(self):
        """
        Sends a request to the permissions updater endpoint serving
        https://github.com/moults31/hydra-gsheet-permission-updater
        """
        requests.get(self.permission_updater_url)