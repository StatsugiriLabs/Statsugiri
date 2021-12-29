#!/bin/bash

#
# This script is used for running data pipeline tests
#

CURR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SRC_DIR="$CURR_DIR/../src"

function run_data_pipeline_tests () {
    PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider $SRC_DIR/data_pipeline
    if [[ "$?" != 0 ]]; then
        printf "\n***Python tests failed!***\n\n"
        exit 1
    fi
}

# Run tests
run_data_pipeline_tests

exit 0
