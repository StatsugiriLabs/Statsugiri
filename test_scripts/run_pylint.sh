#!/bin/bash

#
# This script is used for running `pylint` to lint Python files
#

CURR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SRC_DIR="$CURR_DIR/../src"
LINT_THRESHOLD=9

function run_pylint () {
    pylint --fail-under=$LINT_THRESHOLD $SRC_DIR/**/*.py --rcfile=$CURR_DIR/../.pylintrc
}

# Run pylint
run_pylint

exit 0
