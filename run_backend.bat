@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo [1/2] Creating Python virtual environment...
    py -3.11 -m venv .venv
    if errorlevel 1 (
        echo Could not create the virtual environment. Install Python 3.11 first.
        pause
        exit /b 1
    )
)
echo [2/2] Installing/checking backend dependencies...
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
    echo Dependency installation failed.
    pause
    exit /b 1
)
echo.
echo Starting CareerForge AI backend at http://127.0.0.1:5000
.venv\Scripts\python.exe app.py
pause
