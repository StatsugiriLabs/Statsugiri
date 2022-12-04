#!/bin/bash

#
# This script is used for running formatting checks in CI
# Please run `setup.sh` in `environment_setup` first
# Credit to UBC Thunderbots
# https://github.com/UBC-Thunderbots
#

CURR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SRC_DIR="$CURR_DIR/../src"
LINT_THRESHOLD=8

# Function to check if formatting dependencies are available
function check_dependencies () {
    printf "Checking if dependencies are available...\n\n"
    # Check if black formatter available
    black --version &>/dev/null
    if [[ "$?" != 0 ]]; then
        printf "\n***Black formatter is not installed. Please run `setup.sh` first.***\n\n"
        exit 1
    fi
    # Check if pylint available
    pylint --version &>/dev/null
    if [[ "$?" != 0 ]]; then
        printf "\n***Pylint is not installed. Please run `setup.sh` first.***\n\n"
        exit 1
    fi
}

# Function to run black python formatting
function run_black_formatting () {
    printf "Running Black to format Python files...\n\n"
    # Suppress messages
    black $SRC_DIR &>/dev/null

    if [[ "$?" != 0 ]]; then
        printf "\n***Failed to format Python files!***\n\n"
        exit 1
    fi
}

# Function to run lint check
function run_pylint_linting () {
    printf "Running Pylint to check Python linting...\n\n"
    # Suppress messages
    pylint --fail-under=$LINT_THRESHOLD $SRC_DIR/**/*.py --rcfile=$CURR_DIR/../.pylintrc $>/dev/null

    if [[ "$?" != 0 ]]; then
        printf "\n***Python linting did not pass threshold of 9.0! Run `../test_scripts/run_pylint.sh` for log***\n\n"
        exit 1
    fi
}

function run_eof_new_line(){
    printf "Adding missing new lines to end of files...\n\n"

    # adds missing new lines to the end of non-binary files
    cd $CURR_DIR/../ && git grep -zIl '' | while IFS= read -rd '' f; do tail -c1 < "$f" | read -r _ || echo >> "$f"; done
    if [[ "$?" != 0 ]]; then
        printf "***Failed to add missing new lines!***\n\n"
        exit 1
    fi
}

# Check dependencies available
check_dependencies
# Run formatting
run_black_formatting
run_pylint_linting
run_eof_new_line

exit 0
