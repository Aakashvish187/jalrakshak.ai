@echo off
echo 🌊 JalRakshā AI Backend Server
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

REM Check if app.py exists
if not exist "app.py" (
    echo ❌ app.py not found in current directory
    echo Please run this script from the project directory
    pause
    exit /b 1
)

echo ✅ Python found
echo 📦 Installing dependencies...
pip install -r requirements.txt

echo.
echo 🚀 Starting JalRakshā AI Backend Server...
echo 📊 Server will be available at: http://localhost:5000
echo 🛑 Press Ctrl+C to stop the server
echo.

python app.py

pause
