# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

import mpy.app.fermentation_tracker as fermentation_tracker
import mpy.app.coldcrash_tracker as coldcrash_tracker

if __name__ == '__main__':
    """
    Main entry point to micropython program.
    """

    # TODO: Read switch or something to decide which app to run.
    # For now hardcode it.
    app = 'fermentation_tracker'
    # app = 'coldcrash_tracker'

    if app == 'fermentation_tracker':
        ft = fermentation_tracker.Fermentation_tracker()
        ft.run_blocking()
    elif app == 'coldcrash_tracker':
        ct = coldcrash_tracker.Coldcrash_tracker()
        ct.run_blocking()
    else:
        raise Exception("No app selected!")
