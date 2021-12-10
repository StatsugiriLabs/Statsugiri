#!/bin/bash

#
# This script is used for running all tests
#

CURR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SRC_DIR="$CURR_DIR/../src"

function run_pytest () {
    PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider $SRC_DIR &>/dev/null
    if [[ "$?" != 0 ]]; then
        printf "\n***Python tests failed!***\n\n"
        exit 1
    fi
}

# Run tests
run_pytest

exit 0
