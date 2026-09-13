@echo off
setlocal
cd /d "%~dp0"
echo Creating CareerForge AI backend environment...
py -3.11 -m venv .venv
if errorlevel 1 (
    echo Python 3.11 was not found. Install Python 3.11 and run this again.
    pause
    exit /b 1
)
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
    echo Dependency installation failed.
    pause
    exit /b 1
)
if not exist ".env" copy ".env.example" ".env" >nul
echo.
echo Backend setup complete.
echo Run run_backend.bat to start CareerForge AI.
pause
