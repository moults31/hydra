# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

"""
Simple wrapper for sending HTTP requests to Asana API
"""

import urequests as requests

import mpy.secrets as secrets

class Simple_asana:
    endpoint_hello_world = "https://app.asana.com/api/1.0/users/me"

    def __init__(self):
        self.token = secrets.get_secrets()['asana_personal_access_token']
        self.hello_world()

    def hello_world(self):
        """
        Makes a request for the personal access token owner's user info and prints the response
        """
        data = {}
        headers = {"Authorization": f"Bearer {self.token}"}

        print(requests.get(self.endpoint_hello_world, data=data, headers=headers).json())
