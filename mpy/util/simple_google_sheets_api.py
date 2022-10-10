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

def _build_header(token, content_type=None, accept=None):
    headers = {}

    if content_type:
        headers['Content-type'] = content_type

    if accept:
        headers['Accept'] = accept

    headers['Authorization'] = f'Bearer {token}'

    return headers

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