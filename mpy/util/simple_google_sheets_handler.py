# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

"""
Simple handler for building application-specific Google requests
and sending them to the simple API
"""

import time

import mpy.secrets as secrets
import mpy.util.simple_google_sheets_api as api
import mpy.util.simple_asana_handler as asana

class Simple_google_handler:
    """
    Simple wrapper for sending HTTP requests to Google API
    """

    HEADER = ['POSIX Time', 'Temp (C)', 'Light (Lux)']

    header_uploaded = False

    def __init__(self, row_idx=1):
        self.row_idx = row_idx
        self.sheet_id = secrets.get_secrets()['gsheet_id']
        self.asana = asana.Simple_asana_handler()
        self.jwt = self.asana.get_jwt()

        if self.row_idx == 1:
            header_uploaded = self.upload_header()

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
        sheet_name = 'Sheet3'
        r = api.update_range(self.jwt, self.sheet_id, sheet_name, cell_range=range, values=[self.HEADER])

        update_succeeded = False
        if r != False:
            if not 'error' in r.keys():
                update_succeeded = True

        if update_succeeded:
            # Start from row 2 now since header occupies row 1
            self.row_idx = 2

        return update_succeeded

    def upload_list(self, values):
        """
        Upload a 2D list of values to the sheet
        """
        # api.query_big()
        print("Trying upload_list")
        shape = len(values), len(values[0])

        # Start at [next row index, first index]
        # End at [height of a sample + next row index, width of a sample]
        start = self._rowcol_to_a1(self.row_idx, 1)
        end = self._rowcol_to_a1(self.row_idx + shape[0], shape[1])

        cell_range = f'{start}:{end}'
        sheet_name = 'Sheet3'

        self.get_jwt()

        print("upload_list: about to update_range")
        r = api.update_range(self.jwt, self.sheet_id, sheet_name, cell_range=cell_range, values=values)
        print("upload_list: done update_range")

        update_succeeded = False
        if r != False:
            if not 'error' in r.keys():
                update_succeeded = True

        # TODO: We shouldn't block sensor samples on these retries
        if update_succeeded != False:
            self.row_idx += shape[0]
            print('upload_list: Success!')
            return True
        # else:
        #     for i in range(10):
        #         print(f'Retry #{i+1}...')
        #         self.get_jwt()
        #         r = api.update_range(self.jwt, self.sheet_id, sheet_name, cell_range=cell_range, values=values)
                
        #         update_succeeded = False
        #         if r != False:
        #             if not 'error' in r.keys():
        #                 update_succeeded = True
                
        #         if update_succeeded != False:
        #             self.row_idx += shape[0]
        #             print('upload_list: Success!')
        #             return True
        #         time.sleep(5)

        return False
