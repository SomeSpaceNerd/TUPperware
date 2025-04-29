@echo off
:: Check for Python 3.12+
python3 --version 2>nul | findstr /r "^Python 3\.\(1[2-9]\|[2-9][0-9]\)" >nul
if errorlevel 1 (
    echo Python 3.12 or later is not installed. Exiting...
    exit /b
)

:: Check for pip
python3 -m pip --version >nul 2>&1
if errorlevel 1 (
    echo pip is not installed. Installing pip...
    python3 -m ensurepip --upgrade
    if errorlevel 1 (
        echo Failed to install pip. Exiting...
        exit /b
    )
)

:: Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python3 -m venv venv
    if errorlevel 1 (
        echo Failed to create virtual environment. Exiting...
        exit /b
    )
    call venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

:: Generate UI code
pyside6-uic form.ui -o ui_form.py

:: Run main window
python mainwindow.py
