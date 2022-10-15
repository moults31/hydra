# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

import sys

import mpy.main

IS_LINUX = (sys.platform == 'linux')

if __name__ == '__main__':
    """
    Micropython auto-run entry point
    """
    auto_run = False
    if auto_run:
        # Jump to real main
        mpy.main.main()