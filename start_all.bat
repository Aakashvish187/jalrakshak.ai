@echo off
echo 🌊 JalRakshā AI - Complete System Startup
echo ================================================
echo.

echo 🔧 Starting Flask Backend Server...
start "Flask Backend" cmd /k "python app.py"

echo ⏳ Waiting for backend to start...
timeout /t 3 /nobreak > nul

echo 🌐 Starting Frontend Server...
start "Frontend Server" cmd /k "python -m http.server 8080"

echo ⏳ Waiting for frontend to start...
timeout /t 2 /nobreak > nul

echo 🤖 Starting Telegram Bot...
start "Telegram Bot" cmd /k "python start_telegram_bot.py"

echo.
echo ✅ All services started!
echo.
echo 📱 Frontend: http://localhost:8080/index.html
echo 🔧 Backend: http://localhost:5000
echo 🤖 Telegram Bot: Running
echo.
echo 💡 Press any key to open the website...
pause > nul

start http://localhost:8080/index.html

echo.
echo 🎉 JalRakshā AI System is now running!
echo.
echo 📋 Services Status:
echo    ✅ Flask Backend (Port 5000)
echo    ✅ Frontend Server (Port 8080)  
echo    ✅ Telegram Bot (Active)
echo.
echo 🚀 Ready for hackathon demo!
pause
