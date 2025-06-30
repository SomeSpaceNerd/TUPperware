@echo off
setlocal enabledelayedexpansion

rem ————————————————————————————
rem  Pick a python command (python3 preferred)
rem ————————————————————————————
set "PYTHON_CMD="
where python3 >nul 2>&1 && set "PYTHON_CMD=python3"
if "%PYTHON_CMD%"=="" (
    where python >nul 2>&1 && set "PYTHON_CMD=python"
)
if "%PYTHON_CMD%"=="" (
    echo ERROR: Neither python3 nor python was found on PATH.
    goto Error
)
echo Using %PYTHON_CMD% for all Python operations.

rem ————————————————————————————
rem  1) Check for Python 3.12+
rem ————————————————————————————
echo Checking for Python 3.12 or newer...
%PYTHON_CMD% --version 2>&1 | findstr /r "^Python 3\.\(1[2-9]\|[2-9][0-9]\)" >nul || (
    echo ERROR: Python 3.12 or later is not installed.
    goto Error
)

rem ————————————————————————————
rem  2) Check for pip
rem ————————————————————————————
echo Checking for pip...
%PYTHON_CMD% -m pip --version >nul 2>&1 || (
    echo pip is not installed. Installing via ensurepip...
    %PYTHON_CMD% -m ensurepip --upgrade >nul 2>&1 || (
        echo ERROR: Failed to install pip.
        goto Error
    )
)

rem ————————————————————————————
rem  3) Virtual environment
rem ————————————————————————————
echo Checking for preexisting virtual environment...
if not exist "venv\" (
    echo Creating virtual environment...
    %PYTHON_CMD% -m venv venv >nul 2>&1 || (
        echo ERROR: Failed to create virtual environment.
        goto Error
    )
)

echo Activating virtual environment...
call venv\Scripts\activate.bat >nul 2>&1 || (
    echo ERROR: Could not activate virtual environment.
    goto Error
)
set "PYTHON_CMD=%~dp0venv\Scripts\python.exe"

echo Upgrading pip inside venv...
%PYTHON_CMD% -m pip install --upgrade pip >nul 2>&1 || (
    echo ERROR: Failed to upgrade pip in venv.
    goto Error
)

echo Installing requirements...
%PYTHON_CMD% -m pip install -r requirements.txt >nul 2>&1 || (
    echo ERROR: Failed to install requirements.
    goto Error
)

rem ————————————————————————————
rem  4) Generate UI code
rem ————————————————————————————
echo Generating UI code...
pyside6-uic form.ui -o ui_form.py >nul 2>&1 || (
    echo ERROR: UI code generation failed.
    goto Error
)

rem ————————————————————————————
rem  5) Launch application
rem ————————————————————————————
echo Launching TUPperware...
%PYTHON_CMD% mainwindow.py 2>&1 || (
    echo ERROR: Application exited with errors.
    goto Error
)

echo TUPperware finished successfully.
echo.
pause >nul
exit /b 0

rem ————————————————————————————
rem  Error handler
rem ————————————————————————————
:Error
echo.
echo Press any key to exit...
pause >nul
exit /b 1
