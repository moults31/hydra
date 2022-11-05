# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

import sys

import mpy.main

IS_LINUX = (sys.platform == 'linux')

if not IS_LINUX:
    import machine


if __name__ == '__main__':
    """
    Micropython auto-run entry point
    """
    auto_run = True

    if not IS_LINUX:
        # Check if USB peripheral is connected. Credit: https://forum.micropython.org/viewtopic.php?t=10814
        SIE_STATUS=const(0x50110000+0x50)
        CONNECTED=const(1<<16)
        SUSPENDED=const(1<<4)
        if (machine.mem32[SIE_STATUS] & (CONNECTED | SUSPENDED))==CONNECTED:
            # If USB is connected then we want the REPL so don't auto run main
            auto_run = False

    if auto_run:
        # Jump to real main
        mpy.main.main()