#!/bin/bash

#
# This script is used to set up the development environment
#

CURR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SRC_DIR="$CURR_DIR/../src"

source $SRC_DIR/../venv/bin/activate
