# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

"""
Simple stateless wrapper for sending HTTP requests to Asana API.
Exposes only the endpoints required for hydra's applications.
Only supports personal access token authentication, not client authentication.
"""

import urequests as requests

ENDPOINT_BASE = "https://sheets.googleapis.com/v4/spreadsheets"

def exception_wrapper(func):
    """
    Decorator to prevent us from hanging when an exception is raised by urequests
    """
    def wrapper(*args, **kwargs):
        try:
            rv = func(*args, **kwargs)
            return rv
        except BaseException as e:
            print(f"WARNING: Ignoring exception thrown by {func.__name__}. Details:")
            print(e)
            return False
    return wrapper

def _build_header(token, content_type=None, accept=None):
    headers = {}

    if content_type:
        headers['Content-type'] = content_type

    if accept:
        headers['Accept'] = accept

    headers['Authorization'] = f'Bearer {token}'

    return headers

@exception_wrapper
def get_range(token, sheet_id, sheet_name, cell_range):
    """
    Returns content from the specified cell_range of the specified sheet
    """
    headers = _build_header(token, content_type='application/json')
    endpoint = f'{ENDPOINT_BASE}/{sheet_id}/values/{sheet_name}!{cell_range}'
    r = requests.get(endpoint, headers=headers)
    return r.json()

def update_range(token, sheet_id, sheet_name, cell_range, values):
    """
    Updates the specified cell_range of the specified sheet
    """
    headers = _build_header(token, content_type='application/json')
    endpoint = f'{ENDPOINT_BASE}/{sheet_id}/values/{sheet_name}!{cell_range}?valueInputOption=RAW'
    body = {
        "values": values
    }
    r = requests.put(endpoint, headers=headers, json=body)
    return r.json()

def append_range(token, sheet_id, sheet_name, cell_range, values):
    """
    Updates the specified cell_range of the specified sheet
    """
    headers = _build_header(token, content_type='application/json')
    endpoint = f'{ENDPOINT_BASE}/{sheet_id}/values/{sheet_name}!{cell_range}:append?valueInputOption=RAW'
    body = {
        "values": values
    }
    r = requests.post(endpoint, headers=headers, json=body)
    return r.json()

@exception_wrapper
def create_spreadsheet(token, title):
    """
    Creates a spreadsheet with the given title.
    Returns new sheetId on success, False on failure.
    """
    headers = _build_header(token, content_type='application/json')
    endpoint = f'{ENDPOINT_BASE}'
    body = {
        "properties": {
            "title": title,
            "locale": "en_US",
            "autoRecalc": "ON_CHANGE",
            "timeZone": "Etc/GMT",
            "defaultFormat": {
            }
        },
        "sheets": [
        ],
    }
    r = requests.post(endpoint, headers=headers, json=body)

    return r.json()['spreadsheetId']

@exception_wrapper
def copy_sheet(token, from_id, to_id, gid):
    """
    Copies a single sheet (gid) from within one spreadsheet (from_id)
    to another spreadsheet (to_id)
    """
    headers = _build_header(token, content_type='application/json')
    endpoint = f"{ENDPOINT_BASE}/{from_id}/sheets/{gid}:copyTo"
    body = {
        "destinationSpreadsheetId": to_id
    }
    r = requests.post(endpoint, headers=headers, json=body)
    return r.json()

def get_spreadsheet(token, id, fields=None):
    """
    Returns a spreadsheet object for the spreadsheet with the specified id
    """
    headers = _build_header(token, content_type='application/json')
    endpoint = f"{ENDPOINT_BASE}/{id}"
    if fields:
        endpoint = endpoint + f'?fields={fields}'
    r = requests.get(endpoint, headers=headers)
    return r.json()

@exception_wrapper
def batch_update(token, id, body):
    """
    Performs a batch update on the specified spreadsheet.
    Caller is responsible for building up the body.
    https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/batchUpdate
    """
    headers = _build_header(token, content_type='application/json')
    endpoint = f"{ENDPOINT_BASE}/{id}:batchUpdate"
    r = requests.post(endpoint, headers=headers, json=body)
    return r.json()
