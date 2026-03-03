@echo off
setlocal EnableDelayedExpansion

echo ==================================================
echo        AI X-Ray Assistant - Smart Launcher
echo ==================================================
echo.

:: ── Navigate to script directory ──────────────────
cd /d "%~dp0"

:: ── Find Python ───────────────────────────────────
set PYTHON_CMD=

:: Try common python commands in order of preference
for %%P in (python python3 py) do (
    if "!PYTHON_CMD!"=="" (
        where %%P >nul 2>&1
        if !errorlevel! == 0 (
            set PYTHON_CMD=%%P
        )
    )
)

:: Also check common install paths on Windows
if "!PYTHON_CMD!"=="" (
    for %%D in (
        "%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
        "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
        "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
        "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
        "C:\Python313\python.exe"
        "C:\Python312\python.exe"
        "C:\Python311\python.exe"
        "C:\Python310\python.exe"
    ) do (
        if "!PYTHON_CMD!"=="" (
            if exist %%D (
                set PYTHON_CMD=%%~D
            )
        )
    )
)

if "!PYTHON_CMD!"=="" (
    echo [ERROR] Python not found on this system.
    echo Please install Python 3.10 or later from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

:: Show Python version found
for /f "tokens=*" %%V in ('!PYTHON_CMD! --version 2^>^&1') do set PY_VER=%%V
echo [INFO] Found: !PY_VER! at "!PYTHON_CMD!"

:: ── Venv Setup ────────────────────────────────────
if exist "venv\Scripts\python.exe" (
    echo [INFO] Existing virtual environment found. Reusing it.
    set VENV_PYTHON=venv\Scripts\python.exe
    goto :activate
)

echo [INFO] No virtual environment found. Creating one...
echo [1/3] Creating virtual environment...
!PYTHON_CMD! -m venv venv
if !errorlevel! neq 0 (
    echo [ERROR] Failed to create virtual environment.
    echo Try running:  !PYTHON_CMD! -m pip install virtualenv
    pause
    exit /b 1
)
echo        Done.

:activate
echo [2/3] Activating environment...
call venv\Scripts\activate.bat

:: ── Install / Update Dependencies ─────────────────
echo [3/3] Installing / updating dependencies...
pip install --upgrade pip -q
pip install -r requirements.txt
if !errorlevel! neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

echo.
echo ==================================================
echo   Setup complete! Launching app...
echo ==================================================
echo.

:: ── Launch Streamlit ──────────────────────────────
streamlit run app.py
pause
