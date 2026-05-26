@echo off
setlocal EnableExtensions

cd /d "%~dp0"

set "VENV_DIR=venv"
set "PYTHON_EXE=%VENV_DIR%\Scripts\python.exe"

where python >nul 2>nul
if errorlevel 1 (
    echo Python is not installed or not available on PATH.
    pause
    exit /b 1
)

if not exist "%PYTHON_EXE%" (
    echo Creating virtual environment...
    python -m venv "%VENV_DIR%"
    if errorlevel 1 goto :error
)

echo Installing dependencies...
"%PYTHON_EXE%" -m pip install --upgrade pip
if errorlevel 1 goto :error

"%PYTHON_EXE%" -m pip install -r requirements.txt
if errorlevel 1 goto :error

echo.
echo Starting AI Log Investigation API...
echo Open http://localhost:8000/docs after the server starts.
echo.
start "" /b powershell -NoProfile -ExecutionPolicy Bypass -Command "$ready = $false; while (-not $ready) { try { Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8000/docs -TimeoutSec 1 | Out-Null; $ready = $true } catch { Start-Sleep -Milliseconds 500 } }; Start-Process http://localhost:8000/docs"
"%PYTHON_EXE%" -m uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000
if errorlevel 1 goto :error

goto :end

:error
echo.
echo Failed to start the application.
pause

:end
endlocal
