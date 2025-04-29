#!/bin/bash

# Check for Python 3.12+
if ! python3 --version | grep -qE '^Python 3\.(1[2-9]|[2-9][0-9])'; then
    echo "Python 3.12 or later is not installed. Exiting..."
    exit 1
fi

# Check for pip
if ! python3 -m pip --version &>/dev/null; then
    echo "pip is not installed. Installing pip..."
    python3 -m ensurepip --upgrade
    if [ $? -ne 0 ]; then
        echo "Failed to install pip. Exiting..."
        exit 1
    fi
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment. Exiting..."
        exit 1
    fi
    source venv/bin/activate
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Generate UI code
pyside6-uic form.ui -o ui_form.py

# Run main window
python mainwindow.py
