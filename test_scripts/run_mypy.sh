#!/bin/bash

#
# This script is used for running `mypy` to check Python type stubs
#

CURR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SRC_DIR="$CURR_DIR/../src"

function run_mypy () {
    mypy $SRC_DIR/**/*.py
}

# Run pylint
run_mypy

exit 0
