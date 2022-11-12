# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

import sys

import mpy.main

import mpy.util.util as util

IS_LINUX = (sys.platform == 'linux')

if not IS_LINUX:
    import machine


if __name__ == '__main__':
    """
    Micropython auto-run entry point
    """
    auto_run = True

    if not IS_LINUX:
        if util.get_usb_connected():
            # If USB is connected then we want the REPL so don't auto run main
            auto_run = False

    if auto_run:
        # Jump to real main
        mpy.main.main()