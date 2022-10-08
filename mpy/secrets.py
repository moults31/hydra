# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

"""
Place your app secrets in the fields below!
"""
secrets = {
    'ssid': '',
    'password': '',
    'asana_personal_access_token': ''
}

def get_secrets():
    """
    Returns the programmer-populated secrets dict
    """
    return secrets