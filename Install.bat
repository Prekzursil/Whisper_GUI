@echo off

if not exist "%~dp0\venv\Scripts" (
    echo Creating venv...
    python -m venv venv
)
echo checked the venv folder. now installing requirements..

call "%~dp0\venv\scripts\activate"

REM Constrain pip's isolated build environment. Required because one source
REM dependency's setup.py imports pkg_resources, which setuptools 82 removed.
REM See constraints.txt for the full explanation.
set "PIP_CONSTRAINT=%~dp0constraints.txt"

python -m pip install -U pip
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Requirements installation failed. please remove venv folder and run install.bat again.
) else (
    echo.
    echo Requirements installed successfully.
)
pause