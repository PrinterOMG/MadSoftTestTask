#!/bin/sh

set -e

# Activating virtual environment
. /opt/pysetup/.venv/bin/activate

# Evaluating passed command
exec "$@"
