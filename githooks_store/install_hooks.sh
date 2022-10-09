#!/bin/bash

# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

################################################
## Installs pre-commit githook                ##
## TO MAKE SURE YOU DON'T COMMIT YOUR SECRETS ##
################################################

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cp $SCRIPT_DIR/pre-commit $SCRIPT_DIR/../.git/hooks