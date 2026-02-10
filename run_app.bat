@echo off
TITLE AI X-Ray Assistant
echo ==================================================
echo        AI X-Ray Assistant - Launcher
echo ==================================================
echo.

cd /d "%~dp0"

IF EXIST "venv\Scripts\activate.bat" goto :ACTIVATE

echo [INFO] No virtual environment found. Creating one...
echo.

py --version >nul 2>&1
if errorlevel 1 goto :NOPYTHON

echo [1/3] Creating virtual environment...
py -m venv venv
if errorlevel 1 goto :FAIL

echo [2/3] Activating...
call venv\Scripts\activate.bat

echo [3/3] Installing dependencies (this may take a few minutes)...
pip install -r requirements.txt
if errorlevel 1 goto :FAIL

echo.
echo [OK] Setup complete!
echo.
goto :RUN

:ACTIVATE
echo [INFO] Virtual environment found.
call venv\Scripts\activate.bat
goto :RUN

:RUN
echo.
echo Starting app... (Close this window to stop)
echo.
python -m streamlit run app.py
goto :END

:NOPYTHON
echo.
echo [ERROR] Python not found! Install from https://www.python.org
echo         Make sure to check "Add Python to PATH"
goto :END

:FAIL
echo.
echo [ERROR] Something went wrong. See messages above.
goto :END

:END
echo.
pause
