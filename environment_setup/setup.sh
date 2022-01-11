#!/bin/bash

#
# This script will set up the development environment
#

CURR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SRC_DIR="$CURR_DIR/../src"

# Function to check if pip is installed
function check_pip () {
    # Check if pip available
    pip --version &>/dev/null
    if [[ "$?" != 0 ]]; then
        printf "\n***Pip is not installed. Please refer to `environment_setup.md`.***\n\n"
        exit 1
    fi
}

function install_python_dependencies () {
    # Update pip
    python -m pip install --upgrade pip
    if [[ "$?" != 0 ]]; then
        printf "\n***Pip update failed!***\n\n"
        exit 1
    fi
    pip install -r $SRC_DIR/data_pipeline/requirements.txt
    if [[ "$?" != 0 ]]; then
        printf "\n***Python dependencies failed to install!***\n\n"
        exit 1
    fi
}

# Run setup
check_pip
install_python_dependencies
printf "\n***Setup complete! Please set environment variables for ACCESS_KEY_ID, SECRET_ACCESS_KEY, and REGION_NAME for AWS authentication.***\n\n"

exit 0
