#!/bin/bash

#
# This script is used for running `pylint` to lint Python files
#

CURR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SRC_DIR="$CURR_DIR/../src"

function run_pylint () {
    pylint $SRC_DIR/**/*.py --rcfile=$CURR_DIR/../.pylintrc
}

# Run pylint
run_pylint

exit 0
