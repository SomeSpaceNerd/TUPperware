#!/usr/bin/env bash
set -u

# Prompt “Press any key to exit…” and wait
press_any() {
    echo
    # -n1: read one char; -s: silent (no echo); -r: raw input
    read -n1 -s -r -p "Press any key to exit..."
    echo
}

# Print error, prompt, and exit non‑zero
error_exit() {
    press_any
    exit 1
}

# ————————————————————————————
# 1) Pick a python command (python3 preferred)
# ————————————————————————————
PYTHON_CMD=""
if command -v python3 &>/dev/null; then
    PYTHON_CMD=python3
elif command -v python &>/dev/null; then
    PYTHON_CMD=python
else
    echo "ERROR: Neither python3 nor python is on your PATH."
    error_exit
fi
echo "Using $PYTHON_CMD for Python operations."

# ————————————————————————————
# 2) Check for Python 3.12+
# ————————————————————————————
echo "Checking for Python 3.12 or newer..."
if ! $PYTHON_CMD --version 2>&1 | grep -qE '^Python 3\.(1[2-9]|[2-9][0-9])'; then
    echo "ERROR: Python 3.12 or later is not installed."
    error_exit
fi

# ————————————————————————————
# 3) Check for pip
# ————————————————————————————
echo "Checking for pip..."
if ! $PYTHON_CMD -m pip --version &>/dev/null; then
    echo "pip not found — installing via ensurepip..."
    if ! $PYTHON_CMD -m ensurepip --upgrade &>/dev/null; then
        echo "ERROR: Failed to install pip."
        error_exit
    fi
fi

# ————————————————————————————
# 4) Virtual environment
# ————————————————————————————
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    if ! $PYTHON_CMD -m venv venv &>/dev/null; then
        echo "ERROR: Failed to create virtual environment."
        error_exit
    fi
fi

# Define a variable pointing at the venv’s python for absolute certainty
VENV_PY="$(pwd)/venv/bin/python"
VENV_PIP="$VENV_PY -m pip"

echo "Activating virtual environment..."
# shellcheck disable=SC1091
if ! source venv/bin/activate; then
    echo "ERROR: Could not activate virtual environment."
    error_exit
fi

# Override PYTHON_CMD to point at the venv’s interpreter from here on out
PYTHON_CMD="$VENV_PY"

echo "Upgrading pip in venv..."
if ! $VENV_PIP install --upgrade pip &>/dev/null; then
    echo "ERROR: Failed to upgrade pip inside venv."
    error_exit
fi

echo "Installing requirements..."
if ! $VENV_PIP install -r requirements.txt &>/dev/null; then
    echo "ERROR: Failed to install requirements."
    error_exit
fi

# ————————————————————————————
# 5) Generate UI code
# ————————————————————————————
echo "Generating UI code from form.ui..."
# If the pyside6-uic entry point is only on PATH once the venv is active,
# this will call the venv’s version.
if ! pyside6-uic form.ui -o ui_form.py &>/dev/null; then
    echo "ERROR: UI code generation failed."
    error_exit
fi

# ————————————————————————————
# 6) Launch application
# ————————————————————————————
echo "Launching TUPperware..."
if ! $PYTHON_CMD mainwindow.py; then
    echo "ERROR: Application exited with errors."
    error_exit
fi

echo "TUPperware finished successfully."
press_any
exit 0
