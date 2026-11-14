#!/bin/bash

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

source venv/bin/activate

# Constrain pip's isolated build environment. Required because one source
# dependency's setup.py imports pkg_resources, which setuptools 82 removed.
# See constraints.txt for the full explanation.
export PIP_CONSTRAINT="$(cd "$(dirname "$0")" && pwd)/constraints.txt"
export PIP_BUILD_CONSTRAINT="$PIP_CONSTRAINT" # pip >= 26 build isolation

python -m pip install -U pip
pip install -r requirements.txt && echo "Requirements installed successfully." || {
    echo ""
    echo "Requirements installation failed. Please remove the venv folder and run the script again."
    deactivate
    exit 1
}

deactivate
